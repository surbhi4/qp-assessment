class UserAccessQueries:
    @staticmethod
    def add_user(username, password):
        return f"INSERT INTO users (username, password, role) VALUES ('{username}', '{password}', 'user')"

    @staticmethod
    def verify_user(username, password):
        return f"SELECT user_id FROM users WHERE username = '{username}' AND password = '{password}'"
