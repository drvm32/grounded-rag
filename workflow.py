import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
import time
import json

load_dotenv()

def timed(func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    elapsed = time.time() - start
    return result, elapsed

CACHE_PATH = "cache.json"

def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def retrieve(query, k=6, persist_dir="chroma_db"):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory=persist_dir,
    )
    results = vectorstore.similarity_search(query, k=k)
    return results

def generate(query, chunks):
    context = "\n\n".join(chunk.page_content for chunk in chunks)

    prompt = f"""Answer the question using only the context below. If the context doesn't contain the answer, say so.

Context:
{context}

Question: {query}

Answer:"""

    llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest")
    response = llm.invoke(prompt)
    return response.text

def eval_relevance(query, chunks):
    llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest")

    numbered_chunks = "\n\n".join(
        f"Chunk {i+1}:\n{chunk.page_content}" for i, chunk in enumerate(chunks)
    )

    prompt = f"""For each numbered chunk below, decide whether it helps answer the question.
Reply with exactly {len(chunks)} lines, one per chunk, in the format:
Chunk 1: yes
Chunk 2: no
...and so on. No other text.

Question: {query}

{numbered_chunks}

Answer:"""

    response = llm.invoke(prompt)
    verdict_lines = response.text.strip().lower().splitlines()

    relevant = []
    irrelevant = []

    for i, chunk in enumerate(chunks):
        line = verdict_lines[i] if i < len(verdict_lines) else ""
        if "yes" in line:
            relevant.append(chunk)
        else:
            irrelevant.append(chunk)

    return relevant, irrelevant

def needs_web_search(relevant_chunks, irrelevant_chunks):
    return len(irrelevant_chunks) > 0

def web_search(query, max_results=3):
    llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest")
    rewrite_prompt = f"""Rewrite this question as a concise web search query. Reply with only the search query, nothing else.

Question: {query}

Search query:"""
    response = llm.invoke(rewrite_prompt)
    search_query = response.text.strip()

    search = TavilySearchResults(max_results=max_results)
    results = search.invoke(search_query)
    return results

def query_result(query):
    cache = load_cache()
    if query in cache:
        result = cache[query]
        result["cached"] = True
        return result

    timings = {}

    chunks, timings["retrieve"] = timed(retrieve, query)
    (relevant_chunks, irrelevant_chunks), timings["eval_relevance"] = timed(eval_relevance, query, chunks)

    web_results = []
    timings["web_search"] = 0
    if needs_web_search(relevant_chunks, irrelevant_chunks):
        web_results, timings["web_search"] = timed(web_search, query)

    if not relevant_chunks and not web_results:
        timings["total"] = sum(timings.values())
        result = {"answer": "I don't know based on available information.", "sources": [], "timings": timings, "cached": False}
        cache[query] = result
        save_cache(cache)
        return result

    sources = []
    context_parts = []

    for chunk in relevant_chunks:
        source = chunk.metadata.get("source", "unknown")
        sources.append(source)
        context_parts.append(f"[Source: {source}]\n{chunk.page_content}")

    for result in web_results:
        url = result.get("url", "unknown")
        sources.append(url)
        context_parts.append(f"[Source: {url}]\n{result.get('content', '')}")

    context = "\n\n".join(context_parts)

    prompt = f"""Answer the question using only the context below. Do not mention sources, citations, or file names in your answer, just answer the question in plain prose. The sources are tracked separately and shown to the user elsewhere.

Context:
{context}

Question: {query}

Answer:"""

    llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest")
    response, timings["generate"] = timed(llm.invoke, prompt)

    timings["total"] = sum(timings.values())
    result = {"answer": response.text, "sources": sources, "timings": timings, "cached": False}
    cache[query] = result
    save_cache(cache)
    return result

if __name__ == "__main__":
    query = "What is the maximum item size allowed in a DynamoDB table?"
    result = query_result(query)
    print(f"Question: {query}\n")
    print(f"Answer: {result['answer']}\n")
    print(f"Sources: {result['sources']}\n")
    print(f"Cached: {result['cached']}\n")
    print("Timings (seconds) [from original, uncached run]:")
    for stage, seconds in result["timings"].items():
        print(f"  {stage}: {seconds:.2f}")