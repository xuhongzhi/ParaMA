'''
Created on Jun 11, 2018

@author: xh
'''

def is_reliable_root(root, freq):
    root_len = len(root)
    if root_len < 3: return False
    if root_len == 3 and freq < 2000: return False
    if root_len == 4 and freq < 200: return False
    if root_len == 5 and freq < 20: return False
    if root_len == 6 and freq < 10: return False
    if freq < 3: return False
    return True















