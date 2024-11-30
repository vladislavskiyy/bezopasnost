import os
import psutil
import json
import xml.etree.ElementTree as ET
import zipfile

def clear_screen():
    os.system('cls')

def show_drive_info():
    clear_screen()
    print("Информация о дисках:")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"Диск: {partition.device}")
            print(f"  Тип файловой системы: {partition.fstype}")
            print(f"  Общий объем: {usage.total / (1024 ** 3):.2f} ГБ")
            print(f"  Свободное место: {usage.free / (1024 ** 3):.2f} ГБ")
            print(f"  Метка тома: {partition.mountpoint}")
        except PermissionError:
            print(f"Ошибка при чтении информации о диске {partition.device}: Доступ запрещен")
        except Exception as e:
            print(f"Ошибка при получении информации о диске {partition.device}: {e}")
    input("\nНажмите Enter, чтобы вернуться в меню.")

def file_operations():
    while True:
        clear_screen()
        print("Операции с файлами")
        print("1. Создать файл")
        print("2. Записать в файл")
        print("3. Прочитать файл")
        print("4. Удалить файл")
        print("5. Вернуться в главное меню")
        choice = input("Введите ваш выбор (1-5): ")

        if choice == '1':
            clear_screen()
            filename = input("Введите имя файла для создания (с расширением): ")
            if os.path.exists(filename):
                print(f"Файл '{filename}' уже существует.")
            else:
                try:
                    with open(filename, 'w') as file:
                        print(f"Файл '{filename}' успешно создан.")
                except Exception as e:
                    print(f"Ошибка при создании файла '{filename}': {e}")
            input("\nНажмите Enter, чтобы продолжить.")
        elif choice == '2':
            clear_screen()
            filename = input("Введите имя файла для записи (с расширением): ")
            if os.path.exists(filename):
                content = input("Введите содержимое для записи: ")
                try:
                    with open(filename, 'w') as file:
                        file.write(content)
                    print(f"Содержимое записано в файл '{filename}'.")
                except Exception as e:
                    print(f"Ошибка при записи в файл '{filename}': {e}")
            else:
                print(f"Файл '{filename}' не существует.")
            input("\nНажмите Enter, чтобы продолжить.")
        elif choice == '3':
            clear_screen()
            filename = input("Введите имя файла для чтения (с расширением): ")
            try:
                with open(filename, 'r') as file:
                    content = file.read()
                    print(f"Содержимое файла '{filename}':\n{content}")
            except FileNotFoundError:
                print(f"Файл '{filename}' не найден.")
            except Exception as e:
                print(f"Ошибка при чтении файла '{filename}': {e}")
            input("\nНажмите Enter, чтобы продолжить.")
        elif choice == '4':
            clear_screen()
            filename = input("Введите имя файла для удаления (с расширением): ")
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                    print(f"Файл '{filename}' успешно удален.")
                else:
                    print(f"Файл '{filename}' не существует.")
            except Exception as e:
                print(f"Ошибка при удалении файла '{filename}': {e}")
            input("\nНажмите Enter, чтобы продолжить.")
        elif choice == '5':
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 5.")
            input("\nНажмите Enter, чтобы продолжить.")

