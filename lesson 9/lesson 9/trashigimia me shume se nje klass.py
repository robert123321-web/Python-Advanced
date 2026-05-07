class Kurrizore:
    def __init__(self, ka_kurriz=True):
        self.ka_kurriz = ka_kurriz


    def info(self):
        print("kafshet kurrizore kane shtylle kurrizore")

class Ujore:
    def __init__(self, habitat = "uje"):
        self.habitat = habitat

    def info(self):
        print("kafshet ujore jetojne ne uje")

class Peshku (Kurrizore,Ujore):

    def __init__(self ,llooji, ka_kurriz=True , habitat="uje"):
        super().__init__(ka_kurriz=ka_kurriz)

        self.habitat=habitat
        self.lloji=lloji

    def info(self):
        print(f"{self.lloji} eshte nje lloj peshku qe jeton ne {self.habitat}")


    def noton(self):
        print("Peshku eshte duke notuar")

peshku = Peshku("Peshku i arte")

print(peshku.ka_kurriz)
print(peshku.habitat)


peshku.info_peshku()
peshku.info_ujore()