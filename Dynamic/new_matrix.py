import numpy
import pandas as pd

from eth_hash.auto import keccak as keccak_256
NUM_OF_BITS_IN_BLOOM_FILTER = 2048

def get_bloom_bits(value):#value is in hex
    transactionHash = keccak_256(bytearray.fromhex(value))
    mask1 = 0b11111111
    mask2 = 0b111
    res = []
    for i in range(3):
        res.append((( mask2 & transactionHash[i] ) << 8) + (mask1 & transactionHash[i+1]))
    return res


def get_trx_filter_bits(value: bytes):
    open_bits = get_bloom_bits(value)
    #print("This transaction will light up these following bits:", open_bits)
    return open_bits


def add_edge_from_bits_to_trx_that_light_them(data, C_new ):
    # get trx_bits
    transactions_hash = []

    for hash,index in zip(data['hash'],data['transaction_index']):
        transactions_hash.append((hash[2:],index))

    for transaction,index in transactions_hash:
        trx_filter_bits = get_trx_filter_bits(transaction)
        # enter the corresponding edges to bits:
        for bit in trx_filter_bits:
            C_new[NUM_OF_BITS_IN_BLOOM_FILTER + bit][NUM_OF_BITS_IN_BLOOM_FILTER + NUM_OF_BITS_IN_BLOOM_FILTER + index ] = 1
    return C_new


def make_new_matrix(nam_trx_in_current_block, data, number_of_trx_in_new_block):
    C_new = []
    arraylen = 1 + NUM_OF_BITS_IN_BLOOM_FILTER + NUM_OF_BITS_IN_BLOOM_FILTER + nam_trx_in_current_block + 1 + 1  #1 for s and  1 + 1 for t and t'
    # first line of mettrix - all the edges from s to the 2048 bits
    array0 = []
    array0.append(0) #for s
    #from s to all the src stream 1
    for i in range(1, NUM_OF_BITS_IN_BLOOM_FILTER + 1):  # till NUM_OF_BITS_IN_BLOOM_FILTER
        array0.append(1)
    #for the bits:
    for i in range(1, NUM_OF_BITS_IN_BLOOM_FILTER + 1):
        array0.append(0)
    #for the trx
    for i in range(1, nam_trx_in_current_block + 1):  # till num_trx_in_block
        array0.append(0)
    array0.append(0)  # for t
    array0.append(0)  # for t'

    C_new.append(array0)

    # all other lines of the metrix now initialized with zeros
    for i in range(1, arraylen ):  # we allready did 1 line  - now we need the rest
        C_new.append([0] * arraylen)

    # from src i add edge with flow 1 to bit i:
    for i in range (1,NUM_OF_BITS_IN_BLOOM_FILTER + 1):
        C_new[i][NUM_OF_BITS_IN_BLOOM_FILTER + i] = 1

    # from bit1 to bit 2048 for each of them add the edges to the correct trx:
    C_new = add_edge_from_bits_to_trx_that_light_them(data, C_new)

    # from trx1 ... trxN make edge with capacity 3:
    for i in range(1, nam_trx_in_current_block + 1):
        row1 = NUM_OF_BITS_IN_BLOOM_FILTER + NUM_OF_BITS_IN_BLOOM_FILTER + i
        col1 = NUM_OF_BITS_IN_BLOOM_FILTER + NUM_OF_BITS_IN_BLOOM_FILTER + nam_trx_in_current_block + 1
        C_new[row1][col1] = 3

    #from t to t' stream number_of_trx_in_new_block * 3
    row2 = NUM_OF_BITS_IN_BLOOM_FILTER + NUM_OF_BITS_IN_BLOOM_FILTER + nam_trx_in_current_block + 1
    col2 = NUM_OF_BITS_IN_BLOOM_FILTER + NUM_OF_BITS_IN_BLOOM_FILTER + nam_trx_in_current_block + 1 + 1
    C_new[row2][col2] = 3 * number_of_trx_in_new_block

    C_nuw_print = numpy.array(C_new)
    # print(C_nuw_print)
    # numpy.savetxt("foo.csv", C_nuw_print, delimiter=",")
    # input()
    return C_new,arraylen


def new_matrix(csv_file,number_of_trx_in_new_block):
    data = pd.read_csv(csv_file)
    nam_tax_in_current_block = len(data.index)
    C_new,arraylen = make_new_matrix(nam_tax_in_current_block, data , number_of_trx_in_new_block)
    return C_new,nam_tax_in_current_block,arraylen
