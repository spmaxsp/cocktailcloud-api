import json
from os import listdir, remove
from os.path import isfile, join, exists

class Ingrediant:
    def __init__(self, path):
        self.path = path
    
    def list(self):
        try:
            with open(join(self.path, 'global.json')) as f:
                data = json.load(f)
        except:
            return {'error': True, 'error_msg': 'Error: Could not read database', 'data':{}}
        return {'error': False, 'error_msg': '', 'data':{'ingrediants':data}}

    def new(self, value):
        if value == None:
            return {'error': True, 'error_msg': 'Error: No value given', 'data':{}}
        try:
            with open(join(self.path, 'global.json'), 'r+') as f:
                data = json.load(f)
                new_id = 0
                while str(new_id) in data:
                    new_id += 1
                data[str(new_id)] = value
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()  
        except:
            return {'error': True, 'error_msg': 'Error: Could edit file', 'data':{}}
        return {'error': False, 'error_msg': '', 'data':{'new_id':new_id}}

    def delete(self, id, cocktails, settings):
        if not cocktails.del_check(id):
            return {'error': True, 'error_msg': 'Error: Ingrediant is still in use by cocktail', 'data':{}}
        if id in settings.info["pump"].values():
            return {'error': True, 'error_msg': 'Error: Ingrediant is still in use by pump', 'data':{}}
        if id in settings.info["manual"].values():
            return {'error': True, 'error_msg': 'Error: Ingrediant is still in use by pump (manual)', 'data':{}}
        try:
            with open(join(self.path, 'global.json'), 'r+') as f:
                data = json.load(f)
                if str(id) not in data:
                    return {'error': True, 'error_msg': 'Error: Ingrediant does not exist', 'data':{}}
                del data[str(id)]
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        except:
            return {'error': True, 'error_msg': 'Error: Could edit file', 'data':{}}
        return {'error': False, 'error_msg': '', 'data':{'ingrediants':data}} 
