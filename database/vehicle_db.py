import mysql.connector
from database.db_connection import get_connection

class VehicleDB:
    def create_vehicle(self, data: dict):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """
            INSERT INTO vehicles (model, brand, category, is_available, rented_by_customer_id) 
            VALUES (%s, %s, %s, TRUE, NULL)
        """
        try:
            cursor.execute(sql, (data["title"], data["brand"], data["category"]))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def get_all_vehicles(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM vehicles")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_vehicle_by_id(self, vehicle_id: int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def update_vehicle(self, vehicle_id: int, data: dict):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = f"UPDATE vehicles SET model = %s, brand = %s, category = %s, is_available = %s, rented_by_customer_id = %s  WHERE id = %s"
        try:
            cursor.execute(sql,(data["model"],data["brand"],data["category"],data["is_available"],data["rented_by_customer_id"],vehicle_id))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def set_rented(self, vehicle_id: int, customer_id: int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "UPDATE vehicles SET is_available = FALSE, rented_by_customer_id = %s WHERE id = %s"
        try:
            cursor.execute(sql, (customer_id, vehicle_id))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def set_available(self, vehicle_id: int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "UPDATE vehicles SET is_available = TRUE, rented_by_customer_id = NULL WHERE id = %s"
        try:
            cursor.execute(sql, (vehicle_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def count_total_vehicles(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM vehicles")
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            conn.close()

    def count_available_vehicles(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM vehicles WHERE is_available = TRUE")
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            conn.close()

    def count_rented_vehicles(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM vehicles WHERE is_available = FALSE")
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            conn.close()

    def get_vehicles_count_by_category(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT category as Category, COUNT(*) as COUNT FROM vehicles GROUP BY category")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def count_active_rentals_by_customer(self, customer_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM vehicles WHERE rented_by_customer_id = %s", (customer_id,))
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            conn.close()