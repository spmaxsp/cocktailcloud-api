import json
from os import listdir, remove
from os.path import isfile, join, exists

class Config:
    def __init__(self, path):
        self.path = path

    def info(self):
        try:
            with open(self.path) as f:
                data = json.load(f)
        except:
            return {'error': True, 'error_msg': 'Error: Could not read database', 'data':{}}
        return {'error': False, 'error_msg': '', 'data':{'config':data}}

    def edit(self, parameter, value, ingrediants):
        if value == None:
            return {'error': True, 'error_msg': 'Error: No value given', 'data':{}}
        try:
            with open(self.path, 'r+') as f:
                data = json.load(f)
                if parameter in ["password", "lightcolor1", "lightcolor2", "animation"]:
                    data["parameter"] = value
                elif parameter == "manual":
                    if value == "null":
                        data["manual"] = []
                    else:
                        for item in value.split(','):
                            if item not in ingrediants.list():
                                return {'error': True, 'error_msg': 'Error: Ingrediant does not exist', 'data':{}}
                        data["manual"] = value.split(',')
                elif parameter.split('_')[0] == "pump" and len(parameter.split('_')) == 2:
                    if int(parameter.split('_')[1]) >= 10:
                        return {'error': True, 'error_msg': 'Error: Pump index out of range', 'data':{}}
                    if value != 'null':
                        if value not in ingrediants.list():
                            return {'error': True, 'error_msg': 'Error: Ingrediant does not exist', 'data':{}}
                    data[parameter.split('_')[0]][int(parameter.split('_')[1])] = value
                #elif parameter.split('_')[0] == "manual" and len(parameter.split('_')) == 2:
                #    if value not in ingrediants.list():
                #        return 'Error: Ingrediant does not exist'
                #    if parameter.split('_')[1] == "add":
                #        data[parameter.split('_')[0]].append(value)
                #    elif parameter.split('_')[1] == "remove":
                #        if value in data[parameter.split('_')[0]]:
                #            data[parameter.split('_')[0]].remove(value)
                else:
                    return {'error': True, 'error_msg': 'Error: No valid parameter', 'data':{}}
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        except:
            return {'error': True, 'error_msg': 'Error: Could edit file', 'data':{}}
        return {'error': False, 'error_msg': '', 'data':{'config':data}}