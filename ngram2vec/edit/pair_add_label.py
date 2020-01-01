import sys
import os 
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
                char_com_dict[line_list[0]] = [line_list[1]+line_list[2]]
            if len(line_list) == 5:
                char_com_dict[line_list[0]] = [line_list[1]+line_list[2],line_list[3]+line_list[4]]
            if len(line_list) == 7:
                char_com_dict[line_list[0]] = [line_list[1]+line_list[2],line_list[3]+line_list[4],line_list[5]+line_list[6]]
            if len(line_list) == 9:
                char_com_dict[line_list[0]] = [line_list[1]+line_list[2],line_list[3]+line_list[4],line_list[5]+line_list[6],line_list[7]+line_list[8]]
print("step 1: char_com_dict build______________done!")

with open("../vocab.input_ori","r") as f:
    word_set = set()
    for idx, line in enumerate(f):
        word_set.add(line.strip().rstrip("\n").split(" ")[0])
        if str(idx).endswith("0000"):
            print(len(word_set))
print("step 2: read word_list______________done!")

with open("../pairs_with_labeled","w") as fw:
    word_ngram_dict = {}
    for keyword in word_set:
        if keyword not in word_ngram_dict.keys():
            word_ngram_dict[keyword] = []
    for word, ngrams in word_ngram_dict.items():
        for char, coms in char_com_dict.items():
            if char in word:
                ngrams.extend(coms)
    for k,v in word_ngram_dict.items():
        for i in v:
            fw.write(f"{k} {i}\n")
