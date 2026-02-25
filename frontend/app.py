import streamlit as st
import requests

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Titanic AI Agent",
    page_icon="🚢",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/chat"

# ================= HEADER =================
st.title("🚢 Titanic Dataset AI Agent")
st.caption("Ask questions • Get insights • Generate visualizations")

# ================= SIDEBAR =================
with st.sidebar:

    st.header("Controls")

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("Try these")

    if st.button("How many passengers survived?"):
        st.session_state.prefill = "How many passengers survived?"

    if st.button("Average fare?"):
        st.session_state.prefill = "Average fare?"

    if st.button("Show age distribution"):
        st.session_state.prefill = "Show age distribution"

# ================= SESSION STATE =================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "prefill" not in st.session_state:
    st.session_state.prefill = ""

# ================= CHAT DISPLAY =================
for msg in st.session_state.messages:

    role = msg["role"]
    content = msg["content"]

    with st.chat_message(role):

        if isinstance(content, dict):
            st.write(content["text"])

            if content.get("image"):
                st.image(content["image"], use_container_width=True)
        else:
            st.write(content)

# ================= CHAT INPUT =================
prompt = st.chat_input("Ask anything about Titanic dataset...")

# Auto-fill from sidebar suggestions
if st.session_state.prefill:
    prompt = st.session_state.prefill
    st.session_state.prefill = ""

# ================= HANDLE INPUT =================
if prompt:

    # USER MESSAGE
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    try:
        res = requests.get(API_URL, params={"question": prompt})
        data = res.json()

        answer = data.get("answer", "")
        image = data.get("image")

        st.session_state.messages.append({
            "role": "assistant",
            "content": {
                "text": answer,
                "image": image
            }
        })

    except Exception as e:
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Error: {e}"
        })

    st.rerun()