"""
data <=> attributes
functions <=> methods
"""


class Employee:

    num_of_employees = 0
    raise_multiplier = 1.04

    #  Constructor, assigns attributes to objects, you can ONLY HAVE ONE per class, but it can have functions inside it
    def __init__(self, name, surname, pay):
        self.name = name
        self.surname = surname
        self.email = name + surname + "@ifeisgay.com"
        self.pay = pay

        #  Doesn't edit the object being instantiated, but rather the belonging class
        Employee.num_of_employees += 1

    #  The only argument needed here is self, as self contains all the properties we want
    def get_name(self):
        return self.name, self.surname

    def get_email(self):
        return self.email

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_multiplier)


emp_1 = Employee('Ife', 'Chinweze', 100)
emp_2 = Employee('Adel', 'Haddad', 1000)

#  If we reference get_name as a method belonging to a particular object, we don't need to specify the object
print(emp_1.get_name())
#  If we reference get name as a method from the class itself, we have to specify the particular object
#  Note that under the hood, emp_1.get_name() gets broken down to this format anyway
print(Employee.get_name(emp_1))

print("\n--------------------------------\n")

print(Employee.raise_multiplier, emp_1.raise_multiplier, emp_2.raise_multiplier)
#  Change variable specific to all object of this class
Employee.raise_multiplier = 1.07
print(Employee.raise_multiplier, emp_1.raise_multiplier, emp_2.raise_multiplier)
#  Change variable specific to a particular object
emp_1.raise_multiplier = 1.10
print(Employee.raise_multiplier, emp_1.raise_multiplier, emp_2.raise_multiplier)

print("\n--------------------------------\n")

#  Everything in python is just packaged as a dictionary, with attributes:value/locations in memory
print(Employee.__dict__)
print(Employee.__dict__['get_name'](emp_1))
