class Pattern:
    def __init__(self, data: list):
        self.data = data

    def __get__(self, instance, owner):
        return self.data

    def __getitem__(self, item):
        return self.data[item]

    def __len__(self):
        return len(self.data)

    def __str__(self):
        result = ""
        for row in self.data:
            line = "".join([str(el) for el in row])
            result += line + "\n"
        else:
            result += "\n"
        for row in self.data:
            line = "".join([str(el) for el in row])
            result += line.replace("0", " ").replace("1", "█") + "\n"
        else:
            result += "\n"
        return result

    def define_class(self, classes: list):
        print("-" * 40 + "\n")
        print(self)
        distances = dict()
        for class_ in classes:
            distance = class_.find_distance(self)
            print(f"Class {class_.name}: {distance}")
            distances[class_] = distance
        print(f"Object belongs to class {min(distances, key=lambda x: distances[x]).name}\n")
