# ParaMA
A Paradigm-based Morphological Analyzer

## Description
This is an unsupervised tool for analyzing suffixation morphology for any languages given a list of words. The details of the algorithm can be found in the following paper:

Hongzhi Xu, Mitch Marcus, Charles Yang, and Lyle Ungar. 2018. Unsupervised Morphology Learning with Statistical Paradigms. In *Proceedings of the 27th International Conference on Computational Linguistics (COLING 2018)*. pages 44-54. Santa Fe, New Mexico, USA.

## Segment a word list
Use the following command to segment a word list (each line: \<word\> \<freq\>), and save it to a file. Use -h for more information.

  python3 main.py my_data.txt my_data_seg.txt

The output also gives the derivational chain information. For example, the word _sterilizing_ is derivated by sterilize, deleting _e_ and plus _-ing_, which is then derived from _sterile_, deleting _e_ and plus _-ize_. The line will be like the following except that there will be no brackets.

sterilizing \<\t\> steril iz ing \<\t\> (sterile $ $) (sterile DEL-e ize) (sterilize DEL-e ing)

## Rerun the COLING paper's experiments
Go to coling2018.py for details

