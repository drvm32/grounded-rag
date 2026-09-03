# grounded-rag — Full Session Handoff Summary

## What the project is

A corrective-RAG chatbot answering questions about AWS documentation (S3, EC2, DynamoDB) for an SDE-1 job search portfolio. Named `grounded-rag` by the user at the very start. Built completely from scratch, incrementally, in a teach-by-typing style for the core logic.

## Settled decisions (never reopened)

- **AWS** over Azure — real hands-on AWS experience from an internship
- **Gemini** over DeepSeek — DeepSeek has no embeddings API; Gemini does both embeddings + chat
- **Tavily** over Linkup — native LangChain integration, official MCP server
- **Chroma** over Qdrant — runs as a local Python library, no server needed
- **Fixed corpus** over per-session upload — evaluation numbers only meaningful if corpus/questions stay constant
- **Corrective-RAG** over other project ideas — already compared extensively, final

## How we worked

For `workflow.py`'s core functions: I explained what a function needed to do and why, showed the real code, the user typed it themselves into the file, I confirmed correctness or pointed out fixes. For UI/tooling/eval scripts (not core RAG logic), I built directly after the user agreed that was fine.

## Results at a glance

All numbers are out of the same 18 answerable test questions (6 factual, 6 comparison, 6 operational) unless noted otherwise, manually graded.

| Stage | Config | Hit-rate |
|---|---|---|
| Step 6 — baseline (plain retrieve+generate) | chunk=1000, overlap=150, k=4 | 15/18 |
| Step 7 — chunk tuning | chunk=500, overlap=100, k=4 | 15/18 |
| Step 7 — chunk tuning (final) | chunk=500, overlap=100, **k=6** | **16/18** |
| Step 9 — full corrective pipeline (relevance grading + web fallback + citations) | chunk=500, overlap=100, k=6 | **17/18** |

Additional eval groups (Step 9):
- **Refusal group** (3 genuinely unanswerable questions — neither local corpus nor web search has an answer): **3/3 correct refusals**, no hallucination
- **Web fallback group** (6 questions, real AWS topics outside the local corpus): all correctly answered via Tavily web search with citations — not scored as pass/fail, used to confirm the fallback path works

**Net improvement across the whole project: 15/18 → 17/18**, plus a verified working refusal path and web-fallback path that didn't exist in the baseline.

**One documented regression, not hidden:** adding the corrective pipeline fixed 3 previously-failing questions but introduced 1 new failure (f6) — web search added contradictory noise to a question the local corpus already answered correctly and completely (conflated `BatchWriteItem`'s 25-item limit with a transaction's 100-item limit). This is called out explicitly in the README's limitations section rather than glossed over.

---

## Step 1 — Project setup
Created `data/`, `chroma_db/`, `requirements.txt` (langchain, langchain-community, langchain-google-genai, langchain-chroma, tavily-python, chromadb, streamlit, python-dotenv), `.env.example`, `.gitignore`. Created a Python venv and installed everything.

## Step 2 — `ingest.py`
Built incrementally: imports → `load_documents()` (DirectoryLoader + TextLoader, UTF-8) → `chunk_documents()` (RecursiveCharacterTextSplitter) → `embed_and_store()` (Gemini embeddings → Chroma) → `__main__` runner. Verified with a dummy file, then cleaned it up.

**Issue found & fixed:** Gemini free-tier embedding quota (100 units/minute) counts *each text in a batch*, not each HTTP call — one `Chroma.from_documents()` call with ~100 texts blew the quota instantly. Fixed by rewriting `embed_and_store()` to batch in groups of 50 with a 35s sleep between batches.

## Step 3 — Corpus (18 AWS doc files)
I could not scrape/reproduce copyrighted AWS doc text myself (copyright policy — limited to short quotes), so I gave the user a curated list of 18 real AWS doc URLs (6 each for S3/EC2/DynamoDB) and the user pasted the text into files under `data/S3/`, `data/EC2/`, `data/DynamoDB/`.

**Issue found & fixed:** `ingest.py`'s `DirectoryLoader(glob="*.txt")` doesn't recurse into subfolders, but the user organized files into subfolders. Fixed by changing glob to `"**/*.txt"`.

Verified via a full ingest run: 18 docs → 225 chunks (at chunk_size=1000) → embedded successfully.

## Step 4 — 24 test questions
Built `eval/test_questions.py` with 4 groups (6 each): factual, comparison, operational, unanswerable — later expanded to 5 groups (see Step 9). Facts were pulled directly from the actual corpus files I re-read to ensure accuracy.

## Step 5 — `workflow.py` v1 (baseline)
Built `retrieve()` (Chroma similarity_search) and `generate()` (plain prompt + Gemini).

**Issues found & fixed:**
- `gemini-2.5-flash` was deprecated/unavailable for new users → switched to `gemini-3.6-flash`, later to `gemini-flash-lite-latest` for quota reasons.
- `response.content` wasn't a plain string with the newer model (it returned a list of content blocks with thought signatures) → switched to `response.text`, which normalizes both formats.

