# LangChain
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate
from langchain.chains.sql_database.prompt import PROMPT


class SQLTool:
    def __init__(self, llm, callback_handler):
        self.callback_handler = callback_handler

        # Conexão com o PostgreSQL
        self.db = SQLDatabase.from_uri(
            "postgresql+psycopg2://postgres:senha@localhost/postgres",  # troque 'senha' pela real
            include_tables=["summaries"],
            schema="ai"
        )

        custom_prefix = """Você é um especialista em PostgreSQL com acesso a apenas uma tabela chamada 'summaries' no schema 'ai'.

        Ela tem as seguintes colunas:
        - url: string (link da notícia)
        - summary: string (resumo da notícia)
        - title: string (título da notícia)
        - impacto: string (indica se a notícia teve impacto positivo ou negativo. valores possíveis: 'Positivo', 'Negativo')
        - relevancia: string (indica o quão intenso é o impacto da notícia. valores possíveis: 'Alta', 'Media', 'Baixa')
        - takeaways: string (frase com pontos chave sobre o impacto da notícia na Petrobrás)
        - date: date (data da notícia no formato YYYY-MM-DD)

        Você deve responder **somente com código SQL válido e sem usar blocos markdown** como ```sql.
        Nunca explique a resposta. Retorne apenas a query SQL correta.
        """

        self.custom_prompt = PromptTemplate(
            input_variables=["input", "table_info", "dialect"],
            template=custom_prefix + "\n\n" + PROMPT.template
        )

        self.db_chain = SQLDatabaseChain.from_llm(
            llm, 
            self.db, 
            prompt=self.custom_prompt, 
            return_intermediate_steps=True,
            verbose=True
        )

    def ask_sql(self, query:str) -> str:
        response = self.db_chain.invoke(query, config={"callbacks": [self.callback_handler]})
        
        # print("Query:", query)
        # print("Response:", response)

        # Extração do resultado
        result = response.get("result", "")
        # intermediate = response.get("intermediate_steps", [])

        # Por algum motivo as vezes 'result' parece vir como uma lista de tuplas
        if isinstance(result, list):
            return "\n".join(str(r) for r in result)
        
        return str(result)