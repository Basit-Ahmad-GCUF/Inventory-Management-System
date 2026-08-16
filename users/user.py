class user:
    def __init__(self, user_id, username, password, role, email):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role
        self.email = email

    def to_dict(self):
        return {
            "id": self.user_id,
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "email": self.email
        }
    
    def from_dict(cls, data):
        return cls(
            user_id=data.get("id"),
            username=data.get("username"),
            password=data.get("password"),
            role=data.get("role"),
            email=data.get("email")
        )