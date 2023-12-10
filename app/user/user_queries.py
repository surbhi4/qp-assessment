from uuid import uuid4

class UserGroceryQueries:
    @staticmethod
    def generate_order_id():
        return str(uuid4())

    @staticmethod
    def book_user_item(order_id, item_id, quantity):
        return f"INSERT INTO order_items (order_id, item_id, quantity) VALUES ('{order_id}', '{item_id}', '{quantity}')"

    @staticmethod
    def decrement_units_in_stock(quantity, item_id):
        return f"UPDATE grocery_items SET units_in_stock = units_in_stock - {quantity} WHERE item_id = '{item_id}'"
