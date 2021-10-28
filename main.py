from Class import *


def main():
    classes = [Class("class_A.txt"),
               Class("class_B.txt"),
               Class("class_C.txt"),
               Class("class_D.txt")]
    for class_ in classes:
        print(class_)
    patterns = get_patterns("patterns_to_define.txt")
    for pattern in patterns:
        pattern.define_class(classes)


if __name__ == '__main__':
    main()
