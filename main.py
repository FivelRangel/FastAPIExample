from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"userId": 160893, "title": "Welcome to the Jungle from Local!", "id": 1, "completed": false}

