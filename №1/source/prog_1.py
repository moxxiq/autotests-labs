def closer(A, B):
    c = []
    if A[0]**2 + A[1]**2 < B[0]**2 + B[1]**2:
        c.append(A)
    if A[0]**2 + A[1]**2 > B[0]**2 + B[1]**2:
        c.append(B)
    return c


def fl_input(message):
    isCorrect = False
    while not isCorrect:
        try:
            fl = float(input(message))
        except ValueError:
            print("Невірний формат вводу")
        else:
            isCorrect = True
    return fl


if __name__ == '__main__':
    print("Визначення точки з ")
    print("Введіть дані точки А (х1, у1)")
    x1 = fl_input("x1 = ")
    y1 = fl_input("y1 = ")
    print("Введіть дані точки B (х2, у2)")
    x2 = fl_input("x2 = ")
    y2 = fl_input("y2 = ")
    c = closer((x1, y1), (x2, y2))
    if len(c) == 0:
        print("Точки знаходяться на однаковій відстані")
    else:
        print(f"Точка з координатами {c[0]}\
         знадиться ближче до початку координат")
