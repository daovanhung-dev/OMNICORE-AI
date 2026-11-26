"""Cache bộ nhớ cục bộ TTL, giới hạn kích thước, không lưu secret."""
from threading import RLock
from time import monotonic
from collections import OrderedDict

class TTLCache:
    def __init__(self, maxsize:int=128):
        if maxsize<1:raise ValueError('maxsize phải dương')
        self._maxsize=maxsize;self._data=OrderedDict();self._lock=RLock()
    def get(self,key):
        with self._lock:
            item=self._data.get(key)
            if item is None:return None
            if item[0]<=monotonic():self._data.pop(key,None);return None
            self._data.move_to_end(key);return item[1]
    def set(self,key,value,ttl:float):
        if ttl<=0:raise ValueError('TTL phải dương')
        with self._lock:
            self._data[key]=(monotonic()+ttl,value);self._data.move_to_end(key)
            while len(self._data)>self._maxsize:self._data.popitem(last=False)
    def invalidate(self,key):
        with self._lock:self._data.pop(key,None)
