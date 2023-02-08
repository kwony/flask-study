# class PrintNumber:
#     def __enter__(self):
#         print("start")
#         return self
#     def print_number(self, number):
#         print(f"Number: {number}")

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print("end")

# with PrintNumber() as pn:
#     pn.print_number(42)
#     pn.print_number(10)

# pn.print_number(100)


import time 

# def yield_return():
#     for ch in "ABC":
#         time.sleep(1)
#         print(ch)


# 결과값을 나누어서 얻을 수 있기 때문에 성능상의 이점이 있음
# return 의 경우 모든 결과를 메모리에 한번에 올려야 하는 반면, yield는 결과 값을 하나씩 메모리에 올려 놓는다
def yield_abc():
  for ch in "ABC":
        time.sleep(1)
        yield ch 


# print(yield_return())

for ch in yield_abc():
    print(ch)