from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"greeting": "Hello, Bitches!", "message": "Welcome to the Jungle from Local!"}
