from data.datamanager import Data_Manager

class authentication:
    
    userfilname = "users.json"
    
    def __init__(self):
        self.users_data = Data_Manager.read_data(self.userfilname)
    
    def authenticate(self, username, password):
        for user_data in self.users_data:
            if user_data.get("username") == username and user_data.get("password") == password:
                return user_data.get("role")
        return "UNKNOWN"
        
        