import mysql.connector
from database.db_connection import get_connection

class CustomerDB:
    def create_customer(self, data: dict):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "INSERT INTO customers (name, license_number, is_active, total_rentals) VALUES (%s, %s, TRUE, 0)"
        try:
            cursor.execute(sql, (data["name"], data["license_number"]))
            conn.commit()
        except mysql.connector.Error as err:
            if err.errno == 1062:  # קוד שגיאה של Duplicate Entry ל-UNIQUE
                raise ValueError("License number already exists")
            raise err
        finally:
            cursor.close()
            conn.close()

    def get_all_customers(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM customers")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_customer_by_id(self, customer_id: int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def update_customer(self, customer_id: int, data: dict):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        fields = [f"{key} = %s" for key in data.keys()]
        values = list(data.values())
        values.append(customer_id)
        sql = f"UPDATE customers SET {', '.join(fields)} WHERE id = %s"
        try:
            cursor.execute(sql, tuple(values))
            conn.commit()
        except mysql.connector.Error as err:
            if err.errno == 1062:
                raise ValueError("License number already exists")
            raise err
        finally:
            cursor.close()
            conn.close()

    def set_customer_status(self, customer_id: int, status: bool):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "UPDATE customers SET is_active = %s WHERE id = %s"
        try:
            cursor.execute(sql, (status, customer_id))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def increment_rentals(self, customer_id: int):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "UPDATE customers SET total_rentals = total_rentals + 1 WHERE id = %s"
        try:
            cursor.execute(sql, (customer_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def count_active_customers(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM customers WHERE is_active = TRUE")
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            conn.close()

    def get_top_customer(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id as `customer id`, total_rentals as rentals FROM customers ORDER BY total_rentals DESC LIMIT 1")
            res = cursor.fetchone()
            return res if res else {"customer id": None, "rentals": 0}
        finally:
            cursor.close()
            conn.close()