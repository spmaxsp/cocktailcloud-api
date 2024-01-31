import json
from os import listdir, remove
from os.path import isfile, join, exists

from itertools import groupby

class PreparationInfo:
    automatic_list = []
    manual_list = []
    prepared_id = None

    def generate_presorted_list(data):
        sorted_data = sorted(data, key=lambda x: x['priority'], reverse=True)
        return sorted_data

    def generate_grouped_list(data):    
        result = []
        for key, group in groupby(data, key=lambda x: x['priority']):
            result.append(list(group))
        return result
    
    def map_ingredients_to_pumps(data, pump, manual):
        automatic_list = []
        manual_list = []
        available = True

        for item in data:
            item_id = item['id']
            if item_id in pump:
                index = pump.index(item_id)
                item['pump'] = index
                del item['id']
                automatic_list.append(item)
            elif item_id in manual:
                manual_list.append(item)
            else:
                available = False
                break

        return automatic_list, manual_list, available
    
    def create_step_list(data):
        steplist = []
        for sublist in data:
            sorted_sublist = sorted(sublist, key=lambda x: x['amount'])
            while len(sorted_sublist) > 0:
                pumplist = []
                for item in sorted_sublist:
                    pumplist.append(item['pump'])

                current_item = sorted_sublist.pop(0)

                if current_item['amount'] > 0:
                    steplist.append({'pumps': pumplist, 'amount': current_item['amount']})

                    for item in sorted_sublist:
                        item['amount'] -= current_item['amount']
        return steplist
    
    def map_ingredients_to_names(data, ingredients):
        print (data)
        for item in data:
            item_id = item['id']
            if item_id in ingredients:
                item['name'] = ingredients[item_id]
                del item['id']
                del item['priority']
        return data

    def prepare_prepinfo(self, id, cocktails, settings, ingredients):
        recepie_list = cocktails.get_recepie_as_list(id)
        pump = settings.get_pump()
        manual = settings.get_manual()
        ingredients = ingredients.get_list()

        automatic_list, manual_list, available = PreparationInfo.map_ingredients_to_pumps(recepie_list, pump, manual)

        if available:
            sorted_automatic_list = PreparationInfo.generate_presorted_list(automatic_list)
            sorted_manual_list = PreparationInfo.generate_presorted_list(manual_list)

            grouped_automatic_list = PreparationInfo.generate_grouped_list(sorted_automatic_list)
            step_list = PreparationInfo.create_step_list(grouped_automatic_list)

            long_manual_list = PreparationInfo.map_ingredients_to_names(sorted_manual_list, ingredients)
        
            print(step_list)
            print(long_manual_list)

            self.prepared_id = id
            self.automatic_list = step_list
            self.manual_list = long_manual_list

            return {'error': False, 'error_msg': '', 'data':'OK'}
        else:
            return {'error': True, 'error_msg': 'Not enough ingredients', 'data': ''}

    def number_of_steps_json(self, id):
        if self.prepared_id == id:
            return {'error': False, 'error_msg': '', 'data': len(self.automatic_list)}
        else:
            return {'error': True, 'error_msg': 'Not prepared', 'data': ''}
        
    def number_of_steps_simple(self, id):
        if self.prepared_id == id:
            return str(len(self.automatic_list))
        else:
            return 'ERR'
        
    def manual_steps(self, id):   
        if self.prepared_id == id:
            return {'error': False, 'error_msg': '', 'data': self.manual_list}
        else:
            return {'error': True, 'error_msg': 'Not prepared', 'data': 'Not prepared'}

    def step_info_json(self, id, step):
        if self.prepared_id == id:
            if int(step) < len(self.automatic_list):
                return {'error': False, 'error_msg': '', 'data': self.automatic_list[int(step)]}
            else:
                return {'error': True, 'error_msg': 'Step out of range', 'data': 'Step out of range'}
        else:
            return {'error': True, 'error_msg': 'Not prepared', 'data': 'Not prepared'}
        
    def step_info_simple(self, id, step):
        # ans_str = 100|XXXXXXXXXX (10 pumps as binary)
        # ans_str = ERR

        ans_str = ''
        if self.prepared_id == id:
            if int(step) < len(self.automatic_list):
                ans_str += str(step) + '|'
                ans_str += str(self.automatic_list[int(step)]['amount']) + '|'
                for i in range(10):
                    if i in self.automatic_list[int(step)]['pumps']:
                        ans_str += '1'
                    else:
                        ans_str += '0'
            else:
                ans_str = 'ERR'
        else:
            ans_str = 'ERR'
        return ans_str