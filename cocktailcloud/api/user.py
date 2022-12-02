import json
from os import listdir, remove
from os.path import isfile, join, exists

class User:
    def __init__(self, path):
        self.path = path
        
    def list(self):
        try:
            files = [".".join(f.split(".")[:-1]) for f in listdir(join(self.path, "user")) if isfile(join(self.path, "user", f))]
        except:
            return {'error': True, 'error_msg': 'Error: Could not read database', 'data':{}}
        return {'error': False, 'error_msg': '', 'data':{'users':files}}

    def info(self, id):
        try:
            with open(join(self.path, "user", f'{id}.json')) as f:
                data = json.load(f)
        except:
            return {'error': True, 'error_msg': 'Error: Could not read file with given id', 'data':{}}
        return {'error': False, 'error_msg': '', 'data':{'user':data}}

    def remove(self, id):
        try:
            remove(join(self.path, "user", f'{id}.json'))
            files = [".".join(f.split(".")[:-1]) for f in listdir(join(self.path, "user")) if isfile(join(self.path, "user", f))]
        except:
            return {'error': True, 'error_msg': 'Error: Could not remove file with given id', 'data':{}}
        return {'error': False, 'error_msg': '', 'data':{'users':files}}

    def new(self):
        try:
            new_id = 0
            while exists(join(self.path, "user", f'{new_id}.json')):
                new_id += 1
            with open(join(self.path, "user", f'{new_id}.json'), 'w') as f:
                data = {"name": "", "drinks": 0, "age": 0, "gender": "male", "weight": 0, "attrib": ""}
                json.dump(data, f)
        except:
            return {'error': True, 'error_msg': 'Error: Error while creating new file', 'data':{}}
        return {'error': False, 'error_msg': '', 'data':{'new_id':new_id}}

    def edit_main(self, id, parameter, value):
        if value == None:
            return {'error': True, 'error_msg': 'Error: No value given', 'data':{}}
        try:
            with open(join(self.path, "user", f'{id}.json'), 'r+') as f:
                data = json.load(f)
                if parameter == "drinks" or parameter == "age" or parameter == "weight":
                    data[parameter] = int(value)
                elif parameter == "name" or parameter == "gender" or parameter == "attrib":
                    data[parameter] = value
                else:
                    return {'error': True, 'error_msg': 'Error: No valid parameter', 'data':{}}
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        except:
            return {'error': True, 'error_msg': 'Error: Could edit file with given id', 'data':{}}
        return {'error': False, 'error_msg': '', 'data':{'user':data}}
