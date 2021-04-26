import numbers
import operator
from typing import (
    Iterable,
    Union,
    TYPE_CHECKING,
)

#THIS NOTEBOOK IMPLEMENTS AN ETHEREUM BLOOM FILTER AS DESCRIBED IN THE ETHEREUM YELLOW PAPER
#THE MAIN CLASS IS BLOOM FILTER


#The Ethereum hashing function, keccak256, sometimes (erroneously) called sha3 from:
#https://eth-hash.readthedocs.io/en/latest/index.html
from eth_hash.auto import keccak as keccak_256

def get_bloom_bits(value):#value is in hex
    transactionHash = keccak_256(bytearray.fromhex(value))
    mask1 = 0b11111111
    mask2 = 0b111
    res = []
    for i in range(3):
        res.append((( mask2 & transactionHash[i] ) << 8) + (mask1 & transactionHash[i+1]))
    return res


#A Bloom Filter is a 2048 bits (256 bytes) array initialized with zeros
#Each transaction entered to the Bloom Filter lights up 3 bits according to the ethereum rule:
#"through taking the low-order 11 bits of each of the first three pairs of bytes in a Keccak-256 hash of the byte sequence"
class BloomFilter(numbers.Number):
    value = None  # type: int
    transaction_number = 0
    
    def __init__(self, value: int = 0) -> None:
        self.value = value

    def __int__(self) -> int:
        return self.value

    def __hash__(self) -> int:#get the hash of the bloom filter
        return hash(self.value)


    def add(self, value: bytes,indx):
        open_bits = get_bloom_bits(value)
        #print("Transaction with index {0} will light up these following bits{1}".format(indx,open_bits))
        #print("{0} , {1}".format(indx,open_bits))
        for bit in open_bits:
            self.value |= (1<<bit)
        return open_bits
    
    def printBF(self):
        print(bin(self.value))
        
    def openBits(self):
        return bin(self.value).count("1")


import csv
import pandas as pd

def print_data(output_file_for_graphs_pd,block_size,block_num,bloomFilter,block_index):
    # print("------------------------------------------------------------------------------------")
    # print("block number: ", block_num)
    # print("number of trxes in block :", trx_indx)
    # print("bloom filters open bits:" ,bloomFilter.openBits())

    output_file_for_graphs_pd.at[block_index, 'num of trx'] = block_size
    output_file_for_graphs_pd.at[block_index, 'block num'] = block_num
    output_file_for_graphs_pd.at[block_index, 'num of bits in bloom filter before'] = bloomFilter.openBits()


def print_bits_and_filter_with_output_file(data, output_file_hash_and_bits, block_num,block_index, output_file_for_graphs_pd):
    transactions_hash = []
    for line in data['hash']:
        transactions_hash.append(line[2:])

    bloomFilter = BloomFilter()

    trx_indx = 0
    for transaction in transactions_hash:
        #print(transaction)
        open_bits = bloomFilter.add(transaction, trx_indx)
        for bit in open_bits:
            output_file_hash_and_bits.write("{0} \n".format(transaction))
            output_file_hash_and_bits.write("{0} \n".format(bit))

        trx_indx += 1

    print_data(output_file_for_graphs_pd,len(transactions_hash),block_num,bloomFilter,block_index)

    return trx_indx


def insert_to_output_file_from_one_csv(csv_file,output_file_hash_and_bits,output_file_for_graphs_pd,block_index ):
    data_hash_and_bits = pd.read_csv(csv_file)
    block_numbers_vec = data_hash_and_bits.block_number.unique()
    block_sizes = []
    for block_num in block_numbers_vec:
        one_block_data = data_hash_and_bits.loc[data_hash_and_bits['block_number'] == block_num]
        block_size = print_bits_and_filter_with_output_file(one_block_data, output_file_hash_and_bits,block_num,block_index,output_file_for_graphs_pd)
        block_index += 1
        block_sizes.append(block_size)
    return block_sizes,block_index

