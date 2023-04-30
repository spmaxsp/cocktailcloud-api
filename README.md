# cocktailcloud-api
## About:
This is the associated api for the cocktailcloud-js project. The server is written in python with flask. It stores the data in a json database and lets you retrieve and modify it via http requests.

## API Calls (V1):

### Cocktails:
-	`/cocktail/list`:  
returns a list of all ids
-	`/cocktail/remove/<id>`:  
removes the cocktail with the given id and returns a new list of all ids
-	`/cocktail/info/<id>`:  
returns the complete json file for the given id

        Sample Data:
        {
            "name": "Test 1",
            "likes": 0,
            "recepie": {
                "1": {
                    "amount": 100,
                    "priority": 10
                },
                "2": {
                    "amount": 400,
                    "priority": 0
                }
            }
        }

-	`/cocktail/new`:  
creates a new empty cocktail and retuns the new id
-	`/cocktail/edit/<id>/<value> [GET: val1=data]`:  
changes the given value of the given id to the given data
-	`/cocktail/edit/<id>/ingrediants/<ingrediant> [GET: val1=value val2=priority]`:  
edits the given ingrediant of the given id and retuns the updated json file (setting value to 0 removes the ingrediant, editing a ingrediant that is not in the list adds it)

Data is always returned in the following format:

> `{'error': False, 'error_msg': '', 'data':{'cocktails':files}}` 

> `{'error': False, 'error_msg': '', 'data':{'cocktail':data}}` 

> `{'error': False, 'error_msg': '', 'data':{'new_id':new_id}}` 

### Users:
-	`/user/list`:  
returns a list of all ids
-	`/user/remove/<id>`:  
removes the user with the given id and returns a new list of all ids
-	`/user/info/<id>`:  
returns the complete json file for the given id

        Sample Data:
        {
            "name": "Test 1",
            "drinks": 0,
            "age": 20,
            "gender": "male",
            "weight": "",
            "attrib": ""
        }

-	`/user/new`:  
creates a new empty user enty and retuns the new id
-	`/user/edit/<id>/<value> [GET: val1=data]`:  
changes the given value of the given id to the given data

Data is always returned in the following format:

> `{'error': False, 'error_msg': '', 'data':{'users':files}}`

> `{'error': False, 'error_msg': '', 'data':{'user':data}}`

> `{'error': False, 'error_msg': '', 'data':{'new_id':new_id}}`

### Ingrediant:
-	`/ingrediant/list`:  
returns a list of all ingrediants and their ids

        Sample Data:
        {
            "1": "Test 1",
            "2": "Test 2"
        }

-	`/ingrediant/new/ [GET: val1=data]`:  
creates a new ingrediant and retuns the new id (the name of the new ingrediant is data)
-	`/ingrediant/delete/<id>`:  
removes the ingrediant and returns a list of all ingrediants and their ids

Data is always returned in the following format:

> `{'error': False, 'error_msg': '', 'data':{'ingrediants':data}}`

> `{'error': False, 'error_msg': '', 'data':{'new_id':new_id}}`

### Settings:
-	`/settings/info`:  
returns all settings

        The Config File:
        {
            "password": "2345",
            "lightcolor1": "",
            "lightcolor2": "",
            "animation": "",
            "pump": [
                "0",
                "1",
                "null",
                "null",
                "null",
                "null",
                "null",
                "null",
                "2",
                "3"
            ],
            "manual": [
                "4"
            ]
        }

-	`/settings/edit/<value> [GET: val1=data]`:  
edits the vlaue to data 

> `{'error': False, 'error_msg': '', 'data':{'config':data}}`

### Images:
- `/image/upload/<database>/<id>`:  
not jet implemented...
- `/image/get/<database>/<id>`:  
returns the image of the given id in the given database


## API Calls (V2):

### Cocktails:
-	`/v2/cocktail/list`:  
returns a list of all ids
-	`/v2/cocktail/remove/<id>`:  
removes the cocktail with the given id and returns a new list of all ids
-	`/v2/cocktail/info/<id> [GET: format=format]`:  
returns the complete json file for the given id. if format is long the data is returned in the following format (else it is returned in the old v1 format):

        Sample Data:
        {
            "likes": 0,
            "name": "Test 1",
            "recepie": {
                "Grenadin": {
                "amount": 400,
                "id": "2",
                "priority": 0
                },
                "Malibu": {
                "amount": 100,
                "id": "1",
                "priority": 10
                }
            }
        }

-	`/cocktail/new`:  
creates a new empty cocktail and retuns the new id
-	`/cocktail/edit/<id>/<value> [GET: val1=data]`:  
changes the given value of the given id to the given data
-	`/cocktail/edit/<id>/ingrediants/<ingrediant> [GET: val1=value val2=priority]`:  
edits the given ingrediant of the given id and retuns the updated json file (setting value to 0 removes the ingrediant, editing a ingrediant that is not in the list adds it)

Data is always returned in the following format:

> `{'error': False, 'error_msg': '', 'data':{'cocktails':files}}` 

> `{'error': False, 'error_msg': '', 'data':{'cocktail':data}}` 

> `{'error': False, 'error_msg': '', 'data':{'new_id':new_id}}` 

### Users:

For the user api v1 and v2 are the same (just the calls start with /v2/...)

### Ingrediant:

### Ingrediant:
-	`/ingrediant/list`:  
returns a list of all ingrediants and their ids

        Sample Data:
        {
            "1": "Test 1",
            "2": "Test 2"
        }

-	`/ingrediant/new/ [GET: val1=data]`:  
creates a new ingrediant and retuns the new id (the name of the new ingrediant is data)

-   `/ingrediant/in_use/<id>/`: 
returns true if the ingrediant is used in a cocktail

-	`/ingrediant/delete/<id>`:  
removes the ingrediant and returns a list of all ingrediants and their ids

Data is always returned in the following format:

> `{'error': False, 'error_msg': '', 'data':{'ingrediants':data}}`

> `{'error': False, 'error_msg': '', 'data':{'new_id':new_id}}`

> `{'error': False, 'error_msg': '', 'data':{'in_use':in_use}}`

### Settings:

For the settings api v1 and v2 are the same (just the calls start with /v2/...)

### Images:

For images use the v1 api (is not jet implemented in v2)