def json_operations():
    while True:
        clear_screen()
        print("Операции с JSON-файлами")
        print("1. Создать JSON-файл")
        print("2. Сериализовать объект в JSON и записать в файл")
        print("3. Прочитать JSON-файл")
        print("4. Удалить JSON-файл")
        print("5. Вернуться в главное меню")
        choice = input("Введите ваш выбор (1-5): ")

        if choice == '1':
            clear_screen()
            filename = input("Введите имя JSON-файла для создания (с расширением): ")
            if os.path.exists(filename):
                print(f"JSON-файл '{filename}' уже существует.")
            else:
                try:
                    with open(filename, 'w') as file:
                        print(f"JSON-файл '{filename}' успешно создан.")
                except Exception as e:
                    print(f"Ошибка при создании JSON-файла '{filename}': {e}")
            input("\nНажмите Enter, чтобы продолжить.")
        elif choice == '2':
            clear_screen()
            filename = input("Введите имя JSON-файла для записи (с расширением): ")
            if os.path.exists(filename):
                try:
                    with open(filename, 'r') as file:
                        try:
                            data = json.load(file)
                        except json.JSONDecodeError:
                            data = {}
                    key = input("Введите ключ: ")
                    value = input("Введите значение: ")
                    data[key] = value
                    with open(filename, 'w') as file:
                        json.dump(data, file, indent=4)
                    print(f"Данные в формате JSON записаны в файл '{filename}'.")
                except Exception as e:
                    print(f"Ошибка при записи в JSON-файл '{filename}': {e}")
            else:
                print(f"Файл '{filename}' не существует.")
            input("\nНажмите Enter, чтобы продолжить.")
        elif choice == '3':
            clear_screen()
            filename = input("Введите имя JSON-файла для чтения (с расширением): ")
            try:
                with open(filename, 'r') as file:
                    data = json.load(file)
                    print(f"Содержимое файла '{filename}':\n{json.dumps(data, indent=4)}")
            except FileNotFoundError:
                print(f"Файл '{filename}' не найден.")
            except json.JSONDecodeError:
                print(f"Ошибка декодирования JSON в файле '{filename}'.")
            except Exception as e:
                print(f"Ошибка при чтении JSON-файла '{filename}': {e}")
            input("\nНажмите Enter, чтобы продолжить.")
        elif choice == '4':
            clear_screen()
            filename = input("Введите имя JSON-файла для удаления (с расширением): ")
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                    print(f"Файл '{filename}' успешно удален.")
                else:
                    print(f"Файл '{filename}' не существует.")
            except Exception as e:
                print(f"Ошибка при удалении файла '{filename}': {e}")
            input("\nНажмите Enter, чтобы продолжить.")
        elif choice == '5':
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 5.")
            input("\nНажмите Enter, чтобы продолжить.")

def xml_operations():
    while True:
        clear_screen()
        print("Операции с XML-файлами")
        print("1. Создать XML-файл")
        print("2. Записать в XML-файл")
        print("3. Прочитать XML-файл")
        print("4. Удалить XML-файл")
        print("5. Вернуться в главное меню")
        choice = input("Введите ваш выбор (1-5): ")

        if choice == '1':
            clear_screen()
            filename = input("Введите имя XML-файла для создания (с расширением): ")
            if os.path.exists(filename):
                print(f"XML-файл '{filename}' уже существует.")
            else:
                try:
                    root = ET.Element("root")  
                    tree = ET.ElementTree(root)  
                    tree.write(filename, encoding='utf-8', xml_declaration=True)  
                    print(f"XML-файл '{filename}' успешно создан.")
                except Exception as e:
                    print(f"Ошибка при создании XML-файла '{filename}': {e}")
            input("\nНажмите Enter, чтобы продолжить.")
        
        elif choice == '2':
            clear_screen()
            filename = input("Введите имя XML-файла для записи (с расширением): ")
            if os.path.exists(filename):
                try:
                    tree = ET.parse(filename)
                    root = tree.getroot()
                except ET.ParseError:
                    print(f"Ошибка: Файл '{filename}' повреждён. Будет создан новый файл.")
                    root = ET.Element("root")
                    tree = ET.ElementTree(root)

                tag = input("Введите имя тега: ")
                text = input("Введите текст для тега: ")
                
                new_element = ET.SubElement(root, tag)
                new_element.text = text

                tree.write(filename, encoding='utf-8', xml_declaration=True)
                print(f"Данные записаны в XML-файл '{filename}'.")
            else:
                print(f"Файл '{filename}' не существует.")
            input("\nНажмите Enter, чтобы продолжить.")
        
        elif choice == '3':
            clear_screen()
            filename = input("Введите имя XML-файла для чтения (с расширением): ")
            try:
                tree = ET.parse(filename)
                root = tree.getroot()
                print(f"Содержимое файла '{filename}':")
                xml_string = ET.tostring(root, encoding='utf-8').decode('utf-8')
                print(xml_string)
                
            except FileNotFoundError:
                print(f"Файл '{filename}' не найден.")
            except ET.ParseError:
                print(f"Ошибка парсинга XML в файле '{filename}'.")
            except Exception as e:
                print(f"Ошибка при чтении XML-файла '{filename}': {e}")
            input("\nНажмите Enter, чтобы продолжить.")

        
        elif choice == '4':
            clear_screen()
            filename = input("Введите имя XML-файла для удаления (с расширением): ")
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                    print(f"Файл '{filename}' успешно удален.")
                else:
                    print(f"Файл '{filename}' не существует.")
            except Exception as e:
                print(f"Ошибка при удалении файла '{filename}': {e}")
            input("\nНажмите Enter, чтобы продолжить.")
        
        elif choice == '5':
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 5.")
            input("\nНажмите Enter, чтобы продолжить.")


