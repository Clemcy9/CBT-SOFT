num = 2
def myscope():
    num =3

    def counter():
        for i in range(5):
            nonlocal num
            num += 1
            print(num)
    counter()
myscope()