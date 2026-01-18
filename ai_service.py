import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
    model="meta-llama/llama-3-8b-instruct",
    temperature=0.7
)

def summarize_book_details(title: str, author: str) -> str:
    """Summarizes a book based on known title/author knowledge."""
    template = "Provide a concise summary (max 3 sentences) of the book '{title}' by {author}."
    prompt = PromptTemplate(template=template, input_variables=["title", "author"])
    chain = prompt | llm | StrOutputParser()
    try:
        return chain.invoke({"title": title, "author": author})
    except Exception:
        return "Summary generation unavailable."

def summarize_text(content: str) -> str:
    """Summarizes raw text content provided by the user."""
    template = "Summarize the following book content in a concise paragraph:\n\n{content}"
    prompt = PromptTemplate(template=template, input_variables=["content"])
    chain = prompt | llm | StrOutputParser()
    try:
        return chain.invoke({"content": content})
    except Exception:
        return    "Summary generation unavailable."

def recommend_books(preferences: str) -> str:
    template = "Suggest 3 books for a user who likes: {preferences}. Return a simple list."
    prompt = PromptTemplate(template=template, input_variables=["preferences"])
    chain = prompt | llm | StrOutputParser()
    try:
        return chain.invoke({"preferences": preferences})
    except Exception:
        return "Recommendations unavailable."