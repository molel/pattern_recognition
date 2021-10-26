from Class import *


def main():
    classes = [Class("class_A.txt"),
               Class("class_B.txt"),
               Class("class_C.txt"),
               Class("class_D.txt")]
    for class_ in classes:
        print(class_)
    objects = get_objects("objects.txt")
    for obj in objects:
        obj.define_class(classes)


if __name__ == '__main__':
    main()
