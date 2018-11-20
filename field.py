#/bin/env python
# -*- encoding: utf-8 -*-

'''
Define `fields` inside class definition but outside function, just like C++, Java, etc.

This may be useful when you are writing classes which contains lots of attributes managed by different methods, where problems like which attr is defined where could be a headache. It can also make it easier to maintain the __slots__ attr: you can just define fields and the FieldMetaclass will create __slots__ automatically.

This module should work with inheritance, but be careful when using inheritance: naming conflicts won't be reported by the metaclass, which may result in unexpected behavior.

usage:

from field import Field, FieldMetaclass

class Example(object, metaclass=FieldMetaclass):
    __no_slots__ = True # define this if you
        # don't want to generate `__slots__` automatically.
        # FieldMetaclass will remove this attr,
        # so the value can be anything.
        # if you define __slots__ here,
        # the FieldMetaclass will not generate __slots__ anymore,
        # regardless whether or not have you defined __no_slots__.
    my_field = Field() # `None` will be the default value
    my_other = Field(1) # Field with default value `1`
    another = Field(32, from_arg=3) # Init the field using
        # the 3rd argument of __init__
        # (not counting the `self` argument).
        # If the arg is not provided,
        # the default value `32` will be used.
    yet_another = Field(from_arg='yet_another')
        # Init the field using the keyword argument named `yet_another`.
    # You can define anything you want here as usual.
    # For example, the __init__ method.

Copyright liuchibing 2018
'''

__author__ = 'liuchibing'

from functools import wraps

class Field(object):
    '''
    A placeholder representing a field.
    '''
    def __init__(self, default = None, *, from_arg = None):
        self.default = default
        if not isinstance(from_arg, (int,str,type(None))):
            raise TypeError('from_arg: expected int or str, got %s' % (type(from_arg).__name__,))
        self.from_arg = from_arg

def _wrap_init(fields, init):
    @wraps(init)
    def wrapper(self, *args, **kwargs):
        for k,v in fields.items(): # do initialize
            if v.from_arg != None:
                if isinstance(v.from_arg, int) and v.from_arg < len(args):
                    setattr(self,k,args[v.from_arg])
                elif isinstance(v.from_arg, str) and v.from_arg in kwargs:
                    setattr(self,k,kwargs[v.from_arg])
            else:
                setattr(self,k,v.default)
        if callable(init): # call original __init__, if any.
            init(self, *args, **kwargs)
    return wrapper

class FieldMetaclass(type):
    '''
    The metaclass used to create type using field.
    '''
    def __new__(cls, name, bases, attrs):
        fields = dict()
        no_slots = False

        # collect fields information
        for k,v in attrs.items():
            if k == '__no_slots__':
                no_slots = True
            elif isinstance(v, Field):
                fields[k] = v

        if no_slots:
            attrs.pop('__no_slots__')
        for k in fields.keys():
            attrs.pop(k)

        # generate a new __init__
        init = attrs.get('__init__')
        attrs['__init__'] = _wrap_init(fields, init)
        # generate __slots__
        if not no_slots and not '__slots__' in attrs:
            slots = list(fields.keys())
            # iterate through bases to merge __slots__ definition
            for base in bases:
                if hasattr(base,'__slots__'):
                    slots = slots + list(getattr(base,'__slots__'))
            attrs['__slots__'] = tuple(slots)
        return type.__new__(cls, name, bases, attrs)

# print help message
if __name__ == '__main__':
    print('field')
    print(__doc__)

#    class Test(object,metaclass=FieldMetaclass):
#        #__no_slots__=None
#        a=Field(12)
#        b=Field(from_arg='b')
#        c=Field('c',from_arg=0)
#        def hello(self):
#            print('a=%s, b=%s, c=%s' % (self.a, self.b, self.c))
#        def __init__(self,c,*,b,a=None):
#            print('__init__ called.')
#            if a != None:
#                self.a=a
#    class Test2(Test):
#        a2=Field()
#        def __init__(self):
#            super(Test2,self).__init__(22,b='b2')
#
#    t = Test(6,b='b')
#    print(dir(t))
#    print(Test.__slots__)
#    #print(t.__dict__)
#    t.hello()
#    t2 = Test2()
#    #t2.a4=44
#    print(dir(t2))
#    print(Test2.__slots__)
#    t2.hello()
