'''
Created on Jun 11, 2018

@author: xh
'''


class SegStructure():
    '''
    A class for storing an analysis of a certain token
    '''

    def __init__(self, token, morph, root, trans, suffix):
        self.token = token
        self.root = root
        self.morph = morph
        self.trans = trans
        self.suffix = suffix
        self.key = (root, trans, suffix)
    
    def is_atomic(self):
        return self.token == self.root


class TokenAnalyzer:
    def __init__(self, word_dict, suffix_dict, min_stem_len, max_suffix_len, use_trans_rules):
        self.word_dict = word_dict
        self.suffix_dict = suffix_dict
        self.morph_dict = get_morph_dict(word_dict, min_stem_len)
        self.min_stem_len = min_stem_len
        self.max_suffix_len = max_suffix_len
        self.use_trans_rules = use_trans_rules

    def analyze_token(self, token):
        segs = []
        if len(token) <= self.min_stem_len:
            root = token
            morph = token
            trans = '$'
            suffix = '$'
            ts = SegStructure(token, morph, root, trans, suffix)
            segs.append(ts)
            return segs
        s_indx = max(self.min_stem_len, len(token)-self.max_suffix_len)
        for indx in range(s_indx, len(token)):
            suffix = token[indx:]
            if not suffix in self.suffix_dict: continue
            morph = token[:indx]
            root = morph
            trans = '$'
            #avoid the furious single character suffix with a large amount of non-occurred root
            if (root in self.word_dict):
                ts = SegStructure(token, morph, root, trans, suffix)
                segs.append(ts)
                continue
            #
            if not self.use_trans_rules: continue
            #Always account for a word with the simplest transformation rules
            #avoid -> pains = paint - t + s
            #avoid -> passes = pas + DUP-s + es
            #lost -> borned = borne -e +ing |*born + ing
            if len(suffix) < 2: continue
            #---------------------------------Hypothesize deletion rules
            found_possible_root = False
            if (morph in self.morph_dict):
                for root in self.morph_dict[morph]:
                    if (root + suffix) in self.word_dict: continue
                    found_possible_root = True
                    if root[-1] == suffix[0]:
                        #: voiced = voic(voice-e)+ed
                        trans = 'DEL-' + root[-1]
                        ts = SegStructure(token, morph, root, trans, suffix)
                        segs.append(ts)
                    else:
                        trans = 'DEL-' + root[-1]
                        #: voiced = voic(voice-e)+ed
                        ts = SegStructure(token, morph, root, trans, suffix)
                        segs.append(ts)
            if found_possible_root: continue
            #---------------------------------Hypothesize replacement rules
            #: carried = carry -y+i + ed; morph = carri
            if (morph[0:-1] in self.morph_dict) and (not morph in self.word_dict):
                for root in self.morph_dict[morph[0:-1]]:
                    #avoid painting = paint REP-t+t +ing
                    if root == morph: continue
                    if (root + suffix) in self.word_dict: continue
                    found_possible_root = True
                    trans = 'REP-%s+%s' % (root[-1], morph[-1])
                    ts = SegStructure(token, morph, root, trans, suffix)
                    segs.append(ts)
            if found_possible_root: continue
            #---------------------------------Hypothesize duplication rules
            #avoid passes = pas + DUP+s +es, since pass is already a word
            if (len(morph) > max(2, self.min_stem_len)) and (morph[-1] == morph[-2]):
                root = morph[:-1]
                if (root in self.word_dict) and (not (root + suffix) in self.word_dict):
                    trans = 'DUP-' + morph[-1]
                    ts = SegStructure(token, morph, root, trans, suffix)
                    segs.append(ts)
        if len(segs) == 0:
            root = token
            morph = token
            trans = '$'
            suffix = '$'
            ts = SegStructure(token, morph, root, trans, suffix)
            segs.append(ts)
        return segs

    def analyze_token_list(self, token_list):
        token_segs = []
        for token in token_list:
            segs = self.analyze_token(token)
            token_segs.append(segs)
        return token_segs

def get_morph_dict(word_dict, min_stem_len):
    morph_dict = {}
    for word in word_dict:
        if len(word) <= min_stem_len:
            continue
        morph = word[:-1]
        #---------------------------------------------------------------------
        # pain != paint - t, as itself is a word
        # lost: X = Xe - e, while X is word, Xe is a verb; will be largely affected by noise
        # process in analyzed token
        # (This is done in analyze_token function)
        #---------------------------------------------------------------------
        if morph in morph_dict: morph_dict[morph].append(word)
        else: morph_dict[morph] = [word]
    return morph_dict














