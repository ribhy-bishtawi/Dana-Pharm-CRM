from pydoc import doc
from account.fire_store import FirebaseClient


class NablusClient(FirebaseClient):

    def __init__(self):
        FirebaseClient.__init__(self, "NablusOrders")

    def getItems(self, docId):
        docs = self._collection.document(docId).collection("items").stream()
        return [{**doc.to_dict(), "id": doc.id} for doc in docs]

    def deleteSubCollection(self, docId):
        docs = self._collection.document(docId).collection("items").stream()
        for doc in docs:
            doc.reference.delete()
