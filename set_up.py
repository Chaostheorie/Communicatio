import elasticsearch

from app.models import entrys, terms

entrys.reindex()
terms.reindex()

print("Added/ refreshed elasticsearch index's")
