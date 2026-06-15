from fastapi import APIRouter, HTTPException
import logging
from database.customer_db import CustomerDB

router = APIRouter(prefix="/customers", tags=["Customers"])
customer_db = CustomerDB()
logger = logging.getLogger("app_logger")

@router.post("")
def create_customer(data: dict):
    logger.info("API | POST /customers called")
    if "name" not in data or "license_number" not in data:
        logger.error("API | Missing fields in payload")
        raise HTTPException(status_code=400, detail="Missing fields")
        
    try:
        logger.info("SQL | Inserting new customer")
        customer_db.create_customer(data)
        logger.info("API | Customer created successfully")
        return {"message": "Customer created successfully"}
    except ValueError as e:
        logger.error(f"API | Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("")
def get_customers():
    logger.info("API | GET /customers called")
    return customer_db.get_all_customers()

@router.get("/{id}")
def get_customer(id: int):
    logger.info(f"API | GET /customers/{id} called")
    customer = customer_db.get_customer_by_id(id)
    if not customer:
        logger.error(f"API | Customer not found: {id}")
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.patch("/{id}")
def update_customer(id: int, data: dict):
    logger.info(f"API | PATCH /customers/{id} called")
    customer = customer_db.get_customer_by_id(id)
    if not customer:
        logger.error(f"API | Customer not found: {id}")
        raise HTTPException(status_code=404, detail="Customer not found")
        
    try:
        logger.info(f"SQL | Updating customer {id}")
        customer_db.update_customer(id, data)
        logger.info(f"API | Customer {id} updated successfully")
        return {"message": "Customer updated successfully"}
    except ValueError as e:
        logger.error(f"API | Validation error on update: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{id}/deactivate")
def deactivate_customer(id: int):
    logger.info(f"API | PATCH /customers/{id}/deactivate called")
    customer = customer_db.get_customer_by_id(id)
    if not customer:
        logger.error(f"API | Customer not found: {id}")
        raise HTTPException(status_code=404, detail="Customer not found")
        
    logger.info(f"SQL | Deactivating customer {id}")
    customer_db.set_customer_status(id, False)
    logger.info(f"API | Customer {id} deactivated")
    return {"message": "Customer deactivated successfully"}

@router.patch("/{id}/activate")
def activate_customer(id: int):
    logger.info(f"API | PATCH /customers/{id}/activate called")
    customer = customer_db.get_customer_by_id(id)
    if not customer:
        logger.error(f"API | Customer not found: {id}")
        raise HTTPException(status_code=404, detail="Customer not found")
        
    logger.info(f"SQL | Activating customer {id}")
    customer_db.set_customer_status(id, True)
    logger.info(f"API | Customer {id} activated")
    return {"message": "Customer activated successfully"}