this project - has two inner projects:
first is a python project and second is a c++ project,
the greedy_algorthm is python project, and the max heap is c++ project.
project input: blocks of Etherum
project will buid a mem pool with all the blocks it resived and will give you blocks with samller amout of bloom filter bits-by difault give only one block.

for getting the results follow the following steps:
1.insert to the greedy_algorithm/first_input folder all the blocks csv you want to make a mempool for
and update it in the EthereumBloomFilter.py 
2.run the greedy_algorithm project
3.take the files from greedy_algorithm/first_output folder and put it in max_heap folder
4.run the max_heap project
5.from max_heap folder copy the new_block_output.csv file and past it to greedy_algoritm\second_input
6.run the greedy_algorithm program
7.in the greedy_algorithm/final_output you will find the first_step_block_graph_output.csv and the second_step_block_graph_output.csv:
in first_step_block_graph_output.csv  contain the data of the original blocks - how many transaction was ther and how many bloom filter
bits where on.
and in the second_step_block_graph_output.csv you can find the final block with the new numbers of bits turned on in the bloom filter after
choosing the transactions using the max_heap_greedy_algorithm

hope you enjoy this project
updates will come if needed