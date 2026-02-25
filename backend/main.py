from fastapi import FastAPI
from backend.agent import run_query

app = FastAPI()

@app.get("/chat")
def chat(question: str):
    try:
        answer, image = run_query(question)

        response = {"answer": str(answer)}

        if image:
            response["image"] = image

        return response

    except Exception as e:
        return {"answer": f"Error: {str(e)}"}