import os

# Note: DDB related config are loaded from environment variables
DDB_TODO_TABLE = os.getenv("DDB_TODO_TABLE", "todos")
DDB_ENDPOINT_URL = os.getenv("DDB_ENDPOINT_URL", None)
