from fastapi import FastAPI
import uvicorn
from database import db_connection

db_connection.create_tables()


app = FastAPI()
















if __name__=="__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)