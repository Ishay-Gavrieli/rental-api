import logging
from fastapi import FastAPI
from database.db_connection import create_tables
from routes import vehicle_routes, customer_routes, report_routes


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-5s | %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log", encoding="utf-8"),
        logging.StreamHandler()])

logger = logging.getLogger(__name__)

app = FastAPI()

create_tables()

app.include_router(vehicle_routes.router,prefix="/vehicles", tags=["Vehicles"])
app.include_router(customer_routes.router)
app.include_router(report_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main.py:app", host="127.0.0.1", port=8000, reload=True)