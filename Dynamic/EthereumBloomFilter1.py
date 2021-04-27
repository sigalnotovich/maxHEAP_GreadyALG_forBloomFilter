#!/usr/bin/env python
# coding: utf-8

# # BASIC CODE OF THE ETHEREUM BLOOM FILTER IMPLEMENTATION

# In[4]:
import glob
import numbers
# from numba import jit, cuda
# The Ethereum hashing function, keccak256, sometimes (erroneously) called sha3 from:
# https://eth-hash.readthedocs.io/en/latest/index.html
from eth_hash.auto import keccak as keccak_256


# THIS NOTEBOOK IMPLEMENTS AN ETHEREUM BLOOM FILTER AS DESCRIBED IN THE ETHEREUM YELLOW PAPER
# THE MAIN CLASS IS BLOOM FILTER

def get_bloom_bits(value):  # value is in hex
    transactionHash = keccak_256(bytearray.fromhex(value))
    mask1 = 0b11111111
    mask2 = 0b111
    res = []
    for i in range(3):
        res.append(((mask2 & transactionHash[i]) << 8) + (mask1 & transactionHash[i + 1]))
    return res


# A Bloom Filter is a 2048 bits (256 bytes) array initialized with zeros
# Each transaction entered to the Bloom Filter lights up 3 bits according to the ethereum rule:
# "through taking the low-order 11 bits of each of the first three pairs of bytes in a Keccak-256 hash of the byte sequence"
class BloomFilter(numbers.Number):
    value = None  # type: int
    transaction_number = 0

    def __init__(self, value: int = 0) -> None:
        self.value = value

    def __int__(self) -> int:
        return self.value

    def __hash__(self) -> int:  # get the hash of the bloom filter
        return hash(self.value)

    def add(self, value: bytes):
        open_bits = get_bloom_bits(value)
        print("This transaction will light up these following bits:", open_bits)
        for bit in open_bits:
            self.value |= (1 << bit)

    def printBF(self):
        print(bin(self.value))

    def openBits(self):
        return bin(self.value).count("1")


# # USE EXAMPLE

# In[5]:


# In this example we create an empty bloom filter and add 2 random transactions to this filter
# the transactions hash were taken randomly from etherscan.io website
bloomFilter = BloomFilter()
transaction1 = '68cc7a1d83f9aee1b3af7adc85b1ee5614a4ebf9a4c19409f05bfbfbe79deddf'
transaction2 = '8211a7f9fa4608f2d0229a18472504a59e6b4fec56f44ec1faba00a6ad5d25de'
transaction3 = '1773ccf96888d46f5aa16dfbd5326df6c0d6c0f6492090f2cfc45bd140832020'

print("Add transaction1:")
bloomFilter.add(transaction1)
print("The resulting Bloom Filter is:")
bloomFilter.printBF()
print("Add transaction2:")
bloomFilter.add(transaction2)
print("The resulting Bloom Filter is:")
bloomFilter.printBF()

# # Example with real values from etherscan.io
# ## From a cvs file we read all the transaction hash and then enter each transaction in the bloom filter

# In[ ]:


import pandas as pd

# csv_file = "bq-results-20210403-184904-hannuasg1nco.csv"


transactions_hash = []
files = [f for f in glob.glob("./*.csv")]

cnt = 0
for csv_file in files:
    data = pd.read_csv(csv_file)
    for line in data['hash']:
        cnt += 1
        if cnt < 20:
            transactions_hash.append(line[2:])

# print(transactions_hash)


# In[7]:


bloomFilter = BloomFilter()
print(bloomFilter.openBits())
for transaction in transactions_hash:
    print(transaction)
    print(bloomFilter.openBits())
    bloomFilter.add(transaction)

bloomFilter.printBF()
print("Number of bits that are light up in the bloomFilter:", bloomFilter.openBits())

# # Implementation of dynamic programing algorithm

# In[ ]:


import numpy
import sys

m = len(transactions_hash)  # number of transactions in the mempool
# n = 166  # number of taken transactions

N = 10

hashed_bits = {}
for idx, transaction in enumerate(transactions_hash):
    hashed_bits[transaction] = get_bloom_bits(transaction)

lighted_bit = numpy.empty((m, m), dtype=numpy.ndarray)
print(lighted_bit.shape)
for i in range(m):
    for j in range(m):
        lighted_bit[i][j] = []


def check_new(i, n):
    new_bits = get_bloom_bits(transactions_hash[i])
    txn_bits = []
    for bit in new_bits:
        if not numpy.isin(bit, lighted_bit[i][n]):
            txn_bits.append(bit)
    return txn_bits


def t(i, n):
    if n == N:
        return 0
    if i == m:
    # print("end i == m")
        return sys.maxsize
    new_bits = check_new(i, n)
    num_bits = len(new_bits)
    for bit in new_bits:
        lighted_bit[i][n].append(bit)
    print(lighted_bit[i][n])
    if num_bits == 0:
        return min(t(i+1, n), t(i + 1, n+1))
    elif num_bits == 1:
        return min(t(i+1, n), t(i + 1, n+1) + 1)
    elif num_bits == 2:
        return min(t(i+1, n), t(i + 1, n+1) + 2)
    elif num_bits == 3:
        return min(t(i+1, n), t(i + 1, n+1) + 3)


def __main__():
    result = t(0, 0)
    print("finished")
    print(result)


if __name__ == '__main__':
    __main__()
