from hashlib import sha256
from time import time

from blockchain_types import BlockObject
from users import DataBase


class Blockchain:
    def __init__(self):
        self.db = DataBase()
        self.chain = self.db.get_chain()

    def get_last_block(self):
        block = self.chain[len(self.chain) - 1]
        block_data = {"sender": block[0],
                      "recipient": block[1],
                      "amount": block[2],
                      "hash": block[3],
                      "prev_hash": block[4],
                      "timestamp": block[5]}

        block = BlockObject(block_data)

        return block

    def add_block(self, block):
        print(self.db.blockchain_update(block))
        self.chain = self.db.get_chain()

    def is_valid(self):
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            prevBlock = self.chain[i - 1]

            if (currentBlock.hash != currentBlock.getHash() or prevBlock.hash != currentBlock.prevHash):
                return False

        return True

    def __call__(self):
        return self.chain

    def __repr__(self):
        try:
            block = self.getLastBlock()
        except:
            block = {}
        return repr(block)


class Block:
    def __init__(self,
                 chain: Blockchain,
                 sender: str = "",
                 recipient: str = "",
                 amount: int = 0):
        self.timestamp = time()
        self.prevHash = chain.getLastBlock().hash
        self.nonce = 0

        self.data = {"sender": sender,
                     "recipient": recipient,
                     "amount": amount}

        self.hash = self.get_hash()

        self.block = {"sender": sender,
                      "recipient": recipient,
                      "amount": amount,
                      "hash": self.hash,
                      "prev_hash": self.prevHash,
                      "timestamp": self.timestamp}

        self.block = BlockObject(self.block)

    def get_hash(self):
        hash = sha256()
        hash.update(str(self.prevHash).encode('utf-8'))
        hash.update(str(self.timestamp).encode('utf-8'))
        hash.update(str(self.data).encode('utf-8'))
        hash.update(str(self.nonce).encode('utf-8'))
        return hash.hexdigest()

    def mine(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.get_hash()

    def __repr__(self):
        return repr(self.block)


blockchain = Blockchain()
print(blockchain.getLastBlock())
block = Block(blockchain, "Anton", "NikVas", 100)
print(block.block)
print(blockchain.add_block(block.block))
print(blockchain.get_last_block())