class BlockObject:
    def __init__(self, data: dict | list):
        self.data = data

        if type(self.data) == type({"!": 1}):
            self.sender = data.get("sender")
            self.recipient = data.get("recipient")

            self.amount = data.get("amount")

            self.hash = data.get("hash")
            self.prev_hash = data.get("prev_hash")

            self.timestamp = data.get("timestamp")
        if type(self.data) == type([1, 2]):
            self.data = {"sender": data[0],
                         "recipient": data[1],
                         "amount": data[2],
                         "hash": data[3],
                         "prev_hash": data[4],
                         "timestamp": data[5]}
            self.sender = data[0]
            self.recipient = data[1]

            self.amount = data[2]

            self.hash = data[3]
            self.prev_hash = data[4]

            self.timestamp = data[5]

    def __repr__(self):
        return repr(self.data)


class UserObject:
    def __init__(self, data: dict | list):
        self.data = data

        if type(self.data) == type({"!": 1}):
            self.hash = self.data.get("hash")
            self.balance = self.data.get("balance")
        if type(self.data) == type([1, 2]):
            self.hash = self.data[0]
            self.balance = self.data[0]

            self.data = {"hash": data[0],
                         "balance": data[1]}

    def __repr__(self):
        return repr(self.data)
