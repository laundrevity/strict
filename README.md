I want to better understand how this works:


```
instance = super().__call__(*args, **kwargs)
abstract_attributes = {
    key for key in dir(instance)
    if getattr(
        getattr(instance, key),
        '__is_abstract_attribute__',
        False
    )
}
```

This is within the method ```__call__``` of ```StrictMeta``` which is a subclass of ```type```.

What is the inner ```getattr``` doing? 

By wrapping the method ```necessary_attribute``` in ```StrictClassInterface```, we ensure that the value of any instance of a subclass of ```StrictClassInterface``` at key ```necessary_attribute``` is  ```abstractattribute```, if not otherwise specified. Any other such specification can only happen in the ```___init___``` method. So this "default" value of ```abstractattribute``` for ```necessary_attribute``` will remain if and only if we didn't initialize the member. 

Hence:
```
cls=<class 'test_main.MissingAttribute'>, iterating over keys in dir(instance):
INFO     root:ext_abc.py:52 getattr(instance, necessary_attribute) = <bound method StrictClassInterface.necessary_attribute of <test_main.MissingAttribute object at 0x7fe0b805c490>>
INFO     root:ext_abc.py:55 getattr(getattr(instance, necessary_attribute), '__is_abstract_attribute__', False)=True
INFO     root:ext_abc.py:52 getattr(instance, necessary_method) = <bound method MissingAttribute.necessary_method of <test_main.MissingAttribute object at 0x7fe0b805c490>>
INFO     root:ext_abc.py:55 getattr(getattr(instance, necessary_method), '__is_abstract_attribute__', False)=False
INFO     root:ext_abc.py:52 getattr(instance, optional_attribute) = <bound method StrictClassInterface.optional_attribute of <test_main.MissingAttribute object at 0x7fe0b805c490>>
INFO     root:ext_abc.py:55 getattr(getattr(instance, optional_attribute), '__is_abstract_attribute__', False)=False
INFO     root:ext_abc.py:52 getattr(instance, optional_method) = <bound method StrictClassInterface.optional_method of <test_main.MissingAttribute object at 0x7fe0b805c490>>
INFO     root:ext_abc.py:55 getattr(getattr(instance, optional_method), '__is_abstract_attribute__', False)=False
INFO     root:test_main.py:59 Cannot instantiate abstract class MissingAttribute without attributes necessary_attribute
INFO     root:ext_abc.py:47 
```
The nested ```getattr``` evaluates to ```True``` because ```necessary_attribute``` was never initialized in the ```MissingAttribute``` class, so it still has its "default" wrapped value with ```__is_abstract_attribute__``` set to ```True```.

What is still curious is how to disallow ```necessary_method = None```, which is not a Callable as it should be.

The problem is that there is no way to tell that ```necessary_method```, when overridden as just ```None```, was supposed to be a callable, because by overriding its value we discard the ```__is_abstract_method__``` attribute. To do this properly, we need to determine whether or not this key corresponds to an abstract method by checking with the parent class, ```StrictClassInterface```.
