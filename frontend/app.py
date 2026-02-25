import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- Load dataset ----------
df = pd.read_csv("backend/titanic.csv")

# ---------- Page ----------
st.set_page_config(page_title="Titanic AI Agent", layout="wide")

st.title("🚢 Titanic Dataset AI Agent")
st.caption("Ask questions • Get insights • Generate visualizations")

# ---------- Sidebar ----------
with st.sidebar:
    st.header("Controls")
    if st.button("Clear Chat"):
        st.session_state.messages = []

    st.subheader("Try these")
    q1 = st.button("How many passengers survived?")
    q2 = st.button("Average fare?")
    q3 = st.button("Show age distribution")

# ---------- Chat history ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Handle predefined buttons ----------
user_query = None

if q1:
    user_query = "survived"

if q2:
    user_query = "average fare"

if q3:
    user_query = "age distribution"

# ---------- Chat input ----------
user_input = st.chat_input("Ask anything about Titanic dataset...")

if user_input:
    user_query = user_input.lower()

# ---------- Process query ----------
if user_query:

    # Show user message
    st.session_state.messages.append(("user", user_query))

    response = ""
    show_plot = False

    if "surviv" in user_query:
        survivors = df["Survived"].sum()
        response = f"🟢 {survivors} passengers survived."

    elif "fare" in user_query:
        avg_fare = df["Fare"].mean()
        response = f"💰 Average fare: {avg_fare:.2f}"

    elif "age" in user_query:
        response = "📊 Age distribution:"
        show_plot = True

    else:
        response = "❌ I didn't understand. Try asking about survival, fare, or age."

    st.session_state.messages.append(("assistant", response))

    if show_plot:
        fig, ax = plt.subplots()
        sns.histplot(df["Age"].dropna(), bins=30, ax=ax)
        ax.set_title("Age Distribution")
        st.session_state.messages.append(("plot", fig))

# ---------- Display chat ----------
for role, msg in st.session_state.messages:

    if role == "user":
        st.chat_message("user").write(msg)

    elif role == "assistant":
        st.chat_message("assistant").write(msg)

    elif role == "plot":
        st.pyplot(msg)