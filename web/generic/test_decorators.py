# coding: utf-8
'''
Created on Sep 23, 2012

@author: yeti
'''
from __future__ import print_function


from builtins import object
def test_decorator(view_func):
    def _wrapper(self, *args, **kwargs):
        print("Inside decorated function")
        return view_func(self, *args, **kwargs)
    return _wrapper

class A(object):
    @test_decorator
    def do_smtg(self, test = 1):
        print(test)
    
class B(A):
    @test_decorator
    def do_smtg(self, test = 2):
        print(test)
        super(B, self).do_smtg()
        

if __name__ == "__main__":
    a = A()
    a.do_smtg()
    
    print("----")
    
    b = B()
    b.do_smtg()
    