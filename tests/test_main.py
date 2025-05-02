from fastapi import FastAPI

# Create a simple test app instead of importing the main app
# This avoids all the database dependencies
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "OK"}