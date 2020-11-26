arr = input("Введіть елементи масиву через пробіл\n").split()
arr = arr[-1:] + arr[:-1]
print(*arr)
