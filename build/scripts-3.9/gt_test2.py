import sys
import os
print(os.listdir())
import GeneralTools.annotationTools.createVanillaGFF


def main(item):
    print("In gt_test2!")
    print(len(str(item)))


if __name__ == '__main__':
    main(sys.argv[1])
