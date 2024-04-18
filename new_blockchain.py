import hashlib
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # 创建创世区块
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        创建一个新的区块并将其添加到链上
        :param proof: 由工作量证明算法生成的证明
        :param previous_hash: 前一个区块的hash值
        :return: 新的区块
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # 重置当前交易列表
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        创建一个新的交易并添加到下一个待挖的区块中
        :param sender: 交易发送方的地址
        :param recipient: 交易接收方的地址
        :param amount: 交易金额
        :return: 包含交易信息的下一个待挖的区块的索引
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        生成区块的 SHA-256 hash值
        :param block: 区块
        :return: hash值
        """
        # 确保字典是有序的，否则会导致hash不一致
        block_string = str(block)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def proof_of_work(self, last_proof):
        """
        简单的工作量证明算法：
        - 查找一个数p，使得hash(pp')以4个0开头，其中p是上一个区块的proof，p'是当前的proof
        - p是上一个区块的proof，p'是当前的proof
        :param last_proof: 上一个区块的proof
        :return: 当前的proof
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        验证proof是否满足要求：hash(last_proof, proof)以4个0开头
        :param last_proof: 上一个区块的proof
        :param proof: 当前的proof
        :return: True如果满足要求，否则False
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# 测试
if __name__ == '__main__':
    # 创建一个区块链
    blockchain = Blockchain()

    # 添加一些交易到下一个待挖的区块
    blockchain.new_transaction("Alice", "Bob", 1)
    blockchain.new_transaction("Bob", "Charlie", 2)

    # 挖掘一个新的区块
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # 得到一个有效的proof后，为了完成挖掘，我们需要给工作量证明者一定的奖励。
    # 发送者为 "0" 表示是由系统生成的新币
    blockchain.new_transaction(
        sender="0",
        recipient="Miner Address",
        amount=1,
    )

    # 构造新区块并将其添加到区块链中
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    # 输出区块链
    print(blockchain.chain)