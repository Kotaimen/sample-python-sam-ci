from flask_restplus import Namespace, Resource, fields

# XXX: It would be nice if every library just uses marshmallow ...
from todoapi.models.todo import TodoModel

ns = Namespace("todos", description="TODO operations")

todo = ns.model(
    "Todo",
    {
        "id": fields.String(readonly=True, description="The task unique identifier"),
        "task": fields.String(required=True, description="The task details"),
    },
)


@ns.errorhandler(TodoModel.DoesNotExist)
def handle_does_not_exist_exception(e):
    return {"message": str(e)}, 404


@ns.route("/todo/<string:id>")
@ns.response(404, "Todo not found")
@ns.param("id", "The task identifier")
class TodoResource(Resource):
    """Show a single todo item and lets you delete them"""

    @ns.doc("get_todo")
    @ns.marshal_with(todo, envelope="data")
    def get(self, id):
        """Fetch a given resource"""
        item = TodoModel.get(id)
        return item

    @ns.doc("delete_todo")
    @ns.response(204, "Todo deleted")
    def delete(self, id):
        """Delete a task given its identifier"""
        item = TodoModel(id)
        item.delete()
        return "", 204

    @ns.expect(todo)
    @ns.marshal_with(todo, envelope="data")
    def put(self, id):
        """Update a task given its identifier"""
        item = TodoModel(id, **ns.payload)
        item.save()
        return item
