'''
Created on Jun 11, 2018

@author: xh
'''

from reliableroot import is_reliable_root

def create_paradigms(token_structs):
    atomic_word_dict = {}
    paradigm_dict = {}
    for ts in token_structs:
        suffix = ts.suffix
        morph = ts.morph
        word = ts.token
        root = ts.root
        trans = ts.trans
        if suffix == '$':
            atomic_word_dict[word] =  ((word,),((word, '$', '$'),))
            continue
        if root in paradigm_dict: paradigm_dict[root].append((word, trans, suffix, morph))
        else: paradigm_dict[root] = [(word, trans, suffix, morph)]
    return paradigm_dict, atomic_word_dict

def get_paradigm_suffix_sets(paradigm_dict):
    root_suffix_tuple_list = []
    for root, derived_word_list in paradigm_dict.items():
        suffix_set = set([x[2] for x in derived_word_list])
        root_suffix_tuple_list.append((root, suffix_set))
    return root_suffix_tuple_list

def filter_rare_suffix_from_suffix_set(root_suffix_set_list, min_freq):
    suffix_dict = {}
    for root, suffix_set in root_suffix_set_list:
        for suffix in suffix_set: 
            if suffix in suffix_dict: suffix_dict[suffix] += 1
            else: suffix_dict[suffix] = 1
    filtered_suffix_dict = {}
    for suffix, freq in suffix_dict.items():
        if freq < min_freq: continue
        filtered_suffix_dict[suffix] = freq
    filtered_root_suffix_set_list = []
    for root, suffix_set in root_suffix_set_list:
        suffix_list = []
        for suffix in suffix_set:
            if suffix in filtered_suffix_dict: suffix_list.append(suffix)
        if len(suffix_list) > 0:
            filtered_root_suffix_set_list.append((root, set(suffix_list)))
    return filtered_root_suffix_set_list

def stats_suffix_sets(root_suffix_set_list, word_dict):
    suffix_tuple_dict = {}
    for root, suffix_set in root_suffix_set_list:
        freq = word_dict[root] if root in word_dict else 1
        if not is_reliable_root(root, freq): continue
        suffix_tuple = tuple(sorted(suffix_set))
        if suffix_tuple in suffix_tuple_dict: suffix_tuple_dict[suffix_tuple].append((root, freq))
        else: suffix_tuple_dict[suffix_tuple] = [(root, freq)]
    return suffix_tuple_dict

def filter_suffix_tuple(suffix_tuple_dict, min_support, min_tuple_size):
    filtered_suffix_tuple_dict = {}
    for suffix_tuple, root_list in suffix_tuple_dict.items():
        tuple_size = len(suffix_tuple) 
        if tuple_size < min_tuple_size: continue
        support = len(root_list)
        if support < min_support: continue
        long_suffix_count = 0
        for suffix in suffix_tuple:
            if len(suffix) > 1: long_suffix_count += 1
        filtered_suffix_tuple_dict[suffix_tuple] = root_list
    return filtered_suffix_tuple_dict

def stats_single_suffix_type_freq(suffix_tuple_dict):
    suffix_dict = {}
    for suffix_tuple, root_list in suffix_tuple_dict.items():
        freq = len(root_list)
        for suffix in suffix_tuple:
            if suffix in suffix_dict: suffix_dict[suffix] += freq
            else: suffix_dict[suffix] = freq
    return suffix_dict

def get_single_suffix_tuples(suffix_type_dict, suffix_tuple_dict):
    valid_singleton_dict = {}
    for suffix_tuple in suffix_tuple_dict:
        if len(suffix_tuple) != 1: continue
        suffix = suffix_tuple[0]
        if not suffix in suffix_type_dict: continue
        valid_singleton_dict[suffix_tuple] = suffix_tuple_dict[suffix_tuple]
    return valid_singleton_dict

def get_reliable_suffix_tuples(root_suffix_set_list, word_dict, min_support, min_tuple_size, min_suffix_freq):
    root_suffix_set_list = filter_rare_suffix_from_suffix_set(root_suffix_set_list, min_suffix_freq)
    suffix_tuple_dict = stats_suffix_sets(root_suffix_set_list, word_dict)
    filtered_suffix_tuple_dict = filter_suffix_tuple(suffix_tuple_dict, min_support, min_tuple_size)
    suffix_type_dict = stats_single_suffix_type_freq(filtered_suffix_tuple_dict)
    single_suffix_tuple_dict = get_single_suffix_tuples(suffix_type_dict, suffix_tuple_dict)
    return filtered_suffix_tuple_dict, single_suffix_tuple_dict, suffix_type_dict

def discover_maximal_paradigm():
    return