## Step 6 — Baseline eval
Built `eval/run_baseline.py` to run the 18 answerable questions and write results to a markdown file for manual grading. Ran into repeated transient network errors (`WinError 10054`) — added retry logic (3 attempts, 15s backoff) to the runner.

**Grading:** I graded on the user's behalf (they explicitly asked me to, after I flagged this deviates from their original self-grading plan). Baseline: **15/18 correct**.

## Step 7 — Chunk tuning
Tried three configs, same 18 questions each time:
- chunk=1000, overlap=150, k=4 → 15/18
- chunk=500, overlap=100, k=4 → 15/18 (fixed one failure, broke a different one)
- chunk=500, overlap=100, **k=6** → **16/18** (final)

Kept all three result files (`results_baseline_chunk1000.md`, `_chunk500.md`, `_chunk500_k6.md`) for before/after comparison.

## Step 8 — Corrective logic
Extended `workflow.py` with:
- `eval_relevance()` — per-chunk yes/no LLM grading (later optimized, see below)
- `needs_web_search()` — triggers if even one chunk graded irrelevant (user explicitly chose to keep this aggressive rule after I flagged it would fire often)
- `web_search()` — query rewrite + Tavily search
- `query_result()` — combines relevant local chunks + web results, generates cited answer, or refuses if nothing usable

**Deprecation warning noted (not fixed):** `TavilySearchResults` from `langchain_community` is deprecated in favor of `langchain_tavily`, but left as-is since it still works.

Verified end-to-end: correct answer with both local file and web citations.

## Step 9 — Refusal + regression testing

**Major discovery:** My original 6 "unanswerable" test questions weren't actually unanswerable — they were real AWS topics just outside the local corpus, so `query_result()` correctly answered them via web search fallback. This wasn't a bug, it was correct behavior, but it meant the refusal path was never actually tested.

**Fix:** Relabeled those 6 as a `web_fallback` group (renamed `run_unanswerable.py` → `run_web_fallback.py`), and added 3 *genuinely* unanswerable questions (fictional AWS features, private account data) as a new `refusal` group with `run_refusal.py`. Verified the refusal code path directly with a mocked test (patched `web_search()` to return empty, asked an out-of-domain question) — confirmed it correctly returns "I don't know."

**Results:** Refusal: 3/3 correct. Regression (18 answerable questions through full corrective pipeline): **17/18** — up from 16/18. Fixed 3 previously-failing comparison questions (c2, c4, c6) via the web-search correction. Introduced 1 new failure (f6): web search added contradictory noise to a question the local corpus already answered correctly (mixed up `BatchWriteItem`'s 25-item limit with a transaction's 100-item limit). Documented as an honest, known tradeoff — not hidden.

One eval run hit a network failure on `o1`; re-ran it individually and got the correct answer, updated the results file.

## Step 10 — Latency/token tracking + caching
Added a `timed()` helper wrapping every stage of `query_result()`, returning a `timings` dict (retrieve, eval_relevance, web_search, generate, total). Added `cache.json`-based caching keyed by exact question string, with `load_cache()`/`save_cache()`.

**Bugs found & fixed during this step:** Two separate paste/placement mistakes where new code landed inside the wrong function body (once inside `timed()`, once merging refusal-return logic incorrectly with the final-return logic, referencing undefined variables). Both caught by re-reading the file and fixed directly.

**Real finding:** `eval_relevance()`'s 6 sequential LLM calls were the single biggest latency cost (~45-55% of total). Later optimized (see below) to 1 batched call.

**Rate limit discovery:** Gemini's free tier caps at ~15 requests/minute for the chat model. Heavy testing throughout the day repeatedly hit this, causing internal silent retries that inflated apparent latency (a single call could take 15-20s+ while rate-limited).

## Step 11 — `app.py` (Streamlit) + README
Built the Streamlit chat UI wrapping `query_result()`. Verified working in the browser via automated testing throughout.

**README** written covering: architecture, corrective-RAG explanation, stack, setup instructions, corpus description, eval methodology, the real before/after chunk-tuning table, the corrective-loop improvement numbers, refusal results, and an honest limitations section (web-search noise tradeoff, rate limits, caching being exact-match only, etc.)

---

## Post-completion fixes and UI iterations

### Citation duplication bug
Found: the generation prompt asked the model to cite sources *inline in the answer text*, while `app.py` *also* showed a separate deduplicated "Sources" expander — same info shown twice, messily. Fixed by changing the prompt to explicitly forbid inline citations, relying solely on the app's UI for source display. Also had to clear `cache.json` since it held stale pre-fix answers.

### Performance optimization
User asked directly why the app felt slow. Diagnosed: `eval_relevance()` made 6 sequential API calls (one per retrieved chunk). Rewrote it to grade all chunks in **one** LLM call (numbered list format, parsed by line), cutting that stage's calls 6x. Verified via CLI: dropped from ~18s to ~1s once rate limits cleared.

### App crash on network errors
Found via testing: an unhandled exception from `query_result()` would crash the whole Streamlit page with a raw traceback shown to the user. Fixed by wrapping the call in `query_result_with_retry()` (2 attempts, 3s pause) with a friendly error message on final failure.

