'''
Created on Jun 12, 2018

@author: xh
'''

import argparse
from param import Parameter
from morphanalyzer import MorphAnalyzer

def read_word_freq_list(infile):
    fin = open(infile, 'r', -1, 'utf-8')
    wordlist = []
    for line in fin:
        splitline = line.strip().split()
        if len(line) == 0: continue
        word = splitline[0]
        freq = int(splitline[1])
        wordlist.append((word, freq))
    fin.close()
    return wordlist

def save_segmentations(word_segs, outfile):
    fout = open(outfile, 'w', -1, 'utf-8')
    for word, (seg, components) in word_segs:
        seg_str = ' '.join(seg)
        component_str = ' '.join([' '.join(component) for component in components])
        fout.write('%s\t%s\t%s\n' % (word, seg_str, component_str))
    fout.close()

def run(infile, outfile, params):
    print('| Reading data...')
    word_freq_list = read_word_freq_list(infile)
    print('| Analyzing...')
    morph_analyzer = MorphAnalyzer(params)
    morph_analyzer.train(word_freq_list)
    print('| Segmenting...')
    word_list = [word for word, _freq in word_freq_list]
    word_segs = morph_analyzer.segment_token_list(word_list)
    print('| Saving result...')
    save_segmentations(zip(word_list, word_segs), outfile)
    print('| Done!')

if __name__ == '__main__':
    params = Parameter()
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('infile', help='The input file containing a word list with line format: <word> <freq>')
    arg_parser.add_argument('outfile', help='The output file to save the segmentation result')
    arg_parser.add_argument('-p', '--prune', help='Whether use pruning (1|0, default:%s)' % params.DoPruning, type=bool, default=params.DoPruning)
    arg_parser.add_argument('-t', '--trans', help='Whether use transformation rules (1|0, default:%s)' % params.UseTransRules, type=bool, default=params.UseTransRules)
    arg_parser.add_argument('-c', '--comp', help='Whether process compounding (1|0, default:%s)' % params.DoCompound, type=bool, default=params.DoCompound)
    arg_parser.add_argument('-e', '--excl', help='Whether exclude unreliable roots (1|0, default:%s)' % params.ExcludeUnreliable, type=bool, default=params.ExcludeUnreliable)
    arg_parser.add_argument('-n', '--hyphen', help='Whether explicitly deal with hyphen words (1|0, default:%s)' % params.DoHyphen, type=bool, default=params.DoHyphen)
    arg_parser.add_argument('-a', '--apos', help='Whether explicitly deal with apostrophes (1|0, default:%s)' % params.DoApostrophe, type=bool, default=params.DoApostrophe)
    arg_parser.add_argument('-r', '--root', help='Minimal length of roots that will be possibly segmented (default:%s)' % params.MinStemLen, type=int, default=params.MinStemLen)
    arg_parser.add_argument('-s', '--suff', help='Maximal length of suffixes (default:%s)' % params.MaxSuffixLen, type=int, default=params.MaxSuffixLen)
    args = arg_parser.parse_args()
    params.DoPruning = args.prune
    params.UseTransRules = args.trans
    params.DoCompound = args.comp
    params.ExcludeUnreliable = args.excl
    params.DoHyphen = args.hyphen
    params.DoApostrophe = args.apos
    params.MinStemLen = args.root
    params.MaxSuffixLen = args.suff
    params.print_all()
    run(args.infile, args.outfile, params)

    

    














