# -*- coding: utf-8 -*-
"""
Программа для кодирования и декодирования текста алгоритмом Фано
В соответствии с алгоритмом из слайдов
"""

import os
import json

# Глобальные переменные для хранения кодов
codes_dict = {}  # массив кодов (как в слайдах C)
reverse_codes_dict = {}  # код -> символ
probabilities_list = []  # массив вероятностей (как в слайдах P)


def calculate_frequencies(text):
    """Вычисляет частоты символов в тексте (подготовка массива P)"""
    if not text:
        return []

    # Считаем символы
    char_count = {}
    for char in text:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1

    # Переводим в вероятности и сортируем по убыванию
    total_chars = len(text)
    frequencies = []
    for char, count in char_count.items():
        probability = count / total_chars
        frequencies.append((char, probability))

    # Сортируем по убыванию частоты (как в слайдах)
    frequencies.sort(key=lambda x: x[1], reverse=True)
    return frequencies



def Med(start, stop):

    """
        Функция Med - находит индекс медианы
        Вход: start - начало части массива P, stop - конец части массива P
        Выход: m - индекс медианы
    """
    global probabilities_list

    if stop <= start:
        return start

    # Вычисляем общую сумму
    total = 0.0
    for i in range(start, stop + 1):
        total += probabilities_list[i][1]

    # Ищем оптимальное разделение
    left_sum = 0.0
    best_diff = float('inf')
    best_index = start

    for i in range(start, stop + 1):
        left_sum += probabilities_list[i][1]
        right_sum = total - left_sum
        current_diff = abs(left_sum - right_sum)

        if current_diff < best_diff - 1e-10:
            best_diff = current_diff
            best_index = i
        else:
            # Когда разница начинает увеличиваться - останавливаемся
            break

    return best_index



def Fano(start, stop, current_code=""):
    """
    ИСПРАВЛЕННАЯ ВЕРСИЯ - правильный алгоритм Фано
    """
    global codes_dict, probabilities_list

    if stop < start:
        return


    if start == stop:
        # Базовый случай: один символ - присваиваем код!
        char = probabilities_list[start][0]
        codes_dict[char] = current_code if current_code else "0"
        print(f"📌 Символу '{char}' присвоен код: {codes_dict[char]}")
        return

    # Находим точку разделения
    m = Med(start, stop)

    # Левая часть получает '0'
    left_code = current_code + "0"
    # Правая часть получает '1'
    right_code = current_code + "1"

    # Рекурсивно обрабатываем обе части
    Fano(start, m, left_code)
    Fano(m + 1, stop, right_code)

def encode_text(text):
    """Кодирует текст используя коды Фано"""
    global codes_dict

    if not text:
        return ""

    result_bits = ""
    for char in text:
        if char in codes_dict:
            result_bits += codes_dict[char]
        else:
            print(f"Внимание: символ '{char}' не имеет кода!")
            result_bits += "?"  # заглушка

    return result_bits


def decode_text(encoded_bits):
    """Декодирует битовую строку обратно в текст"""
    global reverse_codes_dict

    if not encoded_bits:
        return ""

    result_text = ""
    current_code = ""

    for bit in encoded_bits:
        current_code += bit
        if current_code in reverse_codes_dict:
            result_text += reverse_codes_dict[current_code]
            current_code = ""

    if current_code:
        print(f"Внимание: остались нераскодированные биты: {current_code}")

    return result_text


def print_codes_table():
    """Показывает таблицу с кодами Фано"""
    global codes_dict, probabilities_list

    if not codes_dict:
        print("Коды еще не построены!")
        return

    print("\n" + "=" * 60)
    print("ТАБЛИЦА КОДОВ ФАНО")
    print("=" * 60)
    print("Символ  |  Вероятность  | Код         | Длина")
    print("-" * 60)

    # Сортируем по длине кода для красивого вывода
    codes_list = []
    for char, code in codes_dict.items():
        # Находим вероятность для этого символа
        prob = 0
        for c, p in probabilities_list:
            if c == char:
                prob = p
                break
        codes_list.append((char, prob, code, len(code)))

    codes_list.sort(key=lambda x: (x[3], x[2]))

    for char, prob, code, length in codes_list:
        # Форматируем вывод специальных символов
        if char == '\n':
            char_display = "\\n"
        elif char == '\t':
            char_display = "\\t"
        elif char == '\r':
            char_display = "\\r"
        elif char == ' ':
            char_display = "space"
        else:
            char_display = char

        print(f"{char_display:6}  | {prob:10.6f}  | {code:10}  | {length}")

    print("-" * 60)


def compare_with_ascii(original_text):
    """Сравнивает с обычным ASCII-кодированием"""
    if not original_text:
        return

    # ASCII использует 7 бит на символ
    ascii_bits = len(original_text) * 7
    fano_bits = len(encode_text(original_text))

    saved_bits = ascii_bits - fano_bits
    efficiency = (saved_bits / ascii_bits) * 100 if ascii_bits > 0 else 0

    print("\nСРАВНЕНИЕ С ASCII:")
    print(f"Исходный текст: {len(original_text)} символов")
    print(f"ASCII (7 бит/символ): {ascii_bits} бит")
    print(f"Фано: {fano_bits} бит")
    print(f"Экономия: {saved_bits} бит ({efficiency:.1f}%)")

    return efficiency