### UI redesign journey (7 iterations, all user-directed)
1. **Glassmorphism v1** — dark theme, animated gradient, glass cards, shine sweep, source pills
2. **Neumorphism** — full rewrite to soft puffy monochrome UI; found and fixed a stray white background bar (Streamlit's `stBottom` container had hardcoded white bg) and a red default focus border bleeding through
3. **Glassmorphism v2 (light reflections)** — vivid saturated background, real cursor-reactive light using `st.components.v1.html()` (discovered `st.markdown`'s injected `<script>` tags don't execute — a real technical finding), refraction-style gradient borders
4. User called out that this wasn't *actually* Apple's Liquid Glass (fair pushback) — added genuine SVG `feTurbulence` + `feDisplacementMap` distortion filter for real pixel-level refraction, the closest browser-native technique to true optical glass
5. **Claymorphism** — full rewrite: light pastel background, puffy dual-shadow (light+dark) + inset highlight depth, chunky rounded shapes
6. **"Liquid clay" hybrid** — combined both; first attempt was too subtle (user: "no noticeable changes") since the background was too washed-out for blur to show; fixed with a much more vivid/saturated background, thicker refraction borders, and reintroduced the shine sweep
7. User then asked to dial back the light effects (cursor light, shine, glare) since they were washing out text even behind the mouse pointer — reduced all three to ~35-40% of their prior intensity, verified text stayed legible everywhere

### Sidebar chat history
Added multi-conversation support: `st.session_state.conversations` dict, a sidebar with "+ New chat" and a clickable list of past threads, auto-generated titles from each thread's first question.

**Bug found & fixed:** the sidebar renders *before* the chat-input handling code in the script, so the title update wasn't visible until the *next* rerun. Fixed by adding an explicit `st.rerun()` right after the answer is generated, so the sidebar redraws immediately with the correct title. Verified via direct DOM inspection (button text checks) since coordinate-based clicking was unreliable in the browser tool throughout this session (a recurring friction point — full-page `navigate` calls reset Streamlit session state each time, so verification had to be done via same-session JS clicks instead).

### Honest UI reassessment
User asked for my genuine opinion on the UI. I said honestly that 7 style iterations with vivid animated backgrounds, SVG distortion, and cursor-tracking JS was over-invested for a portfolio project meant to demonstrate RAG engineering rigor — it risked reading as a design demo rather than serious engineering work, undercutting the README's disciplined, honest-about-limitations tone.

### Final UI: calm + genuine glass + clay hybrid
Rebuilt from scratch, fully flat and professional first (white background, one indigo accent, simple U/AI avatars, no blur/animation at all). User then asked to add back **true liquid glass** (not flat) — added muted color-blob background, real `backdrop-filter: blur`, translucent cards, larger continuous corners, bright top-edge highlights — restrained, no rainbow, no motion, no cursor JS. Then user asked to **add claymorphism on top** — added the dual-shadow puffy depth (light+dark shadow pair + inset highlight) using muted slate-toned shadows to match the calm palette, applied to hero, bubbles, badges, pills, and input.

**Two regression bugs found and fixed in this final version** (leftover from earlier rewrites not carrying forward the old fixes):
- Stray red/pink Streamlit default focus border on the chat input — fixed by re-adding `[data-testid="stChatInput"] > div { border: none; background: transparent; }`
- White background strip behind the input bar (Streamlit's `stBottom` container) — fixed by re-adding the `stBottom` transparent-background override

Full chat flow re-verified end-to-end after these fixes: question → answer → sources → caption all correct; sidebar title updates immediately; new chat starts clean; switching between conversations preserves each history independently with no bleed.

### Port conflict fix
Dev server failed to start once — port 8501 was held by an orphaned `python.exe` process (PID) from an earlier manual run. Killed it via `taskkill`, confirmed Streamlit doesn't need that specific port (no OAuth/webhook dependency), restarted cleanly.

---

## Final project state

```
ingest.py              load → chunk → embed → store (chunk=500, overlap=100)
workflow.py             retrieve(k=6) → eval_relevance (1 batched call) → web_search (conditional) → query_result (cited, cached, timed)
app.py                  Streamlit UI — calm professional theme + genuine liquid glass + claymorphism hybrid, sidebar chat history
data/                   18 real AWS doc files (S3/EC2/DynamoDB)
eval/
  test_questions.py     24 questions: factual, comparison, operational, web_fallback, refusal
  run_baseline.py / run_refusal.py / run_web_fallback.py
  results_*.md           every eval run's raw output, kept for the record
cache.json              query cache (gitignored)
chroma_db/              vector store (gitignored)
README.md               architecture, real eval numbers, honest limitations
```

**Known, documented limitations:** web search can add noise even when local context is sufficient; Gemini free-tier rate limits cause real slowdowns under heavy use; caching is exact-string-match only; source citations show raw file paths.

The project is functionally complete against the original 11-step plan. Everything past that point was UI refinement driven by the user's follow-up requests.
