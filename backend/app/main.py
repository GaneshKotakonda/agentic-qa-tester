from fastapi import FastAPI

app = FastAPI(title="Agentic QA Tester");
@app.get("/health")
def health():
    return {"status":"OK"}

