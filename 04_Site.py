from dotenv import load_dotenv

import streamlit as st
from datetime import date
import asyncio

from utils import load_news, format_news_html
from ai.orchestrator_agent import OrchestratorAgent

# Set the path as environment variable
load_dotenv()

# Instância da classe do agente orquestrador
orchestrator = OrchestratorAgent(model_="gpt-4o-mini")


# Criação do APP com Streamlit
st.set_page_config(page_title="News + Chat", layout="wide")
st.title("🗞️ Market News with AI Chat")

col1, col2 = st.columns([1.5, 1])

# Load and display news
df_news = load_news()
df_news = df_news.loc[(df_news["relevancia"]=="Relevante") & (df_news["impacto"].isin(["Positivo", "Negativo"]))]

with col1:
    st.subheader("Notícias mais recentes:")
    news_html = format_news_html(df_news)
    st.markdown(news_html, unsafe_allow_html=True)

# Chat interface
with col2:
    st.subheader("Converse com um agente 🤖")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Me pergunte sobre as notícias da Petrobrás")
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        prompt = f"""Para seu contexto, hoje é {date.today().isoformat()}.
        
        Responda a seguinte pergunta:
        {prompt}"""
        print("USER PROMPT:\n" + prompt)
        response = asyncio.run(orchestrator.ask_ai(prompt))
        st.chat_message("assistant").markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
