# class RevealAccess(object):
#     """A data descriptor that sets and returns values
#        normally and prints a message logging their access.
#     """
#
#     def __init__(self, initval=None, name='var'):
#         self.val = initval
#         self.name = name
#
#     def __get__(self, obj, objtype):
#         print('Retrieving', self.name)
#         print(objtype)
#         return self.val
#
#     def __set__(self, obj, val):
#         print('Updating', self.name)
#         self.val = val
#
#
# class Fuck():
#     x = RevealAccess(1)
#
#
# # a = Fuck()
# # print(a.x)
#
#
# class TestNew(object):
#     def __new__(cls, *args, **kwargs):
#         obj = super().__new__(cls)
#         obj.field111 = 123
#         return obj
#
#     def __init__(self):
#         print(self.field111)
#
#
# TestNew().__dict__
#
#
# class Fuck():
#     def __init__(self, *_, **kwargs):
#         setattr(self, 'sad', 1)
#         setattr(self, 'sad', 2)
#         setattr(self, 'sad', 3)
#         if 'commit' in kwargs.keys():
#             print(kwargs)
#         else:
#             print('no commit')
#
#
# x = Fuck(pussy=1, origin=None)
# print(x.__dict__)


class A:
    a = 1
    def __init__(self):
        self.print123 = '123'

    def print123(self):
        print('fuck')


class B(A):
    b = 2

print(A().print123)

# b = B()
# print(b.print123())
