"""
data <=> attributes
functions <=> methods
"""


class Employee:

    #  Default constructor
    # def __innit__(self):
    #     self.name = "None set"
    #     self.surname = "None set"
    #     self.email = "None set"

    #  Constructor in python, assigns attributes to objects
    def __innit__(self, name, surname):
        self.name = name
        self.surname = surname
        self.email = name + surname + "@ifeisgay.com"

    #  The only argument needed here is self, as self contains all the properties we want
    def get_name(self):
        return self.name, self.surname

    def get_email(self):
        return self.email


emp_1 = Employee('Ife', 'Chinweze')

#  If we reference get_name as a method belonging to a particular object, we don't need to specify the object
print(emp_1.get_name())
#  If we reference get name as a method from the class itself, we have to specify the particular object
#  Note that under the hood, emp_1.get_name() gets broken down to this format anyway
print(Employee.get_name(emp_1))
