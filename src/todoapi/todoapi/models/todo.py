from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model

from todoapi.config import DDB_TODO_TABLE, DDB_ENDPOINT_URL


class TodoModel(Model):
    class Meta:
        table_name = DDB_TODO_TABLE
        host = DDB_ENDPOINT_URL

    id = UnicodeAttribute(hash_key=True)
    task = UnicodeAttribute()
