import os
from langchain_tavily import TavilySearch


class WebTool:
    def __init__(self):
        self.web_search_tool = TavilySearch(api_key=os.environ["TAVILY_API_KEY"])


    def tavily_search(self, query: str) -> str:
        result = self.web_search_tool.run(query)

        if isinstance(result, dict) and "results" in result:
            articles = result["results"]
            resumo = ""
            for artigo in articles[:3]:  # limite a 3 resultados
                resumo += f"- {artigo['title']}\n  {artigo['content']}\n  Link: {artigo['url']}\n\n"
            return resumo.strip()

        return str(result)
