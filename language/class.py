class Someclass:
    # 생성자임
    def __init__(self, name: str = 'default'):
        # 생성자 내에 클래스 변수를 추가 가능
        self._name = name
        self._age = 10
      
    def hello(self):
        print(f"hello world: {self._name} age: {self._age}")

    def age(self):
        print(f"hello world: age: {self._age}")
        self.__private_age()

    # private 함수
    def __private_age(self):
        private_age = self._age + 3
        print(f"private_page {private_age}")


a = Someclass()

a.hello()
a.age()