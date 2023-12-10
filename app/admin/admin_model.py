import mysql.connector
from mysql.connector import Error  # Import the specific exception class
from app.admin.admin_queries import GroceryItemQueries
from app.shared_services.config import dbconfig

class AdminModel():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(
                host=dbconfig['host'],
                user=dbconfig['username'],
                password=dbconfig['password'],
                database=dbconfig['database']
            )
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print("success")
        except Error as e:
            print(f"Error connecting to the database: {e}")

    def view_products(self):
        try:
            self.cur.execute(GroceryItemQueries.view_products())
            result = self.cur.fetchall()
            if len(result) > 0:
                return {"response": result}
            else:
                return {"message": "No Data Found"}
        except Error as e:
            print(f"Error executing view_products query: {e}")
            return {"message": f"Error: {str(e)}"}

    def add_items(self, params):
        try:
            name = params['name']
            price = params['price']
            units = params['units']
            self.cur.execute(GroceryItemQueries.add_new_product(name, price, units))
            print("success")
        except Error as e:
            print(f"Error executing add_items query: {e}")

    def delete(self, name):
        try:
            self.cur.execute(GroceryItemQueries.delete_product(name))
            print("success")
        except Error as e:
            print(f"Error executing delete query: {e}")

    def manage_inventory(self, params):
        try:
            name = params['name']
            units = params['units']
            self.cur.execute(GroceryItemQueries.manage_inventory(units, name))
            print("success")
        except Error as e:
            print(f"Error executing manage_inventory query: {e}")

    def update_product(self, params):
        try:
            name = params['name']
            id = params['id']
            price = params['price']
            self.cur.execute(GroceryItemQueries.update_product(price, name, id))
            print("success")
        except Error as e:
            print(f"Error executing update_product query: {e}")
