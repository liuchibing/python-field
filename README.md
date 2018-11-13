# field for Python
Define 'fields' inside class definition but outside function, just like C++, Java, etc.

This may be useful when you are writing classes which contains lots of attributes managed by different methods, where problems like which attr is defined where could be a headache. It can also make it easier to maintain the __slots__ attr: you can just define fields and the FieldMetaclass will create __slots__ automatically.

This module should work with inheritance, but be careful when using inheritance: naming conflicts won't be reported by the metaclass, which may result in unexpected behavior.

usage:

```python
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
```
Copyright liuchibing 2018
