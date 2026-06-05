import uvicorn

if __name__ == "__main__":
    print("Starting HackForge AI Backend Server...")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
