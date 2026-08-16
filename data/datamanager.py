import json

class Data_Manager:
    
    def read_data(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    
    def write_data(self, file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4) 
            
    def add_data(self, file_path, new_data):
        data = self.read_data(file_path)
        data.append(new_data)
        self.write_data(file_path, data)
        
    def delete_data(self, file_path, item_id):
        data = self.read_data(file_path)
        data = [item for item in data if item['id'] != item_id]
        self.write_data(file_path, data)
        
    def update_data(self, file_path, item_id, updated_data):
        data = self.read_data(file_path)
        for index, item in enumerate(data):
            if item['id'] == item_id:
                data[index] = updated_data
                break
        self.write_data(file_path, data)
        
    def find_data(self, file_path, item_parameter, parameter_type='name'):
        data = self.read_data(file_path)
        for item in data:
            if item[parameter_type].lower() == item_parameter.lower():
                return item
        return None