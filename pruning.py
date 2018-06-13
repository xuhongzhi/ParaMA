'''
Created on Jun 11, 2018

@author: xh
'''

from reliableroot import is_reliable_root

def get_suffix_type_score(suffix_tuples):
    suffix_type_dict = {}
    for suffix_tuple, root_list in suffix_tuples.items():
        for suffix in suffix_tuple:
            if suffix in suffix_type_dict: suffix_type_dict[suffix] += len(root_list)
            else: suffix_type_dict[suffix] = len(root_list)
    return suffix_type_dict

def prune_suffix_tuple(suffix_tuple, suffix_tuple_dict, suffix_type_score):
    if suffix_tuple in suffix_tuple_dict: return suffix_tuple
    if len(suffix_tuple) == 1: return tuple()
    satisfied_tuples = []
    suffix_set = set(suffix_tuple)
    for suffix_tuple in suffix_tuple_dict:
        satisfied_suffix = []
        for suffix in suffix_tuple:
            if suffix in suffix_set:
                satisfied_suffix.append(suffix)
        if len(satisfied_suffix) < 1: continue
        satisfied_tuples.append(satisfied_suffix)
    if len(satisfied_tuples) == 0: return tuple()
    suffix_tuple_score = []
    for suffix_list in satisfied_tuples:
        score = 0
        for suffix in suffix_list:
            score += suffix_type_score[suffix]
        suffix_tuple_score.append((suffix_list, score))
    sorted_suffix_tuple_score = sorted(suffix_tuple_score, key=lambda x: -x[1])
    e_indx = min(3, len(sorted_suffix_tuple_score))
    suffix_tuple_final = []
    for i in range(e_indx):
        suffix_tuple_final.extend(sorted_suffix_tuple_score[i][0])
    return tuple(sorted(set(suffix_tuple_final)))

def prune_paradigms(paradigm_dict, reliable_suffix_tuples, suffix_type_score, single_suffix_tuples, tokens_prob_segs_dict, word_dict, exclude_unreliable):
    pruned_paradigm_dict = {}
    root_suffix_set_dict = {}
    pruned_words = []
    print('--total: %s' % (len(paradigm_dict)))
    count = 0
    percentage = 1
    next_count = int(len(paradigm_dict) * percentage / 10)
    for word, derived_word_list in paradigm_dict.items():
        count += 1
        if count == next_count:
            print('--%s finished.' % (percentage/10))
            percentage += 1
            next_count = int(len(paradigm_dict) * percentage / 10)
        suffix_set = set([x[2] for x in derived_word_list])
        suffix_tuple = tuple(sorted(suffix_set))
        if not word in word_dict: 
            for x in derived_word_list:
                pruned_word, root, suffix = x[0], word, x[2]
                pruned_words.append((pruned_word, root, suffix))
            continue
        freq = word_dict[word]
        root_unreliable = not is_reliable_root(word, freq)
        if exclude_unreliable and root_unreliable:
            for x in derived_word_list:
                pruned_word, root, suffix = x[0], word, x[2]
                pruned_words.append((pruned_word, root, suffix))
            continue
        if len(suffix_tuple) == 1:
            if suffix_tuple in single_suffix_tuples and ((not exclude_unreliable) or root_unreliable):
                pruned_paradigm_dict[word] = derived_word_list.copy()
                root_suffix_set_dict[word] = suffix_set
                continue
            pruned_word, root, suffix = derived_word_list[0][0], word, derived_word_list[0][2]
            pruned_words.append((pruned_word, root, suffix))
            continue
        rem_tuple = prune_suffix_tuple(suffix_tuple, reliable_suffix_tuples, suffix_type_score)
        rem_set = set(rem_tuple)
        if (len(rem_set) < 1):
            for x in derived_word_list:
                pruned_word, root, suffix = x[0], word, x[2]
                pruned_words.append((pruned_word, root, suffix))
            continue
        derived_word_list_1 = []
        for derived_word, trans, suffix, morph in derived_word_list:
            if suffix in rem_set:
                derived_word_list_1.append((derived_word, trans, suffix, morph))
                continue
            pruned_words.append((derived_word, word, suffix))
        if len(derived_word_list_1) > 0:
            pruned_paradigm_dict[word] = derived_word_list_1
            root_suffix_set_dict[word] = rem_set
    return pruned_paradigm_dict










