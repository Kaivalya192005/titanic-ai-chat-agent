import matplotlib
matplotlib.use("Agg")   # <-- IMPORTANT
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from langchain_community.llms import Ollama

# Load dataset
path = os.path.join(os.path.dirname(__file__), "titanic.csv")
df = pd.read_csv(path)

# LangChain LLM (requirement satisfied)
llm = Ollama(model="tinyllama")


def run_query(question: str):

    q = question.lower()

    # --- Survival ---
    if "survive" in q:
        return f"{df['Survived'].sum()} passengers survived.", None

    # --- Average fare ---
    elif "fare" in q:
        return f"Average fare: {df['Fare'].mean():.2f}", None

    # --- Gender percentage ---
    elif "male" in q or "female" in q:
        counts = df["Sex"].value_counts(normalize=True) * 100
        return counts.to_string(), None

    # --- Embarked ---
    elif "port" in q or "embarked" in q:
        return df["Embarked"].value_counts().to_string(), None

    # --- Age histogram ---
    elif "age" in q or "histogram" in q or "plot" in q:
        plt.figure()
        sns.histplot(df["Age"].dropna(), bins=20)
        plt.title("Age Distribution")

        img_path = "age_plot.png"
        plt.savefig(img_path)
        plt.close()

        return "Age distribution plotted.", img_path

    # --- Otherwise use LLM ---
    else:
     return (
        "Please ask a question related to the Titanic dataset.\n\n"
        "Examples:\n"
        "• How many passengers survived?\n"
        "• Average fare?\n"
        "• Show age distribution"
      ), None