# NeMo AI
from nemoguardrails import RailsConfig
from nemoguardrails.rails import LLMRails

import asyncio

# LangChain
from langchain.chat_models import init_chat_model
from langchain.tools import Tool
from langchain.agents import initialize_agent

# LangFuse
from langfuse.langchain import CallbackHandler

# Tools
from ai.rag_tool import RAGTool
from ai.sql_tool import SQLTool
from ai.web_tool import WebTool


class OrchestratorAgent:
    def __init__(self, model_:str, callback_handler=CallbackHandler, agent="zero-shot-react-description"):
        # Carrega as regras do NeMo Guardrails
        config = RailsConfig.from_path("./config")
        self.rails = LLMRails(config)

        # CallbackHandler do LangFuse (parâmetros no Env)
        self.callback_handler = callback_handler()
        
        # Instância de IA
        self.llm = init_chat_model(model_, model_provider="openai")

        # Instância das classes das tools
        rag_tool = RAGTool(self.llm)
        sql_tool = SQLTool(self.llm, callback_handler=self.callback_handler)
        web_tool = WebTool()

        self.tools = [
            Tool(
                name="PostgreSQL Query Tool",
                func=sql_tool.ask_sql,
                description="Use isso para responder perguntas sobre notícias resumidas, impacto de notícias para a Petrobrás, e key takeaways sobre notícias. Não utilize como fonte de dados financeiros."
            ),
            Tool(
                name="Chroma RAG Tool",
                func=rag_tool.rag_chain.run,
                description="Use isso para ter responder com informações sobre a atuação, estratégia, riscos e regulamentação da Petrobrás."
            ),
            Tool(
                name="Web Search",
                func=web_tool.tavily_search,
                description="Use isso responder perguntas com dados da internet."
            )
        ]

        # Instância de agente
        self.agent_executor = initialize_agent(
            self.tools,
            self.llm,
            agent=agent,
            verbose=True,
            handle_parsing_errors=True
        )

    async def ask_ai(self, prompt):
        # Guardrails
        print("Avaliando Guardrail", end="... ")

        guardrail_prompt = prompt.split("Responda a seguinte pergunta:")[-1]
        print(guardrail_prompt)
        resposta_guardrails = await self.rails.generate_async(guardrail_prompt, options={"rails": ["input"]})
        if resposta_guardrails.response == "Me utilize apenas como uma ferramenta para obter informações relevantes para a Petrobrás. Não posso responder essa pergunta.":
            print(f"Bloqueada: {resposta_guardrails.response}")
            return resposta_guardrails.response
        else:
            print("") # Debug

        # Resposta do Agente
        resposta_agente = self.agent_executor.run(prompt, callbacks=[self.callback_handler])
        print(resposta_agente)
        return resposta_agente