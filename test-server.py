# Cocktail Cloud API:

from flask import Flask
from flask import request
from flask import jsonify, send_file

from flask_cors import CORS

from os.path import join, exists

from cocktailcloud.api.cocktail import Cocktail
from cocktailcloud.api.user import User
from cocktailcloud.api.ingrediant import Ingrediant
from cocktailcloud.api.config import Config

app = Flask(__name__, static_folder='./react-app/js-build/', static_url_path='/')
CORS(app)

cocktails = Cocktail("./database/cocktail_database/")
users = User("./database/user_database/")
ingrediants = Ingrediant("./database/ingrediant_database/")
settings = Config("./database/configuration.json")


    #       REACT
    #
@app.route('/')
def index():
    return app.send_static_file('index.html')


    #       IMAGE UPLOAD
    #
@app.route("/image/upload/<database>/<id>")
def image_upload(database, id):
    pass


    #       IMAGE DOWNLOAD
    #
@app.route("/image/get/<database>/<id>")
def image_download(database, id):
    if database == "cocktail":
        file = join(cocktails.path, "img", str(id)+'.jpg')
        if not exists(file):
            file = join(cocktails.path, "img", str(id)+'.png')
    elif database == "user":
        file = join(users.path, "img", str(id)+'.jpg')
        if not exists(file):
            file = join(cocktails.path, "img", str(id)+'.png')
    else:
        file = "./no_img.jpg"

    if exists(file):
        return send_file(file, mimetype='image/jpg')
    else:
        file = "./no_img.jpg"
        return send_file(file, mimetype='image/jpg')


    #       COCKTAILS V1
    #    
@app.route("/api/cocktail/<action>")
@app.route("/api/cocktail/<action>/<id>", methods=['GET'])
@app.route("/api/cocktail/<action>/<id>/<value>", methods=['GET'])
@app.route("/api/cocktail/<action>/<id>/<value>/<ingrediant>", methods=['GET'])
def cocktail_request(action, id=None, value=None, ingrediant=None):
    match action:
        case "list":
            return jsonify(cocktails.list())
        case "remove":
            return jsonify(cocktails.remove(id))
        case "info":
            return jsonify(cocktails.info(id))
        case "new":
            return jsonify(cocktails.new())
        case "edit":
            if value == "ingrediants":
                return jsonify(cocktails.edit_ingrediant(id, ingrediant, request.args.get("val1"), request.args.get("val2"), ingrediants))
            else:
                return jsonify(cocktails.edit_main(id, value ,request.args.get("val1")))


    #       COCKTAILS V2
    #
@app.route("/api/v2/cocktail/<action>")
@app.route("/api/v2/cocktail/<action>/<id>", methods=['GET'])
@app.route("/api/v2/cocktail/<action>/<id>/<value>", methods=['GET'])
@app.route("/api/v2/cocktail/<action>/<id>/<value>/<ingrediant>", methods=['GET'])
def cocktail_request_v2(action, id=None, value=None, ingrediant=None):
    match action:
        case "list":
            return jsonify(cocktails.list())
        case "remove":
            return jsonify(cocktails.remove(id))
        case "info":
            if request.args.get("format") == "long":
                return jsonify(cocktails.info_long(id, ingrediants))
            else:
                return jsonify(cocktails.info(id))
        case "new":
            return jsonify(cocktails.new())
        case "edit":
            if value == "ingrediants":
                return jsonify(cocktails.edit_ingrediant(id, ingrediant, request.args.get("amount"), request.args.get("priority"), ingrediants, request.args.get("format")))
            else:
                return jsonify(cocktails.edit_main(id, value ,request.args.get("val"), ingrediants, request.args.get("format")))


    #       USER V1
    #       
@app.route("/api/user/<action>")
@app.route("/api/user/<action>/<id>", methods=['GET'])
@app.route("/api/user/<action>/<id>/<value>", methods=['GET'])
def user_request(action, id=None, value=None, ingrediant=None):
    match action:
        case "list":
            return jsonify(users.list())
        case "remove":
            return jsonify(users.remove(id))
        case "info":
            return jsonify(users.info(id))
        case "new":
            return jsonify(users.new())
        case "edit":
            return jsonify(users.edit_main(id, value ,request.args.get("val1")))
        

    #       USER V2
    #
@app.route("/api/v2/user/<action>")
@app.route("/api/v2/user/<action>/<id>", methods=['GET'])
@app.route("/api/v2/user/<action>/<id>/<value>", methods=['GET'])
def user_request_v2(action, id=None, value=None, ingrediant=None):
    match action:
        case "list":
            return jsonify(users.list())
        case "remove":
            return jsonify(users.remove(id))
        case "info":
            return jsonify(users.info(id))
        case "new":
            return jsonify(users.new())
        case "edit":
            return jsonify(users.edit_main(id, value ,request.args.get("val")))


    #       INGREDIANTS V1
    #
@app.route("/api/ingrediant/<action>", methods=['GET'])
@app.route("/api/ingrediant/<action>/<id>")
def ingrediant_request(action, id=None):
    match action:
        case "list":
            return jsonify(ingrediants.list())
        case "new":
            return jsonify(ingrediants.new(request.args.get("val1")))
        case "delete":
            return jsonify(ingrediants.delete(id, cocktails, settings))


    #       INGREDIANTS V2
    #
@app.route("/api/v2/ingrediant/<action>", methods=['GET'])
@app.route("/api/v2/ingrediant/<action>/<id>")
def ingrediant_request_v2(action, id=None):
    match action:
        case "list":
            return jsonify(ingrediants.list())
        case "new":
            return jsonify(ingrediants.new_v2(request.args.get("val")))
        case "remove":
            return jsonify(ingrediants.delete(id, cocktails, settings))
        case "info":
            return jsonify(ingrediants.info(id, cocktails, settings))


    #       SETTINGS V1
    #
@app.route("/api/settings/<action>", methods=['GET'])
@app.route("/api/settings/<action>/<value>", methods=['GET'])
def setting_request(action, value=None):
    match action:
        case "info":
            return jsonify(settings.info())
        case "edit":
            return jsonify(settings.edit(value, request.args.get("val1"), ingrediants))


    #       SETTINGS V2
    #
@app.route("/api/v2/settings/<action>/", methods=['GET'])
@app.route("/api/v2/settings/<action>/<entry>/<value>", methods=['GET'])
def setting_request_v2(action, entry=None, value=None):
    match action:
        case "info":
            if request.args.get("format") == "long":
                return jsonify(settings.info_long(ingrediants))
            else:
                return jsonify(settings.info())
        case "edit":
            if request.args.get("format") == "long":
                return jsonify(settings.edit_v2(entry, value, request.args.get("val"), ingrediants, True))
            else:
                return jsonify(settings.edit_v2(entry, value, request.args.get("val"), ingrediants, False))
                
        

if __name__ == "__main__":
    app.run(host='localhost', port='43560')


