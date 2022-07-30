from pydoc import doc
from account.fire_store import FirebaseClient


class OrderClient(FirebaseClient):

    def __init__(self):
        FirebaseClient.__init__(self, "orders")

    def getItems(self, docId):
        docs = self._collection.document(docId).collection("items").stream()
        return [{**doc.to_dict(), "id": doc.id} for doc in docs]