def first_step(csv_names,pool_size_precentage):
    output_file_hash_and_bits = open("first_output//hash_with_bit_nums_output.txt", "w")
    output_block_size = open("first_output//output_block_size.txt", "w")
    output_file_for_graphs_pd = pd.DataFrame(
        columns=['block num', 'num of trx','num of bits in bloom filter'])
    block_sizes = []
    block_index = 1
    for csv_name in csv_names:
        block_sixes_in_csv, block_index = insert_to_output_file_from_one_csv(csv_name,output_file_hash_and_bits,output_file_for_graphs_pd,block_index)
        block_sizes = block_sizes + block_sixes_in_csv
        number_of_blocks = len(block_sizes)

    output_block_size.write("{0} \n".format(block_sizes[len(block_sizes)-1]))
    # pool_size =  int(number_of_blocks * pool_size_precentage/100)
    # for i in range(number_of_blocks-pool_size,len(block_sizes)):
    #     output_block_size.write("{0} \n".format(block_sizes[i]))

    # for block_size in block_sizes:
    #     output_block_size.write("{0} \n".format(block_size))
    output_file_for_graphs_pd.to_csv('final_output//first_step_block_graph_output.csv')


def second_step():
    data_hash_and_bits = pd.read_csv("second_input//new_block_output.csv")
    output_file_for_graphs_pd = pd.DataFrame(
        columns=['block num', 'num of trx', 'num of bits in bloom filter before', 'num of bits in bloom filter  after'])
    block_numbers_vec = data_hash_and_bits.block_number.unique()
    #block_index = 0
    for block_num in block_numbers_vec:
        one_block_data = data_hash_and_bits.loc[data_hash_and_bits['block_number'] == block_num]
        print_otput_bloom_size(one_block_data, block_num,output_file_for_graphs_pd)
        #block_index += 1
    output_file_for_graphs_pd.to_csv('final_output//second_step_block_graph_output.csv')


def print_otput_bloom_size(data, block_num,output_file_for_graphs_pd):
    transactions_hash = []

    for line in data['hash']:
        transactions_hash.append(line[2:])

    bloomFilter = BloomFilter()

    for transaction in transactions_hash:
        # print(transaction)
        bloomFilter.add(transaction, 0)

    print_data(output_file_for_graphs_pd,len(transactions_hash),block_num,bloomFilter,block_num)


# # #
###csv_names_first_step =["first_input//first_big_csv.csv","first_input//second_big_csv.csv","first_input//input_pool1.csv","first_input//input_pool2.csv","first_input//input_pool3.csv","first_input//input_pool4.csv","first_input//input_pool5.csv","first_input//input_pool6.csv","first_input//input_pool7.csv"]
csv_names_first_step =["first_input//input_pool1.csv","first_input//input_pool2.csv","first_input//input_pool3.csv","first_input//input_pool4.csv","first_input//input_pool5.csv","first_input//input_pool6.csv","first_input//input_pool7.csv"]

#csv_names_first_step_add = ["first_input//input_pool8.csv","first_input//input_pool9.csv","first_input//input_pool10.csv","first_input//input_pool11.csv","first_input//input_pool12.csv","first_input//input_pool13.csv","first_input//input_pool14.csv"]
#csv_names_first_step_add2 = ["first_input//input_pool15.csv","first_input//input_pool16.csv","first_input//input_pool17.csv","first_input//input_pool18.csv","first_input//input_pool19.csv","first_input//input_pool20.csv","first_input//input_pool21.csv"]
#csv_names_first_step_add3 = ["first_input//input_pool22.csv","first_input//input_pool23.csv","first_input//input_pool24.csv","first_input//input_pool25.csv","first_input//input_pool26.csv","first_input//input_pool27.csv","first_input//input_pool28.csv"]
#csv_names_first_step_add4 =  ["first_input//input_pool29.csv","first_input//input_pool30.csv","first_input//input_pool31.csv","first_input//input_pool32.csv","first_input//input_pool33.csv","first_input//input_pool34.csv","first_input//input_pool35.csv"]
#csv_names_first_step_add5 =  ["first_input//input_pool36.csv","first_input//input_pool37.csv","first_input//input_pool38.csv","first_input//input_pool39.csv","first_input//input_pool40.csv","first_input//input_pool41.csv","first_input//input_pool42.csv"]

#csv_names_first_step = csv_names_first_step + csv_names_first_step_add + csv_names_first_step_add2 + csv_names_first_step_add3 + csv_names_first_step_add4 + csv_names_first_step_add5
first_step(csv_names_first_step,2)

second_step()

