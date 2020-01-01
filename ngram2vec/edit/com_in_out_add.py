import codecs
import os, sys
import numpy as np
path = sys.path[0]
os.chdir(path)

with open("com_dict.txt","r",encoding="utf8") as f:
    com_line_list = []
    char_com_dict = {}
    for line in f:
        com_line_list.append(line.strip().rstrip("\n").split())
    for line_list in com_line_list:
        if len(line_list) > 2:
            if len(line_list) == 3:
                char_com_dict[line_list[0]] = [line_list[1]]
            if len(line_list) == 5:
                char_com_dict[line_list[0]] = [line_list[1],line_list[3]]
            if len(line_list) == 7:
                char_com_dict[line_list[0]] = [line_list[1],line_list[3],line_list[5]]
            if len(line_list) == 9:
                char_com_dict[line_list[0]] = [line_list[1],line_list[3],line_list[5],line_list[7]]


with open("sgns.input","r",encoding="utf8") as f:
    input_vec_dict = {}
    first_line_input = f.readline()
    for line in f:
        if line == first_line_input:
            continue
        char_vec_line_list = line.rstrip("\n").strip(" ").split(" ")
        input_vec_array = np.zeros((1,300))
        input_vec_array[0] += np.array(char_vec_line_list[1:]).astype("float64")
        input_vec_dict[char_vec_line_list[0]] = input_vec_array 

with open("sgns.output","r",encoding="utf8") as f:
    output_vec_dict = {}
    first_line_output = f.readline()
    for line in f:
        if line == first_line_output:
            continue
        char_vec_line_list = line.rstrip("\n").strip(" ").split(" ")
        output_vec_array = np.zeros((1,300))
        output_vec_array[0] += np.array(char_vec_line_list[1:]).astype("float64")
        output_vec_dict[char_vec_line_list[0]] = output_vec_array


word_coms_dict = {}

for char, coms in char_com_dict.items():
    for word in input_vec_dict.keys():
        if char in word:
            if word not in word_coms_dict.keys():
                word_coms_dict[word] = []
            word_coms_dict[word].extend(coms)

for word, coms in word_coms_dict.items():
    if word in input_vec_dict.keys():
        coms_vec_mean = np.zeros((1,300)) 
        for com in coms:
            coms_vec_mean += output_vec_dict[com]
        coms_vec_mean = coms_vec_mean / len(coms)
        input_vec_dict[word] = (input_vec_dict[word] + coms_vec_mean) / 2

for word, vec in output_vec_dict.items():
    if word in input_vec_dict.keys():
        input_vec_dict[word] = (input_vec_dict[word] + output_vec_dict[word]) / 2

fw = codecs.open("com_in_out.add","a","utf8")
fw.write(first_line_input)
for word , vec in input_vec_dict.items():
    fw.write(word+" ")
    np.savetxt(fw ,vec, fmt='%.8f')
fw.close()
    
        


