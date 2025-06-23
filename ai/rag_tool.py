# LangChain
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA


class RAGTool:
    def __init__(self, llm, path_chroma="./02. Databases/chroma_db", colletion="PetrobrasV2"):
        self.path_chroma = path_chroma

        embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma(persist_directory=path_chroma, embedding_function=embeddings, collection_name=colletion)

        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
        self.rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)