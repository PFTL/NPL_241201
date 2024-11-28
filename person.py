from student import Student


class Person(Student):
    def calculate_age(self, birth_year):
        print(f"{self.get_full_name()} is {2024-birth_year} years old")

    def __str__(self):
        return f"Person: {self.get_full_name()}"


if __name__ == "__main__":
    another_me = Person('Aquiles', 'Carattino')
    another_me.calculate_age(1986)
    print(another_me)