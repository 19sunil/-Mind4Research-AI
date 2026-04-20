from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=2000,
    api_key=os.getenv("GROQ_API_KEY")
)

# Writer Chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer."),
    ("human", """
Write a detailed research report.

Topic: {topic}

Research:
{research}

Structure:
- Introduction
- Key Findings
- Conclusion
- Sources
""")
])

writer_chain = writer_prompt | llm | StrOutputParser()

# Critic Chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a strict and honest critic."),
    ("human", """
Review this report:

{report}

Return format:

Score: x/10

Strengths:
-

Areas to Improve:
-

Verdict:
-
""")
])

critic_chain = critic_prompt | llm | StrOutputParser()


# #For Testing Only
# if __name__ == "__main__":
#     topic = "Artificial Intelligence in Healthcare"
#     research = """
#     AI is improving diagnostics, medical imaging, drug discovery,
#     and patient monitoring through predictive analytics.
#     """

#     print("=== WRITER TEST ===")
#     report = writer_chain.invoke({
#         "topic": topic,
#         "research": research
#     })
#     print(report)

#     print("\n=== CRITIC TEST ===")
#     review = critic_chain.invoke({
#         "report": report
#     })
#     print(review)