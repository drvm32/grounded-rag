import time
import html
import streamlit as st
from workflow import query_result

MAX_RETRIES = 2


def query_result_with_retry(question):
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return query_result(question), None
        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES:
                time.sleep(3)
    return None, last_error


st.set_page_config(page_title="grounded-rag", page_icon="📦", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #ffffff;
    --surface: #f8f9fb;
    --border: #e5e7eb;
    --text-main: #1f2937;
    --text-dim: #6b7280;
    --accent: #4f46e5;
    --accent-bg: #eef2ff;
    --glass-bg: rgba(255, 255, 255, 0.5);
    --glass-border: rgba(255, 255, 255, 0.9);
    --clay-light: rgba(255, 255, 255, 0.85);
    --clay-shadow: rgba(100, 110, 150, 0.22);
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background:
        radial-gradient(circle at 12% 8%, rgba(99, 102, 241, 0.22), transparent 38%),
        radial-gradient(circle at 88% 12%, rgba(56, 189, 248, 0.18), transparent 40%),
        radial-gradient(circle at 75% 90%, rgba(16, 185, 129, 0.16), transparent 42%),
        radial-gradient(circle at 15% 85%, rgba(244, 114, 182, 0.14), transparent 42%),
        linear-gradient(160deg, #f4f5f9 0%, #eef1f8 100%);
}

.glass {
    position: relative;
    background: var(--glass-bg);
    backdrop-filter: blur(24px) saturate(180%);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.5);
    border-top-color: rgba(255, 255, 255, 0.95);
    box-shadow:
        7px 7px 16px var(--clay-shadow),
        -7px -7px 16px var(--clay-light),
        inset 1px 1px 2px rgba(255, 255, 255, 0.6),
        inset -2px -2px 5px rgba(100, 110, 150, 0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.glass:hover {
    transform: translateY(-2px);
    box-shadow:
        9px 9px 20px var(--clay-shadow),
        -9px -9px 20px var(--clay-light),
        inset 1px 1px 2px rgba(255, 255, 255, 0.6),
        inset -2px -2px 5px rgba(100, 110, 150, 0.08);
}

.hero {
    text-align: center;
    padding: 2rem 1.5rem;
    margin: 1rem 0 1.5rem 0;
    border-radius: 24px;
}

.hero h1 {
    font-size: 1.9rem;
    font-weight: 700;
    margin: 0;
    color: var(--text-main);
    letter-spacing: -0.01em;
}

.hero p {
    color: var(--text-dim);
    font-size: 0.92rem;
    max-width: 540px;
    margin: 0.6rem auto 0 auto;
    line-height: 1.55;
}

.badge-row {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    margin-top: 1.1rem;
    flex-wrap: wrap;
}

.badge-chip {
    font-size: 0.75rem;
    font-weight: 500;
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    color: var(--accent);
    background: rgba(238, 242, 255, 0.65);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(224, 231, 255, 0.9);
    box-shadow:
        3px 3px 8px var(--clay-shadow),
        -3px -3px 8px var(--clay-light),
        inset 1px 1px 1px rgba(255, 255, 255, 0.5);
}

.chat-row { display: flex; margin: 1rem 0; align-items: flex-start; }
.chat-row.user { justify-content: flex-end; }
.chat-row.assistant { justify-content: flex-start; }

.avatar {
    width: 32px; height: 32px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem; font-weight: 600; flex-shrink: 0;
    color: white;
}
.avatar.user { background: var(--accent); margin-left: 0.6rem; order: 2; }
.avatar.assistant { background: #6b7280; margin-right: 0.6rem; }

.bubble {
    max-width: 76%;
    padding: 0.85rem 1.1rem;
    border-radius: 20px;
    line-height: 1.55;
    font-size: 0.94rem;
    color: var(--text-main);
    backdrop-filter: blur(22px) saturate(180%);
    -webkit-backdrop-filter: blur(22px) saturate(180%);
    box-shadow:
        6px 6px 14px var(--clay-shadow),
        -6px -6px 14px var(--clay-light),
        inset 1px 1px 2px rgba(255, 255, 255, 0.6),
        inset -2px -2px 5px rgba(100, 110, 150, 0.08);
}

.bubble.user { order: 1; background: rgba(224, 231, 255, 0.55); border: 1px solid rgba(255, 255, 255, 0.7); }
.bubble.assistant { background: rgba(255, 255, 255, 0.5); border: 1px solid rgba(255, 255, 255, 0.85); }

.meta-caption {
    font-size: 0.75rem;
    color: var(--text-dim);
    margin-top: 0.4rem;
    margin-left: 2.6rem;
    display: flex;
    align-items: center;
    gap: 0.3rem;
}

.sources-wrap {
    margin: 0.5rem 0 0.1rem 2.6rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
}

.source-pill {
    font-size: 0.72rem;
    padding: 0.35rem 0.7rem;
    border-radius: 10px;
    color: var(--text-dim);
    background: rgba(255, 255, 255, 0.5);
    backdrop-filter: blur(16px) saturate(160%);
    -webkit-backdrop-filter: blur(16px) saturate(160%);
    border: 1px solid rgba(255, 255, 255, 0.8);
    font-family: ui-monospace, 'SFMono-Regular', Consolas, monospace;
    max-width: 100%;
    overflow-wrap: anywhere;
    word-break: break-all;
    box-shadow:
        3px 3px 7px var(--clay-shadow),
        -3px -3px 7px var(--clay-light),
        inset 1px 1px 1px rgba(255, 255, 255, 0.5);
}

[data-testid="stChatInput"] {
    border-radius: 20px !important;
    background: rgba(255, 255, 255, 0.55) !important;
    backdrop-filter: blur(24px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
    border: 1px solid rgba(255, 255, 255, 0.85) !important;
    box-shadow:
        6px 6px 16px var(--clay-shadow),
        -6px -6px 16px var(--clay-light),
        inset 1px 1px 2px rgba(255, 255, 255, 0.6),
        inset -2px -2px 5px rgba(100, 110, 150, 0.08) !important;
}

[data-testid="stChatInput"] textarea {
    color: var(--text-main) !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-dim) !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"]:focus-within {
    outline: none !important;
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}

[data-testid="stChatInput"] > div {
    border: none !important;
    background: transparent !important;
}

[data-testid="stChatInputSubmitButton"] {
    background: var(--accent) !important;
    border-radius: 8px !important;
}

div[data-testid="stBottom"],
div[data-testid="stBottom"] div[class],
html body div[data-testid="stBottom"] > div,
html body div[data-testid="stBottom"] div {
    background: transparent !important;
    background-color: transparent !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero glass">
    <h1>📦 grounded-rag</h1>
    <p>A corrective-RAG chatbot over AWS documentation (S3 · EC2 · DynamoDB). It grades its own retrieval, falls back to live web search when local context falls short, and admits when it genuinely doesn't know.</p>
    <div class="badge-row">
        <span class="badge-chip">self-grading retrieval</span>
        <span class="badge-chip">live web fallback</span>
        <span class="badge-chip">cited sources</span>
        <span class="badge-chip">honest refusal</span>
    </div>
</div>
""", unsafe_allow_html=True)

if "conversations" not in st.session_state:
    first_id = "1"
    st.session_state.conversations = {first_id: {"title": "New chat", "messages": []}}
    st.session_state.active_conversation_id = first_id
    st.session_state.next_conversation_id = 2

active_id = st.session_state.active_conversation_id
active_conversation = st.session_state.conversations[active_id]

with st.sidebar:
    st.markdown("### Chats")

    if st.button("+ New chat", use_container_width=True):
        new_id = str(st.session_state.next_conversation_id)
        st.session_state.next_conversation_id += 1
        st.session_state.conversations[new_id] = {"title": "New chat", "messages": []}
        st.session_state.active_conversation_id = new_id
        st.rerun()

    st.markdown("---")

    for conv_id in reversed(list(st.session_state.conversations.keys())):
        conv = st.session_state.conversations[conv_id]
        label = conv["title"]
        is_active = conv_id == active_id
        if st.button(("● " if is_active else "") + label, key=f"conv_{conv_id}", use_container_width=True):
            st.session_state.active_conversation_id = conv_id
            st.rerun()


def render_message(role, content, sources=None, caption=None):
    avatar = "U" if role == "user" else "AI"
    safe_content = html.escape(content).replace("\n", "<br>")
    st.markdown(f"""
    <div class="chat-row {role}">
        <div class="avatar {role}">{avatar}</div>
        <div class="bubble {role}">{safe_content}</div>
    </div>
    """, unsafe_allow_html=True)

    if role == "assistant" and sources:
        pills = "".join(f'<span class="source-pill">{html.escape(s)}</span>' for s in sorted(set(sources)))
        st.markdown(f'<div class="sources-wrap">{pills}</div>', unsafe_allow_html=True)

    if role == "assistant" and caption:
        st.markdown(f'<div class="meta-caption">{caption}</div>', unsafe_allow_html=True)


for message in active_conversation["messages"]:
    render_message(
        message["role"],
        message["content"],
        sources=message.get("sources"),
        caption=message.get("caption"),
    )

if question := st.chat_input("Ask about S3, EC2, or DynamoDB..."):
    active_conversation["messages"].append({"role": "user", "content": question})
    if active_conversation["title"] == "New chat":
        active_conversation["title"] = (question[:40] + "…") if len(question) > 40 else question
    render_message("user", question)

    with st.spinner("Retrieving, grading relevance, and generating an answer..."):
        result, error = query_result_with_retry(question)

    if error is not None:
        answer_text = "Something went wrong reaching the AI service. Please try asking again."
        sources = []
        caption = "error"
    else:
        answer_text = result["answer"]
        sources = result["sources"]
        caption = "served from cache" if result["cached"] else f"{result['timings']['total']:.1f}s"

    render_message("assistant", answer_text, sources=sources, caption=caption)

    active_conversation["messages"].append({
        "role": "assistant",
        "content": answer_text,
        "sources": sources,
        "caption": caption,
    })

    st.rerun()
