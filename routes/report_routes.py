from fastapi import APIRouter
import logging
from database.vehicle_db import VehicleDB
from database.customer_db import CustomerDB

router = APIRouter(prefix="/reports", tags=["Reports"])
vehicle_db = VehicleDB()
customer_db = CustomerDB()
logger = logging.getLogger("app_logger")

@router.get("/summary")
def get_summary():
    logger.info("API | GET /reports/summary called")
    summary_data = {
        "total vehicles": vehicle_db.count_total_vehicles(),
        "available vehicles": vehicle_db.count_available_vehicles(),
        "currently rented": vehicle_db.count_rented_vehicles(),
        "active customers": customer_db.count_active_customers()
    }
    logger.info("API | Summary report generated successfully")
    return summary_data

@router.get("/vehicles-by-category")
def get_vehicles_by_category():
    logger.info("API | GET /reports/vehicles-by-category called")
    return vehicle_db.get_vehicles_count_by_category()

@router.get("/top-customer")
def get_top_customer():
    logger.info("API | GET /reports/top-customer called")
    return customer_db.get_top_customer()