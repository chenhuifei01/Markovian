from .hashtable import Hashtable 

class LPHashtable(Hashtable):
    '''
    Class for constructing a hashtable.
    Attributes:
        capacity(int): the capacity of a hashtable
        _items(lst): a single list to store items
        size(int): the size of a hashtable
        default_value(int): the default value of a hashstable 
    Methods:
        _hash:
            takes in a string and returns a hash value
        __setitem__:
            assign the value associated with key to value
        __getitem__:
            return the value associated with key or default value
        __len__:
            return the total number of items currently sotred within
            table
        rehash:
            grow the hashtable with the GROWTH_RATIO if it meet the 
            a certain proportion of capacity
    '''
    # polynomial constant, used for _hash
    P_CONSTANT = 37
    # if the total number of items / capacity exceeds this value, rehash
    TOO_FULL = 0.5
    # factor by which capacity should grow during a rehash
    GROWTH_RATIO = 2

    def __init__(self, capacity, default_value):
        '''
        Constructor for the LPHashtable class
        Input:
            capacity(int): the capacity of a hashtable
            default_value(int): the default value of a hashstable 
        '''
        self.capacity = capacity 
        self._items = [None] * self.capacity 
        self.default = default_value
        self.size = 0 
        
    def _hash(self, key):
        '''
        takes in a string and returns a hash value
        Input:
            key(str): string
        Returns(int): hash value
        '''        
        hashvalue = 0
        p = 37
        for ch in key:
            hashvalue = p * hashvalue + ord(ch)
            hashvalue = hashvalue % self.capacity
        return hashvalue 

    def __setitem__(self, key, val):
        '''
        assign the value associated with key to value
        Input: 
            key(str): string
            val(int): the number of times the string 
            appeared in text
        '''
        temptuple = (key,val)
        index = self._hash(key)
        for _ in range(self.capacity):
            if self._items[index] == None:
                self._items[index] = temptuple
                self.size = self.size + 1
                if self.size/self.capacity >= self.TOO_FULL:
                    self.rehash()
                break
            if self._items[index][0] == key:
                self._items[index] = temptuple
                break
            index = index + 1
            index = index % self.capacity

    def __getitem__(self, key):
        '''
        return the value associated with key or default value
        Input: 
            key(str): string
        Returns(int): the value
        '''
        index = self._hash(key)
        temp = index
        while 1:
            if self._items[index] != None and self._items[index][0] == key:
                return self._items[index][1] 
            else:
                index = (index + 1) % self.capacity
            if index == temp:
                return self.default
    
    def __len__(self):
        '''
        return the total number of items currently sotred within
        table
        Returns(int): the total number of items
        '''
        return self.size

    def rehash(self):
        '''
        grow the hashtable with the GROWTH_RATIO if it meet the 
        a certain proportion of capacity
        '''
        temp = [None] * (self.capacity * (self.GROWTH_RATIO-1))
        self._items.extend(temp)
        self.capacity = self.capacity * self.GROWTH_RATIO
        for i,pair in enumerate(self._items):
            if pair != None:
                self._items[i] = None
                self.size = self.size - 1
                self.__setitem__(pair[0],pair[1])