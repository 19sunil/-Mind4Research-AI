import re
from agents import writer_chain, critic_chain
from tools import web_search, scrape_url


def extract_first_url(text):
    urls = re.findall(r'https?://\S+', text)
    return urls[0] if urls else None


def run_research_pipeline(topic):
    state = {}

    print("\n" + "=" * 50)
    print("Running Research Pipeline")
    print("=" * 50)

    # Step 1 Search
    state["search_results"] = web_search.invoke(topic)

    print("\nSearch Results:\n")
    print(state["search_results"])

    # Step 2 Scrape first URL
    url = extract_first_url(state["search_results"])

    if url:
        state["scraped_context"] = scrape_url.invoke(url)
    else:
        state["scraped_context"] = "No URL found."

    print("\n" + "=" * 50)
    print("Scraped Content")
    print("=" * 50)
    print(state["scraped_context"][:1500])

    # Step 3 Write Report
    research_combined = f"""
SEARCH RESULTS:
{state['search_results']}

SCRAPED CONTENT:
{state['scraped_context']}
"""

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\n" + "=" * 50)
    print("FINAL REPORT")
    print("=" * 50)
    print(state["report"])

    # Step 4 Critic
    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\n" + "=" * 50)
    print("CRITIC FEEDBACK")
    print("=" * 50)
    print(state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("Enter research topic: ")
    run_research_pipeline(topic)