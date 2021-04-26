#include <iostream>
#include <vector>
#include <algorithm>
#include <stdexcept>
#include <fstream>
#include <tuple>
#include <set>
#include <assert.h>
#include <sstream>
#include <string>

using namespace std;

enum heap_state {empty_heap, not_empty_heap};
enum son_place {first,second};

struct Test{
    int bit_num;
    int times_accured;
};

class test_class{
public:
    static std::vector<int> bits_acuurancy_vector_after_tree_poping;
    static std::vector<int> bits_acuurancy_vector_in_input_file;

};
std::vector<int> test_class::bits_acuurancy_vector_after_tree_poping = std::vector<int>(2048, 0);
std::vector<int> test_class::bits_acuurancy_vector_in_input_file = std::vector<int>(2048, 0);

struct HeapElement {
    double value; // todo : change to: num_accurancies
    double bit_num;
    HeapElement* parent;
    HeapElement* child1;
    HeapElement* child2;

    inline bool operator==(HeapElement a) {
        if (a.child2 == child2 && a.child1 == child1 && a.parent == parent)
            return true;
        else
            return false;
    }
};

class Heap {
    HeapElement* head;
public:
    Heap();
    ~Heap();
    HeapElement* insert(int d,int bit_num); // inserts value d into the heap
    HeapElement* top(); // returns the smallest element
    heap_state pop_top(); // removes the smallest element
    void update_element(HeapElement* d, bool is_rec);
    void after_pop_insert_leaf_to_right_place(HeapElement* elem);
    void swap_father_and_son(HeapElement* son);
};

Heap::Heap(){
    head = NULL;
}

Heap::~Heap(){
    while (head != NULL){
        pop_top();
    }
}
HeapElement* Heap::top(){ // returns the smallest element
    if (head != NULL){
        return head;
    }
    else{
        cout << "empty heap" << endl;
        return nullptr;
    }

}

HeapElement* Heap::insert(int d, int bit_num){// inserts value d into the heap
    HeapElement* freepos = new HeapElement;
    if (head == NULL) {
        head = new HeapElement;
        head->value = (-1) * d;
        head->bit_num = bit_num;
        head->parent = NULL;
        head->child1 = NULL;
        head->child2 = NULL;
        return head;
    }
    else{
        HeapElement* freepos_parent = head;
        //    HeapElement* freepos = new HeapElement;
        double temp;

        //find the parent of a free position and then insert value d to this positon(a node that that has less than 2 childrend.)
        while (freepos_parent->child1 != NULL && freepos_parent->child2 != NULL){
            if (rand() % 2 == 0){
                freepos_parent = freepos_parent->child1;
            }
            else{
                freepos_parent = freepos_parent->child2;
            }
        }

        //if left child is NULL then insert to left child, else insert to right child.
        if (freepos_parent->child1 == NULL){
            freepos_parent->child1 = freepos;
        }
        else{
            freepos_parent->child2 = freepos;
        }
        //insert the new value to the position freepos.
        freepos->parent = freepos_parent;
        freepos->value = (-1) * d;
        freepos->bit_num = bit_num;
        freepos->child1 = NULL;
        freepos->child2 = NULL;

        while (freepos_parent!=NULL && freepos_parent->value > freepos->value){
            //swap the value
            temp = freepos_parent->value;
            freepos_parent->value = freepos->value;
            freepos->value = temp;
            //set to one level higher
            freepos = freepos_parent;
            freepos_parent = freepos->parent;
        }
    }
    return freepos;
}

heap_state Heap::pop_top(){ // removes the smallest element
    if (head == NULL){
        cout << "The heap is already empty." << endl;
        return empty_heap;
    }
    else if (head->child1 == NULL && head->child2 ==NULL){
        delete head;
        head = NULL;
        return empty_heap;
    }
    else{
        HeapElement* leaf =  head;
        //find a leaf node
        while (leaf->child1 != NULL || leaf->child2 != NULL){ //if it has child
            if (leaf->child1 != NULL && leaf->child2 != NULL){ //if has two children
                if (rand() % 2 == 0){
                    leaf = leaf->child1;
                }
                else{
                    leaf = leaf->child2;
                }
            }
            else if (leaf->child1 != NULL){
                leaf = leaf->child1;
            }
            else{ leaf = leaf->child2; }
        }

        //cut the leaf
        if (leaf == leaf->parent->child1){
            leaf->parent->child1 = NULL;
        }
        else{
            leaf->parent->child2 = NULL;
        }

        //change head to the leaf
        leaf->parent = NULL;
        leaf->child1 = head->child1;
        leaf->child2 = head->child2;

        // change the parents of childs of previous head
        if (head->child1 != NULL){
            head->child1->parent = leaf;
        }
        if (head->child2 != NULL){
            head->child2->parent = leaf;
        }

        delete head;
        head = leaf;
        //swap
        HeapElement* small_child = new HeapElement;
        double temp;
        bool flag = true;
        while ((leaf->child1 != NULL || leaf->child2 != NULL) && flag ==true) {
            if (leaf->child1 != NULL ){
                small_child = leaf->child1;
                if (leaf->child2 != NULL && leaf->child2->value < leaf->child1->value){
                    small_child = leaf->child2;
                }
            }
            else{ small_child = leaf->child2; }
            if (leaf->value > small_child->value){
                swap_father_and_son(small_child);
            }
            else{
                flag = false;
            }
        }
        return not_empty_heap;
    }
    return not_empty_heap;
}

