'''
Created on Jun 11, 2018

@author: xh
'''

class Parameter():
    '''
    '''


    def __init__(self):
        '''
        '''
        # Main Parameters
        self.UseTransRules = True
        self.DoPruning = True
        self.ExcludeUnreliable = True
        self.DoCompound = False
        
        # 
        self.MinStemLen = 3
        self.MaxSuffixLen = 6
        
        self.DoHyphen = True
        self.DoApostrophe = True
        self.ApostropheChar = '\''
        
        self.BestNCandSuffix = 100
        self.MinSuffixFreq = 3
        self.MinParadigmSupport = 2
        self.MinParadigmSuffix = 2
        
        
    def print_all(self):
        print('--------------Parameters-------------')
        print('UseTransRules: %s' % self.UseTransRules)
        print('DoPruning: %s' % self.DoPruning)
        print('DoCompound: %s' % self.DoCompound)
        print('ExcludeUnreliable: %s' % self.ExcludeUnreliable)
        print('MinStemLen: %s' % self.MinStemLen)
        print('MaxSuffixLen: %s' % self.MaxSuffixLen)
        print('DoHyphen: %s' % self.DoHyphen)
        print('DoApostrophe: %s' % self.DoApostrophe)
        print('-------------------------------------')
        
























