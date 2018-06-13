'''
Created on Jun 11, 2018

@author: xh
'''


import math

def filter_afx_by_freq(afx_dict, min_afx_freq):
    filtered_suf_dict = {}
    for suf, stem_len_dist in afx_dict.items():
        count = sum(stem_len_dist.values())
        if count >= min_afx_freq:
            filtered_suf_dict[suf] = stem_len_dist
    return filtered_suf_dict

def group_afx_by_length(affix_stem_len_dist):
    min_root_len = 100
    max_root_len = 0
    groups = {}
    for afx, stem_len_dist in affix_stem_len_dist.items():
        afx_len = len(afx)
        if afx_len in groups:
            groups[afx_len].append((afx, stem_len_dist))
        else:
            groups[afx_len] = [(afx, stem_len_dist)]
        min_root_len, max_root_len = min(min_root_len, min(stem_len_dist)), max(max_root_len, max(stem_len_dist))
    return groups, min_root_len, max_root_len


def gen_suf_cand_by_stem_len(word_dict, min_stem_len, max_suf_len, min_suf_freq = 1):
    suf_dict = {}
    for word in word_dict:
        if len(word) <= min_stem_len: 
            continue
        sIndx = max(min_stem_len, len(word) - max_suf_len)
        for i in range(sIndx, len(word)):
            stem = word[:i]
            suf = word[i:]
            if stem in word_dict:
                stem_len = len(stem)
                if suf in suf_dict:
                    suf_len_dict = suf_dict[suf]
                    if stem_len in suf_len_dict:
                        suf_len_dict[stem_len] += 1
                    else:
                        suf_len_dict[stem_len] = 1
                else:
                    suf_dict[suf] = {stem_len:1}
    if min_suf_freq <= 1:
        return suf_dict
    return filter_afx_by_freq(suf_dict, min_suf_freq)


def calc_expected_stem_len(affix_stem_len_dist, min_stem_len, max_stem_len):
    # Smoothing by plus .001
    epi = 0.001
    afx_len_exp = []
    for afx, stem_len_dist in affix_stem_len_dist:
        count_sum = 0.0
        len_sum = 0.0
        for stem_len in range(min_stem_len, max_stem_len+1):
            count = epi
            if stem_len in stem_len_dist:
                count += stem_len_dist[stem_len]
            count_sum += count
            len_sum += stem_len * count
        len_exp = len_sum / count_sum
        afx_score = math.log10(1 + count_sum) * len_exp
        afx_len_exp.append((afx, afx_score, count_sum, len_exp))
    return afx_len_exp

def calc_suf_score_by_dist(paradigm_dict):
    suffix_root_len_dist = {}
    min_root_len = 100
    max_root_len = 0
    for root, derived_word_list in paradigm_dict.items():
        root_len = len(root)
        min_root_len = min(min_root_len, root_len)
        max_root_len = max(max_root_len, root_len)
        for _word, _trans, suffix, _morph in derived_word_list:
            if suffix in suffix_root_len_dist:
                root_len_dist = suffix_root_len_dist[suffix]
                if root_len in root_len_dist:
                    root_len_dist[root_len] += 1
                else:
                    root_len_dist[root_len] = 1
            else:
                root_len_dist = {root_len:1}
                suffix_root_len_dist[suffix] = root_len_dist
    suffix_root_len_dist = sorted(suffix_root_len_dist.items(), key=lambda x: x[0])
    suffix_len_exp = calc_expected_stem_len(suffix_root_len_dist, min_root_len, max_root_len)
    suffix_score_dict = dict([(suffix, score) for suffix, score, _count_sum, _len_exp in suffix_len_exp])
    return suffix_score_dict

def filter_afxes(affix_root_len_dist, top_N = 50):
    filtered_affixes = []
    same_len_affix_dist, min_root_len, max_root_len = group_afx_by_length(affix_root_len_dist)
    print('Suffix Legth Range: (%s, %s)' % (min(same_len_affix_dist.keys()), max(same_len_affix_dist.keys())))
    for afx_len, afx_stem_len_dist in sorted(same_len_affix_dist.items(), key=lambda x: x[0]):
        print('Processing Suffix Length: %s.' % (afx_len))
        affix_len_exp = calc_expected_stem_len(afx_stem_len_dist, min_root_len, max_root_len)
        affix_len_exp = sorted(affix_len_exp, key=lambda x: -x[1])
        top_N_afx = affix_len_exp[:top_N]
        filtered_affixes.extend(top_N_afx)
    filtered_affixes = sorted([(afx, afx_score) for afx, afx_score, _count, _len_exp in filtered_affixes], key = lambda x: -x[1])
    return filtered_affixes

def gen_N_best_suffix(word_dict, min_stem_len=3, max_suf_len=4, min_suf_freq=10, best_N=50):
    suffix_stem_len_dist = gen_suf_cand_by_stem_len(word_dict, min_stem_len, max_suf_len, min_suf_freq)
    best_suffix_list = filter_afxes(suffix_stem_len_dist, best_N)
    return best_suffix_list



















