class Kerri :
    def  __innit__(self,emri,viti,modeli,kilometrat,prejardhje):
        self.emri = emri
        self.viti = viti
        self.modeli = modeli
        self.kilometrat = kilometrat
        self.prejardhje = prejardhje

    def rriteshpejtesin (self):
        print("shpejtesia e kerrit eshte duke u rritur")

    def ndalu(self):
        print("stoop")


    def info(self):
        print(f" {self.emri} , eshte nje veture mjaft luksoze dhe eshte e prodhuar ne vitin: {self.viti}, dhe eshte i prodhuar ne: {self.prejardhja}")