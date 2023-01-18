import sys
from ..collections.lp_hashtable import LPHashtable
import math

HASH_CELLS = 57
TOO_FULL = 0.5
GROWTH_RATIO = 2

class Markov:
    '''
    Class for defining a probabilistic mechanism for randomly 
    generating sequences over some alphabet of symbols. 
    Attributes:
        S(int): the number of unique symbols of a text
        k(int): a positive value used for order
        lphash(object): a hashtable
    Methods:
        log_probability:
            takes a string and returns the log probability 
            that the modeled speaker uttered it, using the 
            approach described above
    '''
    def __init__(self, k, text):
        """
        Construct a new k-order markov model using the text 'text'.
        Inputs:
            k(int): a positive value used for order
            text(str): a text from speaker used to build 
            the model
        """
        self.S = len(set(text))
        self.k = k
        kstr = [] 
        kone = []
        # for i,_ in enumerate(text):
        for i in range(len(text)):
            if i+k <= len(text):
                kstr.append(text[i:i+k])
            else:
                kstr.append(text[i:] + text[:(i+k) % len(text)])
            if i+k+1 <= len(text):
                kone.append(text[i:i+k+1])
            else:
                kone.append(text[i:] + text[:(i+k+1) % len(text)])

        self.lphash = LPHashtable(HASH_CELLS,0)
        kstr.extend(kone)

        for i in kstr:
            if self.lphash.__getitem__(i) == 0:
                self.lphash.__setitem__(i,1)
            else:
                self.lphash.__setitem__(i,self.lphash.__getitem__(i)+1)


    def log_probability(self, s):
        """
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        Inputs:
            s(str): a text of someone speaker
        Returns(float): log probability that the modeled speaker 
        uttered it
        """
        k = self.k
        answer = 0
        S = self.S
        for i in range(len(s)):
            temp1 = ''
            temp2 = ''
            if i+k <= len(s):
                temp1 = s[i:i+k]
            else:
                temp1 = s[i:] + s[:(i+k) % len(s)]
            if i+k+1 <= len(s):
                temp2 = s[i:i+k+1]
            else:
                temp2 = s[i:] + s[:(i+k+1) % len(s)]
            N = self.lphash.__getitem__(temp1)
            M = self.lphash.__getitem__(temp2)
            answer = answer + math.log((M+1)/(N+S))
        return answer
