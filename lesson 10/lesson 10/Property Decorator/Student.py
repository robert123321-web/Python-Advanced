


class Student :

    def __init__(self, name , age):
        self.__name = name
        self.__age = age



    @property
    def name(self):
        return self.__name


    @property
    def age(self):
        return self.__age


    @name.setter
    def age(self,name):
        self.__name=name

    @age.setter
    def age(self,age):
        self.__age=age




studenti1 = Student("Edeni", 17)

print(studenti1.name)
print(studenti1.age)

studenti1.name = "Driarti"
studenti1.age = 15

print(studenti1.name)
print(studenti1.age)
