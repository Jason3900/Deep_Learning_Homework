import codecs
import os, sys
import numpy as np
path = sys.path[0]
os.chdir(path)

with open("../sgns.input","r",encoding="utf8") as f:
    input_vec_dict = {}
    first_line_input = f.readline()
    for line in f:
        if line == first_line_input:
            continue
        word_vec_line_list = line.rstrip("\n").strip(" ").split(" ")
        input_vec_array = np.zeros((1,300))
        input_vec_array[0] += np.array(word_vec_line_list[1:]).astype("float64")
        input_vec_dict[word_vec_line_list[0]] = input_vec_array 

with open("../sgns.output","r",encoding="utf8") as f:
    output_vec_dict = {}
    first_line_output = f.readline()
    for line in f:
        if line == first_line_output:
            continue
        word_vec_line_list = line.rstrip("\n").strip(" ").split(" ")
        output_vec_array = np.zeros((1,300))
        output_vec_array[0] += np.array(word_vec_line_list[1:]).astype("float64")
        output_vec_dict[word_vec_line_list[0]] = output_vec_array

for word, vec in output_vec_dict.items():
    if word in input_vec_dict.keys():
        input_vec_dict[word] = (input_vec_dict[word] + output_vec_dict[word]) / 2

fw = codecs.open("../in_out.add","a","utf8")
fw.write(first_line_input)
for word , vec in input_vec_dict.items():
    fw.write(word+" ")
    np.savetxt(fw ,vec, fmt='%.8f')
fw.close()
    
        


