from flask import Blueprint
from flask_restx import Api

from .todo import ns as todo_api

blueprint = Blueprint("api", __name__)
api = Api(blueprint, version="1.0", title="FlaskRest+ API", description="A simple API")

api.add_namespace(todo_api, path="/todos")
