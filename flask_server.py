# Cocktail Cloud API:

import logging

from kivy.clock import Clock

import re
from kivy.utils import escape_markup

from flask import Flask
from flask import request
from flask import jsonify, send_file

from flask_cors import CORS

from os.path import join, exists

from cocktailcloud.api.cocktail import Cocktail
from cocktailcloud.api.user import User
from cocktailcloud.api.ingrediant import Ingrediant
from cocktailcloud.api.config import Config
from cocktailcloud.api.prep_info import PreparationInfo

class FlaskServerLogger(logging.Handler):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def __init__(self, label):
        super().__init__()
        self.label = label

    def add_ansi_escape(self, text):
        return escape_markup(self.ansi_escape.sub('', text))

    def emit(self, record):
        msg = self.format(record)
        msg_with_ansi = self.add_ansi_escape(msg)
        print("FlaskServerLogger: " + msg_with_ansi)
        def f(dt=None):
            self.label.text += msg_with_ansi + "\n"
            # Scroll to the end of the label to show the latest log messages
            self.label.scroll_y = 0
        Clock.schedule_once(f)

def start_flask_server(app):
    server = Flask(__name__, static_folder='./react-app/js-build/', static_url_path='/')

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)
    log.addHandler(FlaskServerLogger(app.console_output_label))

    CORS(server)

    cocktails = Cocktail("./database/cocktail_database/")
    users = User("./database/user_database/")
    ingrediants = Ingrediant("./database/ingrediant_database/")
    settings = Config("./database/configuration.json")
    prep_info = PreparationInfo()

        #       REACT
        #
    @server.route('/')
    def index():
        return server.send_static_file('index.html')


        #       IMAGE UPLOAD
        #
    @server.route("/image/upload/<database>/<id>")
    def image_upload(database, id):
        pass


        #       IMAGE DOWNLOAD
        #
    @server.route("/image/get/<database>/<id>")
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
    @server.route("/api/cocktail/<action>")
    @server.route("/api/cocktail/<action>/<id>", methods=['GET'])
    @server.route("/api/cocktail/<action>/<id>/<value>", methods=['GET'])
    @server.route("/api/cocktail/<action>/<id>/<value>/<ingrediant>", methods=['GET'])
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
    @server.route("/api/v2/cocktail/<action>")
    @server.route("/api/v2/cocktail/<action>/<id>", methods=['GET'])
    @server.route("/api/v2/cocktail/<action>/<id>/<value>", methods=['GET'])
    @server.route("/api/v2/cocktail/<action>/<id>/<value>/<ingrediant>", methods=['GET'])
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
    @server.route("/api/user/<action>")
    @server.route("/api/user/<action>/<id>", methods=['GET'])
    @server.route("/api/user/<action>/<id>/<value>", methods=['GET'])
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
    @server.route("/api/v2/user/<action>")
    @server.route("/api/v2/user/<action>/<id>", methods=['GET'])
    @server.route("/api/v2/user/<action>/<id>/<value>", methods=['GET'])
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
    @server.route("/api/ingrediant/<action>", methods=['GET'])
    @server.route("/api/ingrediant/<action>/<id>")
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
    @server.route("/api/v2/ingrediant/<action>", methods=['GET'])
    @server.route("/api/v2/ingrediant/<action>/<id>")
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
    @server.route("/api/settings/<action>", methods=['GET'])
    @server.route("/api/settings/<action>/<value>", methods=['GET'])
    def setting_request(action, value=None):
        match action:
            case "info":
                return jsonify(settings.info())
            case "edit":
                return jsonify(settings.edit(value, request.args.get("val1"), ingrediants))


        #       SETTINGS V2
        #
    @server.route("/api/v2/settings/<action>/", methods=['GET'])
    @server.route("/api/v2/settings/<action>/<entry>/<value>", methods=['GET'])
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
                
        #       PREPARATION INFO V1
        #
    @server.route("/api/v1/preparation/<action>/<id>", methods=['GET'])
    @server.route("/api/v1/preparation/<action>/<id>/<value>", methods=['GET'])
    def preparation_request(action, id=None, value=None):
        match action:
            case "prepare_prepinfo":
                return jsonify(prep_info.prepare_prepinfo(id, cocktails, settings, ingrediants))
            case "num_steps":
                if request.args.get("format") == "long":
                    return jsonify(prep_info.number_of_steps_json(id))
                else:
                    return prep_info.number_of_steps_simple(id)
            case "manual_info":
                return jsonify(prep_info.manual_steps(id))
            case "step_info":
                if request.args.get("format") == "long":
                    return jsonify(prep_info.step_info_json(id, value))
                else:
                    return prep_info.step_info_simple(id, value)

                
    server.run(host='localhost', port='43560')