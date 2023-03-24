import sys
from karlos import karlos

if __name__ == "__main__":
    with open('karlosArt.txt') as art:
        print(art.read())
        art.close()
    karlos(sys)