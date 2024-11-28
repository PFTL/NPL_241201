class Student:
    def __init__(self, name, last_name):
        self.name = name
        self.last_name = last_name

    def get_full_name(self):
        full_name = self.name + ' ' + self.last_name
        return full_name

    def __str__(self):
        return f"Student {self.get_full_name()}"


if __name__ == '__main__':
    me = Student('Aquiles', 'Carattino')
    print(me.name)
    print(me.last_name)
    print(me.get_full_name())
    print(me)

    you = Student('John', 'Smith')
    print(you.name)
    print(you.last_name)