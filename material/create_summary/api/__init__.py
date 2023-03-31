from flask import Flask, make_response, jsonify
from flask_cors import CORS


def create_app():
    index_folder = "../../frontend/dist"
    static_folder = "{}/_assets".format(index_folder)
    app = Flask(__name__,static_folder=static_folder,template_folder=index_folder)
    app.config["JSON_AS_ASCII"] = False
    CORS(app)
    app.config.from_object('config.Config')

    return app

app = create_app()