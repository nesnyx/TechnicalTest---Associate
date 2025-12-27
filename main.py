import uvicorn,os
from dotenv import load_dotenv
load_dotenv()

PORT=os.getenv("PORT")
if __name__ == "__main__":
    uvicorn.run("app:app",port=int(PORT),host="localhost",reload=True)