def read_file(filename):
    """Читает содержимое файла"""
    try:
        encodings = ['utf-8', 'cp1251', 'latin-1']
        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    content =  f.read()
                return content
            except UnicodeDecodeError:
                continue
        print(f"Не удалось прочитать файл {filename}")
        return ""
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return ""


def write_file(filename, content):
    """Записывает содержимое в файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Успешно записано: {filename}")
        return True
    except Exception as e:
        print(f"Ошибка при записи: {e}")
        return False


def save_codes_to_file(filename):
    """Сохраняет коды в файл"""
    global codes_dict, probabilities_list
    try:
        data = {'codes': codes_dict, 'frequencies': probabilities_list}
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        print(f"Коды сохранены: {filename}")
        return True
    except Exception as e:
        print(f"Ошибка сохранения кодов: {e}")
        return False


def load_codes_from_file(filename):
    """Загружает коды из файла"""
    global codes_dict, reverse_codes_dict, probabilities_list
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        codes_dict = data['codes']
        probabilities_list = data['frequencies']
        reverse_codes_dict = {v: k for k, v in codes_dict.items()}
        print(f"Коды загружены: {filename}")
        return True
    except Exception as e:
        print(f"Ошибка загрузки кодов: {e}")
        return False


def get_file_path(filename, extension):
    """Создает путь к файлу в той же директории"""
    base_name = os.path.splitext(filename)[0]
    return f"{base_name}{extension}"


def show_files_in_directory():
    """Показывает файлы в текущей директории"""
    print("\n📁 ФАЙЛЫ В ТЕКУЩЕЙ ПАПКЕ:")
    for file in os.listdir():
        if os.path.isfile(file):
            size = os.path.getsize(file)
            print(f"  {file} ({size} байт)")


def main():
    """Главная функция программы"""
    global codes_dict, probabilities_list, reverse_codes_dict

    print("АЛГОРИТМ ФАНО")
    print("=" * 50)

    while True:
        print("\n" + "=" * 50)
        print("ВЫБЕРИТЕ ДЕЙСТВИЕ:")
        print("1. Закодировать файл")
        print("2. Декодировать файл")
        print("3. Показать файлы в папке")
        print("4. Выйти")

        choice = input("Ваш выбор (1-4): ").strip()

        if choice == '1':
            filename = input("Введите имя файла для кодирования: ").strip()
            text = read_file(filename)
            #if not text:
                #continue

            # Добавляем проверку на пустой файл
            if text is None:
                continue
            elif text == "":
                print("❌ Файл пустой! Кодирование невозможно.")
                continue

            # Инициализируем глобальные переменные
            codes_dict = {}
            reverse_codes_dict = {}
            probabilities_list = calculate_frequencies(text)

            print("Строим коды Фано...")
            Fano(0, len(probabilities_list) - 1, "") # запускаем алгоритм Фано

            print_codes_table()
            encoded = encode_text(text)

            encoded_file = get_file_path(filename, "_encoded.bin")
            codes_file = get_file_path(filename, "_codes.json")

            write_file(encoded_file, encoded)
            save_codes_to_file(codes_file)
            compare_with_ascii(text)

            print(f"\n✅ Кодирование завершено!")
            print(f"Созданы файлы: {encoded_file}, {codes_file}")


        elif choice == '2':
            bin_file = input("Введите имя .bin файла: ").strip()

            # Проверяем сразу существует ли .bin файл
            if not os.path.exists(bin_file):
                print(f"❌ Файл {bin_file} не найден!")
                print("Доступные .bin файлы в папке:")
                for file in os.listdir():
                    if file.endswith('.bin'):
                        print(f"  - {file}")
                continue  # возвращаемся в меню

                # Пробуем найти файл кодов автоматически
            codes_file = get_file_path(bin_file, "_codes.json")

            if not os.path.exists(codes_file):
                print("Доступные файлы с кодами:")
                for file in os.listdir():
                    if file.endswith('_codes.json'):
                        print(f"  - {file}")

                codes_file = input("Введите полное имя файла с кодами: ").strip()

                # Проверяем еще раз
                if not os.path.exists(codes_file):
                    print("❌ Файл с кодами не найден! Возможно:")
                    print("1. Файл был удален")
                    print("2. Файл имеет другое имя")
                    print("3. Кодирование не было завершено")
                    continue

            if not load_codes_from_file(codes_file):
                continue

            encoded_text = read_file(bin_file)
            if not encoded_text:
                continue

            decoded = decode_text(encoded_text)
            output_file = get_file_path(bin_file, "_decoded.txt")

            if write_file(output_file, decoded):
                print(f"✅ Декодировано {len(decoded)} символов")


        elif choice == '3':
            show_files_in_directory()

        elif choice == '4':
            print("Выход из программы")
            break

        else:
            print("Неверный выбор! Попробуйте еще раз.")


if __name__ == "__main__":
    main()










