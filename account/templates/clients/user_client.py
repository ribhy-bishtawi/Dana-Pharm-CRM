from account.fire_store import FirebaseClient


class UserClient(FirebaseClient):

    def __init__(self):
        FirebaseClient.__init__(self, "Users")
