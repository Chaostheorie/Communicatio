import elasticsearch

from app import app
from app.models import entrys, terms
from app.mixin import add_to_index

entrys.reindex()
terms.reindex()

print("add elasticsearch index")
