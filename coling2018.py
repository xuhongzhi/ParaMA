'''
Created on Jun 11, 2018

@author: xh
'''
from param import Parameter
from evaluation import evaluate_seg
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

def read_test_gold(infile):
    fin = open(infile, 'r', -1, 'utf-8')
    wordlist = []
    goldseglist = []
    for line in fin:
        line = line.strip()
        token_segs = line.split(':')
        seg_candidates = token_segs[1].strip().split(' ')
        original_word = token_segs[0].strip()
        word = ''
        segs_morphs = []
        for seg in seg_candidates:
            seg_morphs = seg.strip().split('-')
            mainword = ''.join(seg_morphs)
            if word != '' and mainword != word:
                print('Inconsistent segmentations: %s - %s' % (word, mainword))
            word = mainword
            segs_morphs.append(tuple(seg_morphs))
        wordlist.append(original_word)
        goldseglist.append(segs_morphs)
    fin.close()
    return wordlist, goldseglist

def add_test_to_train(train_word_freq_list, test_list):
    word_dict = dict(train_word_freq_list)
    for word in test_list:
        if word in word_dict:
            word_dict[word] += 10
        else:
            word_dict[word] = 10
    return sorted(word_dict.items(), key=lambda x: -x[1])

def run_experiment(infile_train, infile_test_gold, params):
    print('| Reading data...')
    train_word_freq_list = read_word_freq_list(infile_train)
    test_list, test_gold = read_test_gold(infile_test_gold)
    print('--Training data: %s' % (len(train_word_freq_list)))
    print('--Testing data: %s' % (len(test_list)))
    #
    train_word_freq_list = add_test_to_train(train_word_freq_list, test_list)
    #
    print('| Training...')
    morph_analyzer = MorphAnalyzer(params)
    morph_analyzer.train(train_word_freq_list)
    print('| Segmenting test tokens...')
    test_segs_components = morph_analyzer.segment_token_list(test_list)
    test_segs = [x[0] for x in test_segs_components]
    print('| Evaluation...')
    evaluate_seg(test_gold, test_segs)

def run_english():
    params = Parameter()
    params.UseTransRules = True
    params.DoPruning = True
    params.DoCompound = True
    params.ExcludeUnreliable = True
    params.BestNCandSuffix = 70
    infile_train = r'data/wordlist.2010.eng.utf8.txt'
    infile_test_gold = r'data/mit/gold.eng.txt'
    run_experiment(infile_train, infile_test_gold, params)

def run_turkish():
    params = Parameter()
    params.UseTransRules = True
    params.DoPruning = False
    params.DoCompound = False
    params.ExcludeUnreliable = False
    params.BestNCandSuffix = 150
    infile_train = r'data/wordlist.2010.tur.utf8.txt'
    infile_test_gold = r'data/mit/gold.tur.txt'
    run_experiment(infile_train, infile_test_gold, params)

def run_finnish():
    params = Parameter()
    params.UseTransRules = False
    params.DoPruning = True
    params.DoCompound = True
    params.ExcludeUnreliable = True
    params.BestNCandSuffix = 150
    infile_train = r'data/wordlist.2010.fin.utf8.txt'
    infile_test_gold = r'data/mit/gold.fin.txt'
    run_experiment(infile_train, infile_test_gold, params)

if __name__ == '__main__':
    run_english()
    #run_turkish()
    #run_finnish()














