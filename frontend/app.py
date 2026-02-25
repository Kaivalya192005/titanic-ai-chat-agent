import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Titanic AI Agent", layout="wide")

# ---------- LOAD DATA ----------
df = pd.read_csv("backend/titanic.csv")

# ---------- TITLE ----------
st.title("🚢 Titanic Dataset AI Agent")
st.caption("Ask questions • Get insights • Generate visualizations")

# ---------- SESSION ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("Controls")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.subheader("Try these")

    if st.button("How many passengers survived?"):
        st.session_state.messages.append({"role":"user","content":"How many passengers survived?"})

    if st.button("Average fare?"):
        st.session_state.messages.append({"role":"user","content":"Average fare?"})

    if st.button("Show age distribution"):
        st.session_state.messages.append({"role":"user","content":"Show age distribution"})

# ---------- DISPLAY CHAT ----------
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        if isinstance(msg["content"], dict):
            st.write(msg["content"]["text"])
            if msg["content"].get("image"):
                st.pyplot(msg["content"]["image"])
        else:
            st.write(msg["content"])

# ---------- INPUT ----------
prompt = st.chat_input("Ask anything about Titanic dataset...")

if prompt:

    st.session_state.messages.append({"role":"user","content":prompt})

    answer = ""
    image = None

    # ---------- SIMPLE INTELLIGENCE ----------
    q = prompt.lower()

    if "survive" in q:
        count = df["Survived"].sum()
        answer = f"{count} passengers survived."

    elif "fare" in q:
        avg = df["Fare"].mean()
        answer = f"Average fare: {avg:.2f}"

    elif "age" in q or "distribution" in q:
        fig, ax = plt.subplots()
        sns.histplot(df["Age"].dropna(), bins=20, ax=ax)
        ax.set_title("Age Distribution")
        image = fig
        answer = "Age distribution plotted."

    else:
        answer = "I can answer questions about survival, fare, and age distribution."

    st.session_state.messages.append({
        "role":"assistant",
        "content":{"text":answer, "image":image}
    })

    st.rerun()