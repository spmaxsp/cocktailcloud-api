import json
from os import listdir, remove
from os.path import isfile, join, exists

class Config:
    def __init__(self, path):
        self.path = path

    def get_pump(self):
        try:
            with open(self.path) as f:
                data = json.load(f)
        except:
            return {}
        return data["pump"]
        
    def get_manual(self):
        try:
            with open(self.path) as f:
                data = json.load(f)
        except:
            return {}
        return data["manual"]
    
    def get_unsupplied(self, ingrediants):
        pump_list = self.get_pump()
        manual_list = self.get_manual()
        list = []
        for ingrediant in ingrediants.get_list():
            if ingrediant not in pump_list and ingrediant not in manual_list:
                list.append(ingrediant)
        return list

    def info(self):
        try:
            with open(self.path) as f:
                data = json.load(f)
        except:
            return {'error': True, 'error_msg': 'Error: Could not read database', 'data':{}}
        return {'error': False, 'error_msg': '', 'data':{'config':data}}
    
    def info_long(self, ingrediants):
        ingrediant_list = ingrediants.get_list()
        try:
            with open(self.path) as f:
                data = json.load(f)
                long_pump = {}
                i = 0
                for pump in data["pump"]:
                    if pump == 'null':
                        long_pump[str(i)] = {'name': ' - ', 'id': 'null'}
                        i += 1
                    else:
                        long_pump[str(i)] = {'name': ingrediant_list[pump], 'id': pump}
                        i += 1
                long_manual = []
                for manual in data["manual"]:
                    long_manual.append({'name': ingrediant_list[manual], 'id': manual})
                long_unsupplied = []
                for unsupplied in self.get_unsupplied(ingrediants):
                    long_unsupplied.append({'name': ingrediant_list[unsupplied], 'id': unsupplied})
                
                data["pump"] = long_pump
                data["manual"] = long_manual
                data["unsupplied"] = long_unsupplied
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
                    data[parameter] = value
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
    
    def edit_v2(self, entry, value, val, ingrediants, long):
        if entry == None:
            return {'error': True, 'error_msg': 'Error: No entry given', 'data':{}}
        if value == None:
            return {'error': True, 'error_msg': 'Error: No value given', 'data':{}}
        if val == None:
            return {'error': True, 'error_msg': 'Error: No val given', 'data':{}}
        
        #try:
        with open(self.path, 'r+') as f:
            data = json.load(f)
            ingrediant_list = ingrediants.get_list()
            if entry == "machine":
                if value == "password":
                    data["password"] = val
                elif value == "lightcolor1":
                    data["lightcolor1"] = val
                elif value == "lightcolor2":
                    data["lightcolor2"] = val
                elif value == "animation":
                    data["animation"] = val
                else:
                    return {'error': True, 'error_msg': 'Error: No valid value', 'data':{}}
            elif entry == "pump":
                if int(value) >= 10:
                    return {'error': True, 'error_msg': 'Error: Pump index out of range', 'data':{}}
                if val != 'null':
                    if str(val) not in ingrediant_list:
                        return {'error': True, 'error_msg': 'Error: Ingrediant does not exist', 'data':{}}
                    if not val in self.get_unsupplied(ingrediants):
                        return {'error': True, 'error_msg': 'Error: Ingrediant is already supplied', 'data':{}}
                data["pump"][int(value)] = str(val)
            elif entry == "manual":
                if value == "add":
                    if val not in ingrediant_list:
                        return {'error': True, 'error_msg': 'Error: Ingrediant does not exist', 'data':{}}
                    if not val in self.get_unsupplied(ingrediants):
                        return {'error': True, 'error_msg': 'Error: Ingrediant is already supplied', 'data':{}}
                    data["manual"].append(val)
                elif value == "remove":
                    if val in data["manual"]:
                        data["manual"].remove(val)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

        #except:
        #    return {'error': True, 'error_msg': 'Error: Could edit file', 'data':{}}
        if long:
            return self.info_long(ingrediants)
        else:
            return self.info()