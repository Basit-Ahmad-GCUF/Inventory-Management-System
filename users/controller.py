import os
from dotenv import load_dotenv
from data.datamanager import Data_Manager

load_dotenv()
username = os.getenv("CONTROLLER_USERNAME")
password = os.getenv("CONTROLLER_PASSWORD")

class controller:
    
    userfilname = "users.json"
    settingsfilename = "settings.json"
    
    def __init__(self):
        self.data_manager = Data_Manager()
        self.username = username
        self.password = password
        
    def change_setting(self, new_setting, parameter_type='name'):
        settings_data = self.data_manager.read_data(self.settingsfilename)
        settings_data[parameter_type] = new_setting
        self.data_manager.write_data(self.settingsfilename, settings_data)
        print(f"{parameter_type.capitalize()} changed to: {new_setting}")
    
    def create_user(self, user_data):
        self.data_manager.add_data(self.userfilname, user_data)
        print(f"User created successfully.")

    def delete_user(self, user_data, parameter_type='id'):
        self.data_manager.delete_data(self.userfilname, user_data[parameter_type])
        print(f"User with {parameter_type} {user_data[parameter_type]} deleted successfully.")

    def update_user(self, user_data, updated_data, parameter_type='id'):
        self.data_manager.update_data(self.userfilname, user_data[parameter_type], updated_data)
        print(f"User with {parameter_type} {user_data[parameter_type]} updated successfully.")
    
