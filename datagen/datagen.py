import random

def randgen(row:int, col:int, rand_size:tuple) -> None:
    with open('datagen/rand.txt', 'w') as file:
        for _ in range(row):
            s = str()
            for _ in range(col):
                s += " " + str(random.randint(rand_size[0], rand_size[1]))
            file.write(s.strip() + "\n")

def symmetricgen(row:int, col:int, rand_size:tuple) -> None:
    metrix = dict()
    for i in range(row):
        for j in range(col):
            if i == j:
                metrix[(i,j)] = 0
            elif i < j:
                metrix[(i,j)] = random.randint(rand_size[0], rand_size[1])
            elif i > j:
                metrix[(i,j)] = metrix[(j,i)]
    with open('datagen/rand.txt', 'w') as file:
        s = str()
        for j in range(col):
            s = " ".join([str(metrix[(i,j)]) for i in range(row)])
            file.write(s.strip() + "\n")

if __name__ == "__main__":
    randgen(100, 1, (1,2))
    # symmetricgen(100, 100, (1,9))
