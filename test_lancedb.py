import lancedb

db = lancedb.connect("knowledge_base")
table = db["jobads"]

print(table.schema)
