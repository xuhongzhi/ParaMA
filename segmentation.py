'''
Created on Jun 11, 2018

@author: xh
'''


def get_seg_dict_by_token_dict(token_seg_dict):
    seg_dict = {}
    for word in token_seg_dict.keys():
        if word in seg_dict: continue
        wd_stack = [word]
        while wd_stack:
            wd = wd_stack[-1]
            if wd in seg_dict:
                wd_stack.pop()
                continue
            if wd in token_seg_dict:
                #morph, suffix, root, trans
                wd_morph, wd_suffix, wd_root, wd_trans = token_seg_dict[wd]
                if wd_suffix == '$' or wd_suffix == '':
                    seg_dict[wd] = ((wd_morph,), ((wd_root, wd_trans, wd_suffix),))
                    wd_stack.pop()
                    continue
                elif wd_root in seg_dict:
                    #examples: loneliness = loneli (lonely -y+i) +ness;    lonely = lone () +ly
                    #Alignment:
                    #--REP: lone+ly -> lone+li
                    #--DEL: en+force -> en+forc
                    #--DUP: under+pin -> under+pinn
                    rt_seg = seg_dict[wd_root]
                    rt_morphs = rt_seg[0]
                    morphs = []
                    indx = 0
                    for i in range(len(rt_morphs)-1):
                        rt_morph = rt_morphs[i]
                        morphs.append(wd_morph[indx:indx+len(rt_morph)])
                        indx += len(rt_morph)
                    morphs.append(wd_morph[indx:])
                    morphs.append(wd_suffix)
                    components = list(rt_seg[1])
                    components.append((wd_root, wd_trans, wd_suffix))
                    seg_dict[wd] = (tuple(morphs), tuple(components))
                    wd_stack.pop()
                    continue
                else:
                    wd_stack.append(wd_root)
                    continue
            else:
                #inferenced non-appeared root:
                #example: communicating = communicat + ing
                seg_dict[wd] = ((wd,), ((wd, '$', '$'),))
                wd_stack.pop()
                continue
    return seg_dict

def seg_dict_update(seg_dict):
    #Recursively update segmentation if root is segmented
    updated_seg = {}
    for word, (morphs, components) in seg_dict.items():
        if len(morphs) == 1: continue
        r_seg_morphs = tuple(morphs)
        r_seg_components = tuple(components)
        root = r_seg_components[0][0]
        r_morph = morphs[0]
        morphs_new = tuple(morphs[1:])
        components_new = tuple(components[1:])
        while root in seg_dict:
            r_seg = seg_dict[root]
            r_seg_morphs_1 = r_seg[0]
            r_seg_components_1 = r_seg[1]
            if len(r_seg_morphs_1) == 1: break
            indx = sum([len(x) for x in r_seg_morphs_1[:-1]])
            morphs_new = tuple(r_seg_morphs_1[1:-1]) + (r_morph[indx:],) + morphs_new
            components_new = tuple(r_seg_components_1[1:]) + components_new
            r_seg_morphs = r_seg_morphs_1
            r_seg_components = r_seg_components_1
            root = r_seg_components[0][0]
            r_morph = r_seg_morphs[0]
        morphs_new = r_seg_morphs[:1] + morphs_new
        components_new = r_seg_components[:1] + components_new
        updated_seg[word] = (morphs_new, components_new)
    seg_dict.update(updated_seg)

def get_seg_dict_by_paradigms(paradigm_dict):
    token_seg_dict = {}
    for root, word_list in paradigm_dict.items():
        for word, trans, suffix, stem in word_list:
            token_seg_dict[word] = (stem, suffix, root, trans)
    seg_dict = get_seg_dict_by_token_dict(token_seg_dict)
    return seg_dict