//void Heap::after_pop_insert_leaf_to_right_place(HeapElement* elem){
//    if(elem->value > elem->child1->value || elem->value > elem->child2->value )
//        if(elem->value > elem->child1->value ){
//            swap_father_and_son(elem->child1);
//        }
//        if(elem->value > elem->child2->value ){
//            swap_father_and_son(elem->child2);
//        }
//}
//void Heap::pop_top(){ // removes the smallest element
//    if (head == NULL){
//        cout << "The heap is already empty." << endl;
//    }
//    else if (head->child1 == NULL && head->child2 ==NULL){
//        delete head;
//        head = NULL;
//    }
//    else{
//        HeapElement* leaf =  head;
//        //find a leaf node
//        while (leaf->child1 != NULL || leaf->child2 != NULL){ //if it has child
//            if (leaf->child1 != NULL && leaf->child2 != NULL){ //if has two children
//                if (rand() % 2 == 0){
//                    leaf = leaf->child1;
//                }
//                else{
//                    leaf = leaf->child2;
//                }
//            }
//            else if (leaf->child1 != NULL){
//                leaf = leaf->child1;
//            }
//            else{ leaf = leaf->child2; }
//        }
//
//        //cut the leaf
//        if (leaf == leaf->parent->child1){
//            leaf->parent->child1 = NULL;
//        }
//        else{
//            leaf->parent->child2 = NULL;
//        }
//
//        //change head to the leaf
//        leaf->parent = NULL;
//        leaf->child1 = head->child1;
//        leaf->child2 = head->child2;
//
//        // change the parents of childs of previous head
//        if (head->child1 != NULL){
//            head->child1->parent = leaf;
//        }
//        if (head->child2 != NULL){
//            head->child2->parent = leaf;
//        }
//
//        delete head;
//        head = leaf;
//        //swap
//        HeapElement* small_child = new HeapElement;
//        double temp;
//        while (leaf->child1 != NULL || leaf->child2 != NULL){
//            if (leaf->child1 != NULL){
//                small_child = leaf->child1;
//                if (leaf->child2 != NULL && leaf->child2->value < leaf->child1->value){
//                    small_child = leaf->child2;
//                }
//            }
//            else{ small_child = leaf->child2; }
//            if (leaf->value > small_child->value){
//                temp = small_child->value;
//                small_child->value = leaf->value;
//                leaf->value = temp;
//            }
//            leaf = small_child;
//        }
//
//    }
//
//}

