# -*- coding: UTF-8 -*-

class Person(object):

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.weight = 'weight'

    def talk(self):
        print("person is talking....")


class Chinese(Person):

    def __init__(self, name, age, language):
        super(Chinese, self).__init__(name ,age)
        self.language = language

c = Chinese('bigberg', 22, 'chinese')
print(c.language, c.name)