arr = input("������ �������� ������ ����� �����\n").split()
arr = arr[-1:] + arr[:-1]
print(*arr)