//son
//father = son->parent
void Heap::swap_father_and_son(HeapElement* son){

        HeapElement* cur_child1_of_son = son->child1;
        HeapElement* cur_child2_of_son = son->child2;

        HeapElement* cur_father_of_father = son->parent->parent;
        HeapElement* cur_child2_of_father = nullptr;
        son_place elems_fathers_father_son_place;
        HeapElement* cur_elem_father = son->parent;

        if ((son->parent->child1) == (son)) { //todo
            cur_child2_of_father = son->parent->child2;
            //cout << "first child";
        }
        else{
            cur_child2_of_father = son->parent->child1;
            //cout << "second child";
        }

        if (son->parent == head){
            head = son;
            head->parent = nullptr;
            son->child1 = cur_elem_father;
            son->child2 = cur_child2_of_father;
            cur_elem_father->parent = son;
            if (cur_child2_of_father != nullptr){
                cur_child2_of_father->parent = son;
            }
            cur_elem_father->child1 = cur_child1_of_son;
            if (cur_child1_of_son != nullptr){
                cur_child1_of_son->parent = cur_elem_father;
            }

            cur_elem_father->child2 = cur_child2_of_son;
            if (cur_child2_of_son != nullptr){
                cur_child2_of_son->parent = cur_elem_father;
            }
            //cur_elem_father->parent = head;
        }
        else {
            if (cur_father_of_father->child1 == cur_elem_father){
                elems_fathers_father_son_place = first;
            }
            else{
                elems_fathers_father_son_place = second;
            }

            son->parent = cur_father_of_father;
            son->child1 = cur_elem_father;

            cur_elem_father->parent = son;

            son->child2 = cur_child2_of_father;
            if (cur_child2_of_father != nullptr) {
                cur_child2_of_father->parent = son;
            }
            //cur_elem_father->parent = son;
            cur_elem_father->child1 = cur_child1_of_son;
            if (cur_child1_of_son != nullptr){
                cur_child1_of_son->parent = cur_elem_father;
            }
            cur_elem_father->child2 = cur_child2_of_son;
            if (cur_child2_of_son != nullptr){
                cur_child2_of_son->parent = cur_elem_father;
            }
            if (elems_fathers_father_son_place == first){
                cur_father_of_father->child1 = son;
            }
            else{
                cur_father_of_father->child2 = son;
            }
        }
        //swift father and sun


}

//until elems value smaller then elems_fathers value swap elem with father
void Heap::update_element(HeapElement* elem,bool is_rec = false){
    if (is_rec == false) {
        elem->value = elem->value - 1;
    }
    if (elem->parent != nullptr && elem->value < elem->parent->value) {
        swap_father_and_son(elem);
    }
     if (elem->parent != nullptr && elem->value < elem->parent->value) {
         update_element(elem, true);
     }
}

std::vector<int> func(vector<int> bits,vector<vector<int>>* vec) {
    vector<HeapElement*> array(2048, nullptr); //init array of size 2048 with nullptr in each cell
    Heap heap;
    for (int i = 0; i < bits.size(); i++) {
        int cur_bit = bits[i];
        if (array[cur_bit] == nullptr) { //bits never seen yet, therefore not counted in array
            //element* elem = new element(1, cur_bit);
            HeapElement* freepos = heap.insert(1,cur_bit);
            //array[cur_bit] = (element *) malloc(sizeof(elem));
            array[cur_bit] = freepos;
        } else {
            HeapElement *cur_elem = array[cur_bit];
            heap.update_element(cur_elem);//todo
        }
    }
    //print bits by number of accurancies first one accures the most

    HeapElement* a = heap.top();
    std::vector<int> final_trxes;
    std::set<int> trxes_set;
    vector<int> trxes = vec->at(a->bit_num);
    //cout << " most accured bit is: " << a->bit_num << " showed: " << (-1) * a->value <<" times" << endl;
    test_class::bits_acuurancy_vector_after_tree_poping[a->bit_num] = (-1) * a->value;
    trxes = vec->at(a->bit_num);
    for(std::vector<int>::iterator trx_hash = std::begin(trxes); trx_hash != std::end(trxes); ++trx_hash) {
        // std::cout << *trx_hash << "\n";
        //put trx_hash in a set
        //if find in set dont push if dont find push
        //trxes_set.find()
        trxes_set.insert(*trx_hash);
        final_trxes.push_back(*trx_hash);
    }

    heap_state heapState  = heap.pop_top();
    //todo: insert to vector
    while (heapState != empty_heap){
        a = heap.top();
        //cout << " bit number : " << a->bit_num << " showed: " << (-1) *  a->value <<" times" << endl;

        //for testing purposes:
        test_class::bits_acuurancy_vector_after_tree_poping[a->bit_num] = (-1) * a->value;

        trxes = vec->at(a->bit_num);
        for(std::vector<int>::iterator trx_hash = std::begin(trxes); trx_hash != std::end(trxes); ++trx_hash) {
           // std::cout << *trx_hash << "\n";
            //put trx_hash in a set
            if (trxes_set.find(*trx_hash) == trxes_set.end())
            {
                trxes_set.insert(*trx_hash);
                final_trxes.push_back(*trx_hash);
            }
//            trxes_set.insert(*trx_hash);
//            final_trxes.push_back(*trx_hash);
        }

        heapState = heap.pop_top();
    }
    return final_trxes;

}

