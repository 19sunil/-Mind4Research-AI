from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """Search the web for recent reliable information."""
    try:
        response = tavily.search(query=query, num_results=5)

        if not response.get("results"):
            return "No results found."

        out = []
        for result in response["results"]:
            out.append(
                f"Title: {result['title']}\n"
                f"URL: {result['url']}\n"
                f"Snippet: {result['content'][:300]}\n"
            )

        return "\n----\n".join(out)

    except Exception as e:
        return f"Search failed: {str(e)}"


@tool
def scrape_url(url: str) -> str:
    """Scrape readable text from a URL."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, timeout=8, headers=headers)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup([
            "script", "style", "header",
            "footer", "nav", "aside"
        ]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return text[:3000]

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"

# #For Testing Only
# print(web_search.invoke("Latest AI news"))
# print(scrape_url.invoke("https://www.hindustantimes.com/"))   