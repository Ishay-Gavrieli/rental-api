from fastapi import APIRouter, HTTPException
import logging
from database.vehicle_db import VehicleDB
from database.customer_db import CustomerDB

router = APIRouter()


vehicle_db = VehicleDB()
customer_db = CustomerDB()

logger = logging.getLogger(__name__)

VALID_CATEGORIES = {"sedan", "suv", "truck", "electric", "luxury"}

@router.post("")
def create_vehicle(data: dict):
    logger.info("API | POST /vehicles called")
    if "title" not in data or "brand" not in data or "category" not in data:
        logger.error("API | Missing fields in request payload")
        raise HTTPException(status_code=400, detail="Missing required fields")
        
    if data["category"].lower() not in VALID_CATEGORIES:
        logger.error(f"API | Invalid category requested: {data['category']}")
        raise HTTPException(status_code=400, detail="Invalid category")
        
    logger.info("SQL | Executing vehicle insert")
    vehicle_db.create_vehicle(data)
    logger.info("API | Vehicle created successfully")
    return {"message": "Vehicle created successfully"}

@router.get("")
def get_vehicles():
    logger.info("API | GET /vehicles called")
    return vehicle_db.get_all_vehicles()

@router.get("/{id}")
def get_vehicle(id: int):
    logger.info(f"API | GET /vehicles/{id} called")
    vehicle = vehicle_db.get_vehicle_by_id(id)
    if not vehicle:
        logger.error(f"API | Vehicle not found: {id}")
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@router.patch("/{id}")
def update_vehicle(id: int, data: dict):
    logger.info(f"API | PATCH /vehicles/{id} called")
    vehicle = vehicle_db.get_vehicle_by_id(id)
    if not vehicle:
        logger.error(f"API | Vehicle not found: {id}")
        raise HTTPException(status_code=404, detail="Vehicle not found")
        
    if "category" in data and data["category"].lower() not in VALID_CATEGORIES:
        logger.error(f"API | Invalid category for update: {data['category']}")
        raise HTTPException(status_code=400, detail="Invalid category")
        
    logger.info(f"SQL | Updating vehicle {id}")
    vehicle_db.update_vehicle(id, data)
    logger.info(f"API | Vehicle {id} updated successfully")
    return {"message": "Vehicle updated successfully"}

@router.patch("/{id}/rent/{customer_id}")
def rent_vehicle(id: int, customer_id: int):
    logger.info(f"API | PATCH /vehicles/{id}/rent/{customer_id} called")
    
    vehicle = vehicle_db.get_vehicle_by_id(id)
    if not vehicle:
        logger.error(f"API | Vehicle not found: {id}")
        raise HTTPException(status_code=404, detail="Vehicle not found")
        
    customer = customer_db.get_customer_by_id(customer_id)
    if not customer:
        logger.error(f"API | Customer not found: {customer_id}")
        raise HTTPException(status_code=404, detail="Customer not found")
        
    if not vehicle["is_available"]:
        logger.error(f"API | Vehicle {id} is already rented")
        raise HTTPException(status_code=400, detail="Vehicle is not available")
        
    if not customer["is_active"]:
        logger.error(f"API | Customer {customer_id} is inactive")
        raise HTTPException(status_code=400, detail="Customer is not active")
        
    active_rentals = vehicle_db.count_active_rentals_by_customer(customer_id)
    if active_rentals >= 2:
        logger.error(f"API | Customer {customer_id} reached maximum rentals (2)")
        raise HTTPException(status_code=400, detail="Customer has reached maximum rentals")
        
    logger.info(f"SQL | Executing rent process for vehicle {id} to customer {customer_id}")
    vehicle_db.set_rented(id, customer_id)
    customer_db.increment_rentals(customer_id)
    
    logger.info(f"API | Vehicle {id} successfully rented by customer {customer_id}")
    return {"message": "Vehicle rented successfully"}

@router.patch("/{id}/return/{customer_id}")
def return_vehicle(id: int, customer_id: int):
    logger.info(f"API | PATCH /vehicles/{id}/return/{customer_id} called")
    
    vehicle = vehicle_db.get_vehicle_by_id(id)
    if not vehicle:
        logger.error(f"API | Vehicle not found: {id}")
        raise HTTPException(status_code=404, detail="Vehicle not found")
        
    customer = customer_db.get_customer_by_id(customer_id)
    if not customer:
        logger.error(f"API | Customer not found: {customer_id}")
        raise HTTPException(status_code=404, detail="Customer not found")
        
    if vehicle["is_available"]:
        logger.error(f"API | Vehicle {id} is already available, cannot return")
        raise HTTPException(status_code=400, detail="Vehicle is not currently rented")
        
    if vehicle["rented_by_customer_id"] != customer_id:
        logger.error(f"API | Vehicle {id} was not rented by customer {customer_id}")
        raise HTTPException(status_code=400, detail="Vehicle is not rented by this customer")
        
    logger.info(f"SQL | Returning vehicle {id}")
    vehicle_db.set_available(id)
    logger.info(f"API | Vehicle {id} successfully returned by customer {customer_id}")
    return {"message": "Vehicle returned successfully"}