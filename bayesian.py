'''
Created on Jun 11, 2018

@author: xh
'''


def feature(root, suffix):
    if suffix == '$': return ('$', suffix)
    return (root[-1], suffix[0])

def get_initial_parameters(token_segs):
    estems = {}
    esuffix = {}
    etrans = {}
    eftrans = {}
    #
    for ts_list in token_segs:
        avg_prob = 1.0 / len(ts_list) 
        for ts in ts_list:
            root = ts.root
            rand_val = 1.0
            if root in estems: estems[root] += rand_val * avg_prob
            else: estems[root] = rand_val * avg_prob
            #
            suffix = ts.suffix
            if suffix in esuffix: esuffix[suffix] += rand_val * avg_prob
            else: esuffix[suffix] = rand_val * avg_prob
            #
            trans = ts.trans
            ftrans = feature(root, suffix)
            if (trans, ftrans) in etrans: etrans[(trans, ftrans)] += rand_val * avg_prob
            else: etrans[(trans, ftrans)] = rand_val * avg_prob
            #
            if ftrans in eftrans: eftrans[ftrans] += rand_val * avg_prob
            else: eftrans[ftrans] = rand_val * avg_prob
    #
    probstems = estems
    probsum = sum(probstems.values())
    for stem in probstems: probstems[stem] /= probsum
    #
    probsuffix = esuffix
    probsum = sum(probsuffix.values())
    for suffix in probsuffix: probsuffix[suffix] /= probsum
    #
    probtrans = etrans
    for trans, ftrans in probtrans: probtrans[(trans, ftrans)] /= eftrans[ftrans]
    return probstems, probsuffix, probtrans

def calc_seg_prob(ts, probroots, probsuffix, probtrans):
    root = ts.root
    suffix = ts.suffix
    trans = ts.trans
    feat = feature(root, suffix)
    score = 0.0
    if root in probroots and suffix in probsuffix and (trans, feat) in probtrans:
        score = probroots[root] * probsuffix[suffix] * probtrans[(trans, feat)]
    return score

def calc_seg_probs(token_segs, probroots, probsuffix, probtrans):
    token_seg_probs = []
    for segs in token_segs:
        seg_probs = []
        token = segs[0].token
        for ts in segs:
            score = calc_seg_prob(ts, probroots, probsuffix, probtrans)
            seg_probs.append((ts, score))
        seg_probs = sorted(seg_probs, key=lambda x: -x[1])
        token_seg_probs.append((token, seg_probs))
    return token_seg_probs

def do_step1_segmention(token_segs, probroots, probsuffix, probtrans):
    resolved_segs = []
    for segs in token_segs:
        max_score = -1.0
        best_ts = None
        for ts in segs:
            score = calc_seg_prob(ts, probroots, probsuffix, probtrans)
            if score > max_score:
                best_ts = ts
                max_score = score
        resolved_segs.append(best_ts)
    return resolved_segs

def estimate_suffix_probability(suffix_freq_dict):
    suffix_prob_dict = {}
    probsum = sum(suffix_freq_dict.values())
    for suffix, freq in suffix_freq_dict.items():
        suffix_prob_dict[suffix] = freq * 1.0 / probsum
    return suffix_prob_dict








