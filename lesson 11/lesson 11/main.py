
file = open("example.txt","x")

file.close()


with open("example.txt","x") as file:
    content = file.read()
    print(content)

with open("example.txt","w") as file:
    file.write("hello from main")



lista = ["Hello world!\n","Welcome to python!\n"]

with open("example.txt","w") as file:
    file.write(lista)



if os.path.exists("example.txt"):
    print("fajlli ekziston")

if os.path.exists("fds.txt"):
    print("fajlli fds nuk ekziston")



name="Donjeta"
age =354345

with open("output.txt","w") as file:
    file.write("Name:" + name + "\n")
    file.write("Age:" + str(age) + "\n")
