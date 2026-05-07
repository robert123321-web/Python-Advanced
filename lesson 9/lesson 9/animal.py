class Animal:

    def sound(self):
        print("sound of the animal")


class Dog(Animal)   :

    def sound(self):
        print("woof! woof!")


class Cat(Animal):

    def sound(self):
        print("meow meoww")


animal1 = Animal()
aniaml1.sound()


animal2 = Dog()
animal2.sound()

animal3 = Cat()
animal3.sound()