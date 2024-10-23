# file_actions.py

# Открыть файл example.txt на чтение (аргумент 'r').
file = open('example.txt', 'r')
# Прочитать первые 12 символов из файла и сохранить их в переменную content.
content = file.read(12)
# Вывести на печать содержимое переменной content.
print(content)
# Закрыть файл.
file.close() 