def zip_operations():
    while True:
        clear_screen()
        print("Операции с ZIP-архивами")
        print("1. Создать ZIP-архив")
        print("2. Добавить файл в ZIP-архив")
        print("3. Извлечь файлы из ZIP-архива")
        print("4. Удалить ZIP-архив")
        print("5. Вернуться в главное меню")
        choice = input("Введите ваш выбор (1-5): ")

        if choice == '1':
            clear_screen()
            archive_name = input("Введите имя ZIP-архива для создания (с расширением): ")
            if os.path.exists(archive_name):
                print(f"ZIP-архив '{archive_name}' уже существует.")
            else:
                try:
                    with zipfile.ZipFile(archive_name, 'w') as zipf:
                        print(f"ZIP-архив '{archive_name}' успешно создан.")
                except Exception as e:
                    print(f"Ошибка при создании ZIP-архива '{archive_name}': {e}")
            input("\nНажмите Enter, чтобы продолжить.")
        elif choice == '2':
            clear_screen()
            archive_name = input("Введите имя ZIP-архива: ")
            if os.path.exists(archive_name):
                file_to_add = input("Введите имя файла для добавления в архив: ")
                if os.path.exists(file_to_add) and os.path.isfile(file_to_add):
                    try:
                        with zipfile.ZipFile(archive_name, 'a') as zipf:
                            zipf.write(file_to_add, os.path.basename(file_to_add))
                        os.remove(file_to_add)
                        print(f"Файл '{file_to_add}' перемещен в архив '{archive_name}'.")
                    except Exception as e:
                        print(f"Ошибка при добавлении файла в архив: {e}")
                else:
                    print(f"Файл '{file_to_add}' не найден в текущей директории.")
            else:
                print(f"Архив '{archive_name}' не найден.")
            input("\nНажмите Enter, чтобы продолжить.")
        elif choice == '3':
            clear_screen()
            archive_name = input("Введите имя ZIP-архива для извлечения: ")
            if os.path.exists(archive_name):
                try:
                    with zipfile.ZipFile(archive_name, 'r') as zipf:
                        zipf.extractall(os.getcwd())
                        print(f"Архив '{archive_name}' извлечен в текущую директорию.")
                except Exception as e:
                    print(f"Ошибка при извлечении архива: {e}")
            else:
                print(f"Архив '{archive_name}' не найден.")
            input("\nНажмите Enter, чтобы продолжить.")
        elif choice == '4':
            clear_screen()
            archive_name = input("Введите имя ZIP-архива для удаления: ")
            try:
                if os.path.exists(archive_name):
                    os.remove(archive_name)
                    print(f"Архив '{archive_name}' успешно удален.")
                else:
                    print(f"Архив '{archive_name}' не существует.")
            except Exception as e:
                print(f"Ошибка при удалении архива '{archive_name}': {e}")
            input("\nНажмите Enter, чтобы продолжить.")
        elif choice == '5':
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 5.")
            input("\nНажмите Enter, чтобы продолжить.")

def main():
    while True:
        clear_screen()
        print("Главное меню")
        print("1. Показать информацию о дисках")
        print("2. Операции с файлами")
        print("3. Операции с JSON-файлами")
        print("4. Операции с XML-файлами")
        print("5. Операции с ZIP-архивами")
        print("6. Выйти")
        choice = input("Введите ваш выбор (1-6): ")

        if choice == '1':
            show_drive_info()
        elif choice == '2':
            file_operations()
        elif choice == '3':
            json_operations()
        elif choice == '4':
            xml_operations()
        elif choice == '5':
            zip_operations()
        elif choice == '6':
            print("Выход из файлового менеджера.")
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 6.")
            input("\nНажмите Enter, чтобы продолжить.")

if __name__ == "__main__":
    main()
