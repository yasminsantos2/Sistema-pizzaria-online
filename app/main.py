from fastapi import FastAPI

app = FastAPI(title="Sistema Pizzaria Online")


@app.get("/")
def root():
    return {"message": "API da pizzaria online"}
