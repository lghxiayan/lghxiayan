class User:
    def __init__(self, first_name: str, last_name: str, age: int, sex: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.sex = sex
        self.login_attempts = 0

    def describe_user(self) -> None:
        print(f"{self.first_name} {self.last_name} {self.age} {self.sex}")

    def greet_user(self) -> None:
        print(f"{self.first_name} {self.last_name} hello")

    def increment_login_attempts(self) -> None:
        self.login_attempts += 1
        print(f"{self.first_name}  {self.last_name} now loging: {self.login_attempts}")

    def reset_login_attempts(self) -> None:
        self.login_attempts = 0
        print(f"{self.first_name} {self.last_name} now has reset {self.login_attempts}")


def main():
    user1 = User('lgh1', 'lgh2', 20, 'male')
    user1.describe_user()
    user1.greet_user()
    user1.increment_login_attempts()
    user1.increment_login_attempts()
    user1.increment_login_attempts()
    user1.increment_login_attempts()
    user1.reset_login_attempts()


if __name__ == '__main__':
    main()
