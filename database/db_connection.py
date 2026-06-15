import mysql.connector
import logging


logger = logging.getLogger(__name__)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="rental_api"
    )



def create_tables():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""CREATE TABLE IF NOT EXISTS vehicles(
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   model VARCHAR(50) NOT NULL,
                   brand VARCHAR(50) NOT NULL,
                   category ENUM("Sedan","SUV","Truck","Electric","Luxury") NOT NULL,
                   is_available BOOLEAN NOT NULL DEFAULT TRUE,
                   rented_by_customer_id INT NULL);""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS customers(
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   name VARCHAR(50) NOT NULL,
                   license_number VARCHAR(50) UNIQUE NOT NULL,
                   is_active BOOLEAN NOT NULL DEFAULT TRUE,
                   total_rentals INT DEFAULT 0);""")


    conn.commit()
    cursor.close()
    conn.close()



if __name__=="__main__":
    logger.info("get connection")

