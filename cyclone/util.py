# coding: utf-8

class superdict(dict):
    def __setattr__(self, k, v): dict.__setitem__(self, k, v)
    def __delattr__(self, k): dict.__delitem__(self, k)
    def __getattr__(self, k):
	if k == '__getstate__': raise AttributeError # pickle safe!
	return getattr(dict, k, self.get(k, None))
