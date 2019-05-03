class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.occupation = 'unemployed'

p1 = Person('Adam', 20)
p2 = Person('Karen', 32)
#print(p1.occupation)

class Duck:
    def fly(self):
        print('Duck flying')

class Airplane:
    def fly(self):
        print('Airplace flying')

def lift_off(entity):
    entity.fly()

duck = Duck()
airplane = Airplane()


#lift_off(duck)
#lift_off(airplane)

dbl = lambda x: x * 2
#print(dbl(5))

#Overriding Default Behavior
class Foo:
    def __init__(self):
        self.x = 10
    
    def __str__(self):
        return 'This object has x = ' + str(self.x)

f = Foo()
#Makes f have the value of the string returned in __str__
#print(f)

#Modifies the default getter and setter and adds our own print statements
class Attrs:
    def __getattribute__(self, a):
        print(f'Getting {a}')
        return object.__getattribute__(self, a)

    def __setattr__(self, k, v):
        print(f'Setting {k} to {v}')
        object.__setattr__(self, k, v)

#attrs = Attrs()
#attrs.x = 10
#print(attrs.x)

s = "42 13 7 26"
data = [int(x) for x in s.split()]
#for i in range(len(data)):
#    print(f'Element {i} is {data[i]}')
#print(';'.join(s))

#for i, x in enumerate(data):
#    print(f'Element {i} is {x}')

states = {'New Jersey' : 'NJ',
            'California' : 'CA',
            'Texas' : 'TX'}

"""try:
    print(states['New York'])
except KeyError:
    raise Exception('something bad happened')
except Exception:
    print('uh oh')
"""
#for k in states:
#    print(f"{k}'s abbreviation is {states[k]}")

#for k, v in states.items():
#    print(f"{k}'s abbreviation is {v}")

def foo():
    return (10, 20)

x, y = foo()
#print(x)
#print(y)

"""
class Flower:
    pass

class Plant(Flower):
    pass

class Employee:
    def __init__(self, taxID):
        self.taxID = taxID

    def __str__(self):
        return f'My taxID is {self.taxID}'

class Student:
    def __init__(self, gpa):
        self.gpa = gpa

    def __str__(self):
        return f'My gpa is {self.gpa}'

class GradStudent(Employee, Student):
    def __init__(self, taxID, gpa):
        Employee.__init__(self, taxID)
        Student.__init__(self, gpa)

Guang = GradStudent(Student(4.0), Employee('A1234'))
print(Guang)
"""

# Example of Multiple Inheritance
class A:
    def f(self):
        print("f in A called")

class B(A):
    pass

class C(A):
    def f(self):
        print("f in C called")

class D(B, C):
    pass

c = A()
#c.f()

