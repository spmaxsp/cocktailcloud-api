import json
from os import listdir, remove
from os.path import isfile, join, exists

class Ingrediant:
    def __init__(self, path):
        self.path = path

    def get_list(self):
        try:
            with open(join(self.path, 'global.json')) as f:
                data = json.load(f)
        except:
            return {}
        return data
    
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
    
    def new_v2(self, value):
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
        return self.list()

    def delete(self, id, cocktails, settings):
        if not cocktails.del_check(id):
            return {'error': True, 'error_msg': 'Error: Ingrediant is still in use by cocktail', 'data':{}}
        if id in settings.get_pump():
            return {'error': True, 'error_msg': 'Error: Ingrediant is still in use by pump', 'data':{}}
        if id in settings.get_manual():
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
    
    
    def info(self, id, cocktails, settings):
        info = {}
        info['in_use_by_cocktail'] = not cocktails.del_check(id)
        info['is_supplyed'] = False
        info['is_supplyed_by'] = ''
        if id in settings.get_pump():
            info['is_supplyed'] = True
            info['is_supplyed_by'] = settings.get_pump().index(id)
        elif id in settings.get_manual():
            info['is_supplyed'] = True
            info['is_supplyed_by'] = 'manual'
        try:
            with open(join(self.path, 'global.json')) as f:
                data = json.load(f)
                if str(id) not in data:
                    return {'error': True, 'error_msg': 'Error: Ingrediant does not exist', 'data':{}}
                info['value'] = data[str(id)]
        except:
            return {'error': True, 'error_msg': 'Error: Could not read database', 'data':{}}
        return {'error': False, 'error_msg': '', 'data':{'ingrediant':info}}
