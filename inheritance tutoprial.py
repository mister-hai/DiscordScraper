class ParentClass(object):
    def __new__(cls, *args, **kwargs):
        return super(__class__, cls).__new__(cls, *args, **kwargs)
    def __init__(self):
        self.data = {}
    def __call__(self):
        return self.data

class ChildClass(ParentClass):
    def __new__(cls, *args, **kwargs):
        print(super(__class__, cls).__new__(cls, *args, **kwargs))
    def __init__(self):
        self.data = {}
    def __call__(self):
        print("class name: " + self.__class__)
