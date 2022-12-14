# cocktailcloud-api
## About:
This is the associated api for the cocktailcloud-js project. The server is written in python with flask. It stores the data in a json database and lets you retrieve and modify it via http requests.

## API Calls:

### Cocktails:
-	`/cocktail/list`:  
returns a list of all ids
-	`/cocktail/remove/<id>`:  
removes the cocktail with the given id and returns a new list of all ids
-	`/cocktail/info/<id>`:  
returns the complete json file for the given id
-	`/cocktail/new`:  
creates a new empty cocktail and retuns the new id
-	`/cocktail/edit/<id>/<value> [GET: val1=data]`:  
changes the given value of the given id to the given data
-	`/cocktail/edit/<id>/ingrediants/<ingrediant> [GET: val1=value val2=priority]`:  
edits the given ingrediant of the given id and retuns the updated json file (setting value to 0 removes the ingrediant, editing a ingrediant that is not in the list adds it)

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
-	`/user/new`:  
creates a new empty user enty and retuns the new id
-	`/user/edit/<id>/<value> [GET: val1=data]`:  
changes the given value of the given id to the given data

> `{'error': False, 'error_msg': '', 'data':{'users':files}}`

> `{'error': False, 'error_msg': '', 'data':{'user':data}}`

> `{'error': False, 'error_msg': '', 'data':{'new_id':new_id}}`

### Ingrediant:
-	`/ingrediant/list`:  
returns a list of all ingrediants and their ids
-	`/ingrediant/new/ [GET: val1=data]`:  
creates a new ingrediant and retuns the new id (the name of the new ingrediant is data)
-	`/ingrediant/delete/<id>`:  
removes the ingrediant and returns a list of all ingrediants and their ids

> `{'error': False, 'error_msg': '', 'data':{'ingrediants':data}}`

> `{'error': False, 'error_msg': '', 'data':{'new_id':new_id}}`

### Settings:
-	`/settings/info`:  
returns all settings
-	`/settings/edit/<value> [GET: val1=data]`:  
edits the vlaue to data 

> `{'error': False, 'error_msg': '', 'data':{'config':data}}`

### Images:
- `/image/upload/<database>/<id>`:  
not jet implemented...
- `/image/get/<database>/<id>`:  
returns the image of the given id in the given database

