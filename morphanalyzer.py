'''
Created on Jun 11, 2018

@author: xh
'''
from segcandidate import TokenAnalyzer
from bayesian import get_initial_parameters, estimate_suffix_probability, do_step1_segmention, calc_seg_probs, calc_seg_prob
from segmentation import get_seg_dict_by_paradigms
from pruning import prune_paradigms
from suffixcandidate import gen_N_best_suffix, calc_suf_score_by_dist
from paradigm import create_paradigms, get_paradigm_suffix_sets, get_reliable_suffix_tuples
from reliableroot import is_reliable_root


class MorphAnalyzer():
    '''
    '''
    
    def __init__(self, param):
        self.param = param

    def __get_frequent_long_words(self, word_dict):
        new_word_dict = {}
        for word, freq in word_dict.items():
            word_len = len(word)
            if word_len <= 4: continue
            if freq < 3: continue
            new_word_dict[word] = freq
        return new_word_dict

    def __get_reliable_paradigm_suffixes(self, word_dict):
        #Use long and frequent words to generate initial set of suffixes
        print('--get reliable words')
        reliable_word_dict = self.__get_frequent_long_words(word_dict)
        print('--create token analyzer')
        prior_prob_suffix = {}
        suffix_dict = dict(gen_N_best_suffix(word_dict, min_stem_len=self.param.MinStemLen, max_suf_len=self.param.MaxSuffixLen, best_N=self.param.BestNCandSuffix))
        itr = 0
        while itr < 2:
            itr += 1
            ta = TokenAnalyzer(reliable_word_dict, suffix_dict, self.param.MinStemLen, self.param.MaxSuffixLen, self.param.UseTransRules)
            print('--analyze possible segmentations for tokens')
            token_segs = ta.analyze_token_list(reliable_word_dict.keys())
            print('--get initial parameters')
            probroots, probsuffix, probtrans = get_initial_parameters(token_segs)
            if prior_prob_suffix: probsuffix = prior_prob_suffix
            print('--segment tokens')
            resolved_segs = do_step1_segmention(token_segs, probroots, probsuffix, probtrans)
            print('--create paradigms')
            paradigm_dict, _atomic_word_dict = create_paradigms(resolved_segs)
            print('--get paradigm suffix sets')
            root_suffix_set_list = get_paradigm_suffix_sets(paradigm_dict)
            print('--pruning paradigms')
            reliable_suffix_tuples, single_suffix_tuples, reliable_suffix_type_dict = get_reliable_suffix_tuples(root_suffix_set_list, word_dict, self.param.MinParadigmSupport, self.param.MinParadigmSuffix, self.param.MinSuffixFreq)
            suffix_dict = reliable_suffix_type_dict
            prior_prob_suffix = estimate_suffix_probability(suffix_dict)
        return reliable_suffix_tuples, single_suffix_tuples, reliable_suffix_type_dict
    
    def __strip_apostrophe(self, token):
        apostrophe = ''
        left_part = token
        indx = token.rfind(self.param.ApostropheChar)
        indx_hyphen = token.rfind('-')
        if indx > indx_hyphen:
            apostrophe = token[indx:]
            left_part = token[:indx]
        return left_part, apostrophe
    
    def __split_compound(self, token, word_dict):
        if len(token) < 7: return [token]
        candidate_analyses = []
        for i in range(3, len(token) - 2):
            word0 = token[:i]
            word1 = token[i:]
            if not (word0 in word_dict and word1 in word_dict): continue
            freq0 = word_dict[word0]
            freq1 = word_dict[word1]
            if not (is_reliable_root(word0, freq0) and is_reliable_root(word1, freq1)): continue
            candidate_analyses.append([[word0, word1], abs(len(token) - i - i), -i])
        if len(candidate_analyses) == 0: return [token]
        return sorted(candidate_analyses, key=lambda x: (x[1], x[2]))[0][0]
    
    def __get_subtokens(self, token, word_dict):
        subtokens = token.split('-')
        subtoken_compound = []
        for subtoken in subtokens:
            if self.param.DoCompound:
                compound_components = self.__split_compound(subtoken, word_dict)
                subtoken_compound.extend(compound_components)
            else:
                subtoken_compound.append(subtoken)
        return subtoken_compound

    def __process_hyphen(self, word_dict):
        processed_word_dict = {}
        for word, freq in word_dict.items():
            subwords = word.split('-')
            for subword in subwords:
                if len(subword) == 0: continue
                if subword in processed_word_dict: processed_word_dict[subword] += freq
                else: processed_word_dict[subword] = freq
        return processed_word_dict
    
    def __process_apostrophe(self, word_dict):
        processed_word_dict = {}
        for word, freq in word_dict.items():
            indx = word.find(self.param.ApostropheChar)
            if indx >= 0:
                word = word[:indx]
            if word in processed_word_dict: processed_word_dict[word] += freq
            else: processed_word_dict[word] = freq
        return processed_word_dict
    
    def __process_tokens(self, token_freq_list):
        word_dict = dict(token_freq_list)
        if self.param.DoHyphen: word_dict = self.__process_hyphen(word_dict)
        if self.param.DoApostrophe: word_dict = self.__process_apostrophe(word_dict)
        return word_dict

    def __segment_simple_token(self, token, seg_dict, ta, probroots, probsuffix, probtrans):
        if token in seg_dict: return seg_dict[token]
        segs = ta.analyze_token(token)
        max_prob = 0.0
        best_ts = None
        for ts in segs:
            prob = calc_seg_prob(ts, probroots, probsuffix, probtrans)
            if prob > max_prob:
                max_prob = prob
                best_ts = ts
        if best_ts:
            root = best_ts.root
            suffix = best_ts.suffix
            trans = best_ts.trans
            morph = best_ts.morph
            if suffix == '$': return ((token,),((token, '$', '$'),))
            morphs = []
            components = []
            if root in seg_dict:
                root_seg = seg_dict[root]
                seg_morphs = list(root_seg[0])
                seg_components = root_seg[1]
                indx = 0
                for i in range(len(seg_morphs) - 1):
                    root_morph = seg_morphs[i]
                    morphs.append(root_morph)
                    indx += len(root_morph)
                morphs.append(morph[indx:])
                components.extend(seg_components)
            else:
                morphs.append(morph)
                components.append((root, '$', '$'))
            morphs.append(suffix)
            components.append((root, trans, suffix))
            return (tuple(morphs), tuple(components))
        return ((token,),((token, '$', '$'),))
    
    def __segment_token(self, token, word_dict, seg_dict, ta, probroots, probsuffix, probtrans):
        token, apostrophe_0 = self.__strip_apostrophe(token)
        subtokens = self.__get_subtokens(token, word_dict)
        morphs = []
        components = []
        for i in range(len(subtokens)):
            subtoken, apostrophe = self.__strip_apostrophe(subtokens[i])
            if len(subtoken) == 0: continue
            seg_subtoken_morphs, seg_subtoken_components = self.__segment_simple_token(subtoken, seg_dict, ta, probroots, probsuffix, probtrans)
            morphs.extend(seg_subtoken_morphs)
            components.extend(seg_subtoken_components)
            if apostrophe and len(apostrophe) > 0:
                morphs.append(apostrophe)
                components.append((apostrophe, '$', '$'))
        if apostrophe_0 and len(apostrophe_0) > 0:
            morphs.append(apostrophe_0)
            components.append((apostrophe_0, '$', '$'))
        return tuple(morphs), tuple(components) 
    
    def __segment_tokens(self, token_list, seg_dict, word_dict, ta, probroots, probsuffix, probtrans):
        token_segs = []
        for token in token_list:
            morphs, components = self.__segment_token(token, word_dict, seg_dict, ta, probroots, probsuffix, probtrans)
            token_segs.append((morphs, components))
        return token_segs

    def train(self, train_word_freq_list):
        train_dict = self.__process_tokens(train_word_freq_list)
        reliable_suffix_tuples, single_suffix_tuples, suffix_dict = self.__get_reliable_paradigm_suffixes(train_dict)
        print('| Generate tokens candidate segmentations')
        token_analyzer = TokenAnalyzer(train_dict, suffix_dict, self.param.MinStemLen, self.param.MaxSuffixLen, self.param.UseTransRules)
        token_segs = token_analyzer.analyze_token_list(train_dict.keys())
        print('| Obtain statistics')
        probroots, _probsuffix, probtrans = get_initial_parameters(token_segs)
        probsuffix = estimate_suffix_probability(suffix_dict)
        print('| Segment tokens')
        resolved_segs = do_step1_segmention(token_segs, probroots, probsuffix, probtrans)
        print('| Create paradigms')
        paradigm_dict, atomic_word_dict = create_paradigms(resolved_segs)
        print('| Recalculate seg probability')
        token_seg_probs = calc_seg_probs(token_segs, probroots, probsuffix, probtrans)
        token_seg_prob_dict = dict(token_seg_probs)
        print('| Calculate suffix score')
        suffix_type_score = calc_suf_score_by_dist(paradigm_dict)
        if self.param.DoPruning:
            print('| Prune paradigms')
            paradigm_dict = prune_paradigms(paradigm_dict, reliable_suffix_tuples, suffix_type_score, single_suffix_tuples, token_seg_prob_dict, train_dict, self.param.ExcludeUnreliable)
        print('| Get segmentation dictionary')
        seg_dict = get_seg_dict_by_paradigms(paradigm_dict)
        seg_dict.update(atomic_word_dict)
        #
        suffix_tuple_dict = {}
        suffix_tuple_dict.update(reliable_suffix_tuples)
        suffix_tuple_dict.update(single_suffix_tuples)
        #
        self.__word_dict, self.__seg_dict, self.__ta, self.__probroots, self.__probsuffix, self.__probtrans = train_dict, seg_dict, token_analyzer, probroots, probsuffix, probtrans
    
    def segment_token(self, token):
        return self.__segment_token(token, self.__word_dict, self.__seg_dict, self.__ta, self.__probroots, self.__probsuffix, self.__probtrans)
    
    def segment_token_list(self, token_list):
        token_seg_list = []
        for token in token_list:
            token_seg_list.append(self.segment_token(token))
        return token_seg_list









