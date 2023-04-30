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

app = Flask(__name__)
CORS(app)

cocktails = Cocktail("./database/cocktail_database/")
users = User("./database/user_database/")
ingrediants = Ingrediant("./database/ingrediant_database/")
settings = Config("./database/configuration.json")

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
    elif database == "user":
        file = join(users.path, "img", str(id)+'.jpg')
    else:
        file = "./no_img.jpg"
    if exists(file):
        return send_file(file, mimetype='image/jpg')
    else:
        file = "./no_img.jpg"
        return send_file(file, mimetype='image/jpg')


    #       COCKTAILS V1
    #    
@app.route("/cocktail/<action>")
@app.route("/cocktail/<action>/<id>", methods=['GET'])
@app.route("/cocktail/<action>/<id>/<value>", methods=['GET'])
@app.route("/cocktail/<action>/<id>/<value>/<ingrediant>", methods=['GET'])
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
@app.route("v2/cocktail/<action>")
@app.route("v2/cocktail/<action>/<id>", methods=['GET'])
@app.route("v2/cocktail/<action>/<id>/<value>", methods=['GET'])
@app.route("v2/cocktail/<action>/<id>/<value>/<ingrediant>", methods=['GET'])
def cocktail_request_v2(action, id=None, value=None, ingrediant=None):
    match action:
        case "list":
            return jsonify(cocktails.list())
        case "remove":
            return jsonify(cocktails.remove(id))
        case "info":
            if request.args.get("fromat") == "long"
                return jsonify(cocktails.info_long(id, ingrediants))
            else:
                return jsonify(cocktails.info(id))
        case "new":
            return jsonify(cocktails.new())
        case "edit":
            if value == "ingrediants":
                return jsonify(cocktails.edit_ingrediant(id, ingrediant, request.args.get("amount"), request.args.get("priority"), ingrediants))
            else:
                return jsonify(cocktails.edit_main(id, value ,request.args.get("val")))


    #       USER V1
    #       USER V2
    #
@app.route("/v2/user/<action>")
@app.route("/v2/user/<action>/<id>", methods=['GET'])
@app.route("/v2/user/<action>/<id>/<value>", methods=['GET'])
@app.route("/user/<action>")
@app.route("/user/<action>/<id>", methods=['GET'])
@app.route("/user/<action>/<id>/<value>", methods=['GET'])
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


    #       INGREDIANTS V1
    #
@app.route("/ingrediant/<action>", methods=['GET'])
@app.route("/ingrediant/<action>/<id>")
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
@app.route("/v2/ingrediant/<action>", methods=['GET'])
@app.route("/v2/ingrediant/<action>/<id>")
def ingrediant_request_v2(action, id=None):
    match action:
        case "list":
            return jsonify(ingrediants.list())
        case "new":
            return jsonify(ingrediants.new(request.args.get("val1")))
        case "in_use":
            return jsonify(ingrediants.in_use(id, cocktails))
        case "delete":
            return jsonify(ingrediants.delete(id, cocktails, settings))


    #       SETTINGS V1
    #       SETTINGS V2
    #
@app.route("/settings/<action>")
@app.route("/settings/<action>/<value>", methods=['GET'])
def setting_request(action, value=None):
    match action:
        case "info":
            return jsonify(settings.info())
        case "edit":
            return jsonify(settings.edit(value, request.args.get("val1"), ingrediants))


if __name__ == "__main__":
    app.run(host='localhost', port='43560')


