from pydoc import doc
from typing import overload
from account.fire_store import FirebaseClient


class ProductClient(FirebaseClient):

    def __init__(self):
        FirebaseClient.__init__(self, "Medicines")

    def create(self, data, name):
        """Create todo in firestore database"""
        doc_ref = self._collection.document(name)
        doc_ref.set(data)
