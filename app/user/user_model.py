import mysql.connector
from mysql.connector import Error  # Import the specific exception class
from app.shared_services.config import dbconfig
from app.user.user_queries import UserGroceryQueries

class UserModel():
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

    def all_user_model(self):
        try:
            self.cur.execute(UserGroceryQueries.view_products())
            result = self.cur.fetchall()
            if len(result) > 0:
                return {"response": result}
            else:
                return {"message": "No Data Found"}
        except Error as e:
            print(f"Error executing view_products query: {e}")
            return {"message": f"Error: {str(e)}"}

    def book_user_items(self, items):
        try:
            order_id = UserGroceryQueries.generate_order_id()
            success_count = 0

            for item in items:
                item_id = item.get('item_id')
                quantity = item.get('quantity')

                if item_id and quantity:
                    # Associate the generated order ID with each item
                    self.cur.execute(UserGroceryQueries.book_user_item(order_id, item_id, quantity))
                    self.cur.execute(UserGroceryQueries.decrement_units_in_stock(quantity, item_id))
                    success_count += 1

            # Commit changes to the database
            self.con.commit()

            return success_count

        except Error as e:
            # Rollback changes in case of an exception
            self.con.rollback()
            print(f"Error executing book_user_items query: {e}")
            return {"message": f"Error: {str(e)}"}
