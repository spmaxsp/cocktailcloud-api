import json
from os import listdir, remove
from os.path import isfile, join, exists

class Cocktail:
    def __init__(self, path):
        self.path = path
        
    def list(self):
        try:
            files = [".".join(f.split(".")[:-1]) for f in listdir(join(self.path, "cocktail")) if isfile(join(self.path, "cocktail", f))]
        except:
            return {'error': True, 'error_msg': 'Error: Could not read database', 'data':{}}
        return {'error': False, 'error_msg': '', 'data':{'cocktails':files}}

    def info(self, id):
        try:
            with open(join(self.path, "cocktail", f'{id}.json')) as f:
                data = json.load(f)
        except:
            return {'error': True, 'error_msg': 'Error: Could not read file with given id', 'data':{}}
        return {'error': False, 'error_msg': '', 'data':{'cocktail':data}}

    def info_long(self, id, ingrediants):
        try:
            with open(join(self.path, "cocktail", f'{id}.json')) as f:
                data = json.load(f)
                long_recepie = {}
                for ingrediant in data["recepie"]:
                    ingrediant_name = ingrediants.list()["data"]["ingrediants"][str(ingrediant)]
                    long_recepie[ingrediant_name] = data["recepie"][ingrediant]
                    long_recepie[ingrediant_name]["id"] = ingrediant
                data["recepie"] = long_recepie 
                data["available"] = ingrediants.list()["data"]["ingrediants"]
        except:
            return {'error': True, 'error_msg': 'Error: Could not read file with given id', 'data':{}}
        return {'error': False, 'error_msg': '', 'data':{'cocktail':data}}

    def remove(self, id):
        try:
            remove(join(self.path, "cocktail", f'{id}.json'))
            files = [".".join(f.split(".")[:-1]) for f in listdir(join(self.path, "cocktail")) if isfile(join(self.path, "cocktail", f))]
        except:
            return {'error': True, 'error_msg': 'Error: Could not remove file with given id', 'data':{}}
        return {'error': False, 'error_msg': '', 'data':{'cocktails':files}}

    def new(self):
        try:
            new_id = 0
            while exists(join(self.path, "cocktail", f'{new_id}.json')):
                new_id += 1
            with open(join(self.path, "cocktail", f'{new_id}.json'), 'w') as f:
                data = {"name": "", "likes": 0, "recepie":{}}
                json.dump(data, f)
        except:
            return {'error': True, 'error_msg': 'Error: Error while creating new file', 'data':{}}
        return self.list()

    def edit_main(self, id, parameter, value, ingrediants, format):
        if value == None:
            return {'error': True, 'error_msg': 'Error: No value given', 'data':{}}
        try:
            with open(join(self.path, "cocktail", f'{id}.json'), 'r+') as f:
                data = json.load(f)
                if parameter == "likes":
                    data[parameter] = int(value)
                elif parameter == "name":
                    data[parameter] = value
                else:
                    return {'error': True, 'error_msg': 'Error: No valid parameter', 'data':{}}
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        except:
            return {'error': True, 'error_msg': 'Error: Could edit file with given id', 'data':{}}
        if format == "long":
            return self.info_long(id, ingrediants)
        else:
            return self.info(id)

    def edit_ingrediant(self, id, ingrediant, value, priority, ingrediants, long):
        if value == None or priority == None:
            return {'error': True, 'error_msg': 'Error: No values given', 'data':{}}
        if ingrediant not in ingrediants.get_list():
            return {'error': True, 'error_msg': 'Error: Ingrediant does not exist', 'data':{}}
        #try:
        with open(join(self.path, "cocktail", f'{id}.json'), 'r+') as f:
            data = json.load(f)
            data["recepie"][str(ingrediant)] = {"amount":int(value),"priority":int(priority)}
            if value == "0":
                del data["recepie"][str(ingrediant)]
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        #except:
        #    return 'Error: Could edit file with given id'
        if long:
            return self.info_long(id, ingrediants)
        else:
            return self.info(id)

    
    def get_cocktails(self):
        try:
            files = [".".join(f.split(".")[:-1]) for f in listdir(join(self.path, "cocktail")) if isfile(join(self.path, "cocktail", f))]
        except:
            return {}
        return files
    
    def get_recepie(self, id):
        try:
            with open(join(self.path, "cocktail", f'{id}.json')) as f:
                data = json.load(f)
        except:
            return {}
        return data["recepie"]

    def del_check(self, id):
        for c_entry in self.get_cocktails():
            if id in self.get_recepie(c_entry):
                return False
        return True