//int rendare(){
//    vector<std::tuple<string,int>> indx_bit_tuples_vec;
//    fstream newfile;
//    newfile.open("Output.txt",ios::in);
//    if (newfile.is_open()){ //checking whether the file is open
//        string a;
//        int b;
//        int counter = 0;
//        bool flag = true;
//        getline(newfile,a);
//        getline(newfile,b);
//
//        while(getline(newfile, tp)){
//            if (counter == 0) {
//                a = tp;
//                counter += 1;
//            }
//            if (counter == 1) {
//                b = std::stoi(tp);
//                indx_bit_tuples_vec.push_back(tuple<string, int>(a, b));
//                counter = 0;
//            }
//
//        }
//    }
//}
struct Tuple{
    vector<string> trx_vector;
    vector<int> bits_vec;
};


void render2(vector<vector<int >>* vec,Tuple* tuple){
    vector<int> bits_vec;
    vector<string> trx_vector;
    string filename("hash_with_bit_nums_output.txt");
    string trx;
    int bit;

    ifstream input_file(filename);
    if (!input_file.is_open()) {
        cerr << "Could not open the file - '"
             << filename << "'" << endl;
    }
    bool flag = true;
    int counter = 0;
    while (flag == true) {
        if(!(input_file >> trx)){
            flag = false;
        }
        //cout<<trx<<endl;
        else {
            input_file >> bit;
//                cout << trx << endl;
//                cout << bit << endl;

            test_class::bits_acuurancy_vector_in_input_file[bit] += 1;
            bits_vec.push_back(bit);
            //push trx to the corect list:
            //make trx index vector: couse in the file we get 3 bits with the same hash one ofter the other
            if (counter % 3 == 0){
                trx_vector.push_back(trx);
            }

            vec->at(bit).push_back(counter/3);
            counter +=1;
        }
    }

    cout << endl;
    input_file.close();
    tuple->trx_vector = trx_vector;
    tuple->bits_vec = bits_vec;
}

void test(){
    for (int i = 0; i < 2048; ++i) {
        int a = test_class::bits_acuurancy_vector_in_input_file[i];
        int b = test_class::bits_acuurancy_vector_after_tree_poping[i];
        //cout << "bit num is: " << i << "and the difference are: he was " << a << " times in the input file and " << b << " times in the tree"<<endl;
        assert( a == b );
    }
}
//todo: i change final_trxes from vector of strings to vector of int
void makeNewBlocks(std::vector<int> final_trxes,vector<int> blocks_sizes,vector<string> trx_vector){
    //vector<string> file_names {"first_new_block.csv", "second_new_block.csv", "third_new_block.csv", "forth_new_block.csv", "fifth_new_block.csv", "six_new_block.csv","seven_new_block.csv","eight_new_block.csv","nine_new_block.csv","ten_new_block.csv"};
    std::ofstream myfile;
    myfile.open ("new_block_output.csv");
    myfile << "hash,block_number" << endl;
    std::ostringstream stream;
    int trx_indx_in_final_trx = 0;
    int final_trx_index; //
    for (int block_indx = 0; block_indx < blocks_sizes.size(); ++block_indx) {
        for (int j = 0; j < blocks_sizes[block_indx]; ++j) {
            //final_trx_index = final_trxes[trx_indx_in_final_trx];
            stream << trx_vector[final_trxes[trx_indx_in_final_trx]] << "," << block_indx ;
            //cout << stream.str() << endl;
            myfile << stream.str() << "\n";
            stream.str(std::string());
            trx_indx_in_final_trx += 1;
        }
    }
    myfile.close();
}

vector<int> get_block_sizes(){
    vector<int> blocks_sizes;
    string filename("output_block_size.txt");
    ifstream input_file(filename);
    int size;
    while((input_file >> size)){
        blocks_sizes.push_back(size);
    }
    return blocks_sizes;
}



int main(){
    //vector<int> blocks_sizes = {166,296,224,218,208};

    vector<int> blocks_sizes = get_block_sizes();
    vector<vector<int>>* vec = new vector<vector<int>>(2048);
    //vector<vector<string>> vec(2048);
    Tuple* tuple = new Tuple();
    render2(vec,tuple);
    vector<int> bits_vec = tuple->bits_vec;
    vector<string> trx_vector = tuple->trx_vector;
    //test_class::bits_acuurancy_vector_after_tree_poping[2] = 8;
    //only for check
    int counter = 0;
    for (int i = 0; i < bits_vec.size(); ++i) {
        if (bits_vec[i] == 40){
            counter +=1;
        }
    }
   // cout << "the conter of 40 is : " << counter << endl;
     //for test purposes:
    std::vector<int> final_trxes= func(bits_vec,vec);
    test();

    makeNewBlocks(final_trxes,blocks_sizes,trx_vector);

    return 0;
}
