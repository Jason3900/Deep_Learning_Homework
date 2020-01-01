#!/bin/bash
memory_size=50
cpus_num=32
corpus=chinesegigawordv5_text.txt.jian.hanlp.seg
output_path=outputs/${corpus}/word_word

echo "Step 1: input + output calculation"
python ${output_path}/edit/in_out_add.py
echo "step 2: Evaluation on Analogy Task"
echo "____________________________________________"
python ${output_path}/sgns/Chinese-Word-Vectors/evaluation/ana_eval_dense.py -v ${output_path}/sgns/in_out.add -a ${output_path}/sgns/Chinese-Word-Vecotrs/testsets/CA8/semantic.txt
python ${output_path}/sgns/Chinese-Word-Vectors/evaluation/ana_eval_dense.py -v ${output_path}/sgns/in_out.add -a ${output_path}/sgns/Chinese-Word-Vecotrs/testsets/CA8/morphological.txt
echo "__________________done!_____________________"

echo "Step 3: input + output + component calculation"
python ${output_path}/edit/com_in_out_add.py
echo "step 4: Evaluation on Analogy Task"
echo "____________________________________________"
python ${output_path}/sgns/Chinese-Word-Vectors/evaluation/ana_eval_dense.py -v ${output_path}/sgns/com_in_out.add -a ${output_path}/sgns/Chinese-Word-Vecotrs/testsets/CA8/semantic.txt
python ${output_path}/sgns/Chinese-Word-Vectors/evaluation/ana_eval_dense.py -v ${output_path}/sgns/com_in_out.add -a ${output_path}/sgns/Chinese-Word-Vecotrs/testsets/CA8/morphological.txt
echo "__________________done!_____________________"
