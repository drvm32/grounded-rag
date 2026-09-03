# grounded-rag

A corrective-RAG chatbot that answers questions about AWS documentation (S3, EC2, DynamoDB). It's built to know when not to trust its own retrieval.

Built as a portfolio project for an SDE-1 job search. Everything here (the corpus, the eval questions, the tuning numbers, the failure modes) is real and reproducible, not staged.

## What makes it "corrective"

Plain RAG retrieves chunks and generates an answer, trusting retrieval blindly. This system doesn't:

1. **Retrieve** the top-k chunks from a local vector store (Chroma)
2. **Grade** each chunk's relevance with an LLM call. Is this chunk actually useful for answering the question, or just semantically nearby?
3. **Correct**: if even one chunk is graded irrelevant, fall back to a live web search (Tavily) to fill the gap
4. **Generate** one answer from whatever's left (relevant local chunks plus web results), with every source cited
5. **Refuse**: if neither local retrieval nor web search turns up anything usable, say "I don't know" instead of guessing

## Architecture

```
ingest.py    load AWS doc .txt files -> chunk -> embed (Gemini) -> store in Chroma
workflow.py  retrieve() -> eval_relevance() -> web_search() (conditional) -> query_result()
app.py       Streamlit chat UI, wraps query_result() with history and caching display
```

Three files, built incrementally. `workflow.py` started as a minimal retrieve+generate pipeline and was extended in place with relevance grading, web fallback, citations, refusal, latency tracking, and caching.

## Stack

- **LLM & embeddings**: Google Gemini (`gemini-flash-lite-latest` for chat, `gemini-embedding-001` for embeddings), chosen over DeepSeek because DeepSeek's API has no embeddings support
- **Vector store**: Chroma, running as a local Python library so there's no server to manage
- **Web search**: Tavily, via its native LangChain integration
- **Framework**: LangChain
- **UI**: Streamlit

## Setup

```bash
python -m venv venv
./venv/Scripts/pip install -r requirements.txt   # Windows; use venv/bin/pip on macOS/Linux
cp .env.example .env
# fill in GOOGLE_API_KEY (Google AI Studio) and TAVILY_API_KEY (Tavily free tier)
```

Ingest the corpus (only needs to run once, or after changing `data/` or the chunk settings):

```bash
./venv/Scripts/python ingest.py
```

Run the app:

```bash
./venv/Scripts/streamlit run app.py
```

## The corpus

18 real AWS documentation pages, hand-picked across three services:

- **S3** (6 pages): storage classes, versioning, lifecycle rules, transitions
- **EC2** (6 pages): instance types, launch parameters, security groups
- **DynamoDB** (6 pages): quotas, constraints, partition key design, read/write operations

It's a fixed corpus by design. An evaluation number is only meaningful if the corpus and test questions stay constant across every measurement.

## Evaluation

24 test questions across four groups, each with a hand-written expected answer:

- **Factual** (6): precise numeric limits (e.g. "max item size in DynamoDB?")
- **Comparison** (6): tradeoffs between two options (e.g. "S3 Standard-IA vs One Zone-IA?")
- **Operational** (6): practical how-do-I scenarios
- **Refusal** (3): genuinely unanswerable by either the local corpus or the open web (fictional AWS features, private account data)
- **Web fallback** (6, not scored): real AWS topics outside the local corpus, used to test the web-search correction path specifically

Grading was manual. I read each system answer against the expected answer and marked it correct or incorrect myself, not automated exact-match and not an LLM-as-judge. Every eval run's raw output is kept in `eval/results_*.md` for inspection.

### Chunk tuning (before/after)

Same 18 answerable questions, same `workflow.py` logic, varying only chunk size/overlap and retrieval `k`:

| Config | Hit-rate |
|---|---|
| chunk=1000, overlap=150, k=4 (initial baseline) | 15/18 |
| chunk=500, overlap=100, k=4 | 15/18 |
| chunk=500, overlap=100, k=6 (**final**) | 16/18 |

Smaller chunks fixed one failure (a specific numeric limit that had been buried inside a larger chunk) but introduced a different one (a comparison question that needed two related facts from separate chunks). Bumping `k` from 4 to 6 fixed that without another re-chunk, by giving the relevance-grading step more candidates to pull from.

### Adding the corrective loop (relevance grading, web search, citations)

Same 18 questions, now through the full `query_result()` pipeline instead of plain retrieve+generate:

**17/18 correct**, up from 16/18. The corrective mechanism fixed 3 previously-failing comparison questions by pulling in web search when local chunks were graded insufficient. It also introduced one new failure: a question the local corpus already answered correctly got contradictory noise added from web search results (a `BatchWriteItem` limit got conflated with a `TransactWriteItems` limit). That's a real, documented tradeoff of the "even one irrelevant chunk triggers web search" policy, and I'm not hiding it.

### Refusal path

3 questions designed to be unanswerable by both local retrieval and live web search (a fictional AWS storage tier, private account-specific data). Result: **3/3 correctly refused**, no hallucinated details in any case.

## Known limitations

- **Web search can add noise even when local context is already sufficient.** The rule is "even one irrelevant chunk triggers web search," which is more cautious than necessary once `k` gets above 2-3. Most queries end up triggering a web search regardless of whether they need one.
- **Free-tier rate limits are real.** Gemini's free tier caps at roughly 15 requests per minute for the chat model. A single query makes about 8 calls (embedding, up to k relevance checks, an optional query rewrite, and generation), so heavy testing sessions routinely hit the limit and see multi-second internal retry delays.
- **Relevance grading is the single biggest latency cost.** It used to be 6 sequential LLM calls; it's now batched into 1 call per query (grading all retrieved chunks together), which cut that stage's cost roughly 6x.
- **Caching is exact-match only.** `cache.json` keys on the literal question string, so rephrasing a question doesn't hit the cache even if it means the same thing.
- **Source citations show local file paths as-is** (e.g. `data\DynamoDB\dynamodb_constraints.txt`), not cleaned-up display names.

## Project structure

```
ingest.py              load -> chunk -> embed -> store
workflow.py             retrieve, eval_relevance, web_search, query_result (the actual pipeline)
app.py                  Streamlit UI
data/                   18 AWS doc .txt files (S3/EC2/DynamoDB)
eval/
  test_questions.py     24 questions with expected answers, in 5 groups
  run_baseline.py        runs the answerable groups
  run_refusal.py          runs the refusal group
  run_web_fallback.py     runs the web-fallback group
  results_*.md            raw output from every eval run, kept for before/after comparison
cache.json              query cache (gitignored)
chroma_db/              vector store (gitignored, rebuild with ingest.py)
```
