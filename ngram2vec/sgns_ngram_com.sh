#!/bin/bash
memory_size=50
cpus_num=32
corpus=chinesegigawordv5_text.txt.jian.hanlp.seg
output_path=outputs/${corpus}/word_word

mkdir -p ${output_path}/sgns

echo "step 1: Create corpus vocab"
echo "____________________________________________"
python ngram2vec/corpus2vocab.py --corpus_file ${corpus} --vocab_file ${output_path}/vocab --memory_size ${memory_size} --feature word --order 1
echo "_____________________done___________________"

echo "step 2: Create input & output pairs"
echo "____________________________________________"
python ngram2vec/corpus2pairs.py --corpus_file ${corpus} --pairs_file ${output_path}/pairs --vocab_file ${output_path}/vocab --processes_num ${cpus_num} --cooccur word_word --input_order 1 --output_order 1 --win 2
echo "_____________________done___________________"

echo "step 3: Concatenate pair files. "
echo "____________________________________________"
# Concatenate pair files. 
if [ -f "${output_path}/pairs" ]; then
	rm ${output_path}/pairs
fi
for i in $(seq 0 $((${cpus_num}-1)))
do
	cat ${output_path}/pairs_${i} >> ${output_path}/pairs
	rm ${output_path}/pairs_${i}
done
echo "_____________________done___________________"

echo "step 4: Add coms to pairs"
echo "____________________________________________"
cp -r ./edit ${output_path}
python ${output_path}/edit/pair_add_com.py
echo "_____________________done___________________"

echo "step 5: Generate input vocabulary and output vocabulary, which are used as vocabulary files for all models"
echo "____________________________________________"
python ngram2vec/pairs2vocab.py --pairs_file ${output_path}/pairs --input_vocab_file ${output_path}/vocab.input --output_vocab_file ${output_path}/vocab.output
echo "_____________________done___________________"

# SGNS, learn representation upon pairs.
echo "step 6: SGNS, learn representation upon pairs."
echo "____________________________________________"
# We add a python interface upon C code.
python ngram2vec/pairs2sgns.py --pairs_file ${output_path}/pairs --input_vocab_file ${output_path}/vocab.input --output_vocab_file ${output_path}/vocab.output --input_vector_file ${output_path}/sgns/sgns.input --output_vector_file ${output_path}/sgns/sgns.output --threads_num ${cpus_num} --size 300
echo "_____________________done___________________"

echo "step 7: Evaluation on Analogy Task"
echo "____________________________________________"
cp -r ./Chinese-Word-Vectors ${output_path}/sgns/
python ${output_path}/sgns/Chinese-Word-Vectors/evaluation/ana_eval_dense.py -v ${output_path}/sgns/sgns.input -a ${output_path}/sgns/Chinese-Word-Vecotrs/testsets/CA8/semantic.txt
python ${output_path}/sgns/Chinese-Word-Vectors/evaluation/ana_eval_dense.py -v ${output_path}/sgns/sgns.input -a ${output_path}/sgns/Chinese-Word-Vecotrs/testsets/CA8/morphological.txt
echo "__________________all_done!_________________"
