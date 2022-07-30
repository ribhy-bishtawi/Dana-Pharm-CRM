from account.fire_store import FirebaseClient


class IndexClient(FirebaseClient):

    def __init__(self):
        FirebaseClient.__init__(self, "MyIndex")
