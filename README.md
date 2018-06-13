# ParaMA
A Paradigm-based Morphological Analyzer

## Description
This is an unsupervised tool for analyzing suffixation morphology for any languages given a list of words. The details of the algorithm can be found in the following paper:

Hongzhi Xu, Mitch Marcus, Charles Yang, and Lyle Ungar. 2018. Unsupervised Morphology Learning with Statistical Paradigms. (To appear) In *Proceedings of the 27th International Conference on Computational Linguistics (COLING 2018)*. Santa Fe, New-Mexico, USA.

## Start
Use the following command to segment a word list (each line: <word> <freq>), and save it to a file.

  python3 main.py my_data.txt my_data.seg.txt

## Rerun the COLING paper's experiments
Go to coling2018.py for details

