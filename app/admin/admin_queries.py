class GroceryItemQueries:
    @staticmethod
    def view_products():
        return "SELECT * FROM grocery_items WHERE units_in_stock > 0"

    @staticmethod
    def add_new_product(name,price,units):
        return f"INSERT INTO grocery_items (item_name, item_price, units_in_stock) VALUES ('{name}', '{price}', '{units}')"

    @staticmethod
    def delete_product(name):
        return f"DELETE FROM grocery_items WHERE item_name = '{name}'"

    @staticmethod
    def update_product(price,name,id):
        return f"UPDATE grocery_items SET item_price = '{price}', item_name = '{name}' WHERE item_id = '{id}'"

    @staticmethod
    def manage_inventory(units,name):
        return f"UPDATE grocery_items SET units_in_stock = '{units}' WHERE item_name = '{name}' "
