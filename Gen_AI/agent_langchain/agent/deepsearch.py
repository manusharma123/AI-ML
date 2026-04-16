from langchain.tools import tool 
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os 
from dotenv import load_dotenv
from rich import print
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URLs, snippets, and scraped content."""
    results = tavily.search(query=query, max_results=5)

    out = []
    for r in results['results']:
        title = r['title']
        url = r['url']
        snippet = r['content']
        scraped_content = scrape_url(url, verify_ssl=False)

        out.append(
            f"Title: {title}\nURL: {url}\nSnippet: {snippet}\nScraped Content: {scraped_content}\n"
        )

    return "\n----\n".join(out)

def scrape_url(url: str, verify_ssl: bool = True) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"}, verify=verify_ssl)
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
    
# print(web_search.invoke("latest Noida protest report "))
# print(scrape_url("https://www.bbc.com/news/topics/cx2jyv8j8gwt", verify_ssl=False))