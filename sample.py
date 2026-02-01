from abc import ABC, abstractmethod

class Foo:
    def __getitem__(self, index):
        ...
    def __len__(self):
        ...
    def __iter__(self):
        for i in range(len(self)):
            yield self[i]
    def get_iterator(self):
        return iter(self)

class MyIterable(ABC):
    @abstractmethod
    def __iter__(self):
        pass

    def get_iterator(self):
        return self.__iter__()

    @classmethod
    def __subclasshook__(cls, C):
        if cls is MyIterable:
            if any("__iter__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented

MyIterable.register(Foo)
