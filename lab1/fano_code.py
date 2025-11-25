# -*- coding: utf-8 -*-
"""
Программа для кодирования и декодирования текста алгоритмом Фано
Сохранение закодированных данных ПО БАЙТАМ и сравнение по реальному размеру.
"""

import os
import json

# Глобальные переменные
codes_dict = {}           # символ -> код
reverse_codes_dict = {}   # код -> символ
probabilities_list = []   # список вероятностей (символ, P)


def calculate_frequencies(text):
    """Вычисляет частоты символов в тексте"""
    if not text:
        return []

    char_count = {}
    for char in text:
        char_count[char] = char_count.get(char, 0) + 1

    total_chars = len(text)
    frequencies = [(char, count / total_chars) for char, count in char_count.items()]
    frequencies.sort(key=lambda x: x[1], reverse=True)
    return frequencies


def Med(b, e):
    """Поиск медианы (индекса оптимального разбиения)"""
    global probabilities_list

    if e <= b:
        return b

    total = sum(probabilities_list[i][1] for i in range(b, e + 1))
    left_sum = 0.0
    best_diff = float('inf')
    best_index = b

    for i in range(b, e + 1):
        left_sum += probabilities_list[i][1]
        right_sum = total - left_sum
        diff = abs(left_sum - right_sum)

        if diff < best_diff:
            best_diff, best_index = diff, i
        else:
            break

    return best_index


def Fano(b, e, k=0):
    """Рекурсивный алгоритм Фано"""
    global codes_dict, probabilities_list

    if e <= b:
        return

    current_k = k + 1
    m = Med(b, e)

    for i in range(b, e + 1):
        char = probabilities_list[i][0]
        if char not in codes_dict:
            codes_dict[char] = ""

        while len(codes_dict[char]) < current_k:
            codes_dict[char] += "0"

        if i > m:
            codes_dict[char] = codes_dict[char][:current_k - 1] + "1"
        else:
            codes_dict[char] = codes_dict[char][:current_k - 1] + "0"

    if m > b:
        Fano(b, m, current_k)
    if e > m:
        Fano(m + 1, e, current_k)


def encode_text(text):
    """Кодирует текст в битовую строку"""
    result_bits = ""
    for char in text:
        if char in codes_dict:
            result_bits += codes_dict[char]
        else:
            print(f"Внимание: символ '{char}' не имеет кода!")
    return result_bits


def decode_text(encoded_bits):
    """Декодирует битовую строку"""
    global reverse_codes_dict

    result_text = ""
    current_code = ""

    for bit in encoded_bits:
        current_code += bit
        if current_code in reverse_codes_dict:
            result_text += reverse_codes_dict[current_code]
            current_code = ""

    if current_code:
        print(f"⚠ Остались нераскодированные биты: {current_code}")

    return result_text


def write_binary_file(filename, bitstring):
    """Записывает битовую строку как бинарные байты"""
    try:
        if len(bitstring) % 8 != 0:
            bitstring += '0' * (8 - (len(bitstring) % 8))

        byte_array = bytearray()
        for i in range(0, len(bitstring), 8):
            byte_array.append(int(bitstring[i:i + 8], 2))

        with open(filename, 'wb') as f:
            f.write(byte_array)
        print(f"Успешно записано: {filename}")
        return True
    except Exception as e:
        print(f"Ошибка при бинарной записи: {e}")
        return False


def read_binary_file(filename):
    """Читает бинарный .bin и возвращает битстроку"""
    try:
        with open(filename, 'rb') as f:
            data = f.read()
        return ''.join(f'{byte:08b}' for byte in data)
    except Exception as e:
        print(f"Ошибка при чтении бинарного файла: {e}")
        return None


def print_codes_table():
    """Выводит таблицу кодов"""
    global codes_dict, probabilities_list

    if not codes_dict:
        print("Коды еще не построены!")
        return

    print("\n" + "=" * 60)
    print("ТАБЛИЦА КОДОВ ФАНО")
    print("=" * 60)
    print("Символ  | Вероятность | Код        | Длина")
    print("-" * 60)

    table = []
    for char, code in codes_dict.items():
        prob = next(p for c, p in probabilities_list if c == char)
        table.append((char, prob, code, len(code)))

    table.sort(key=lambda x: (x[3], x[2]))

    for char, prob, code, length in table:
        display = repr(char)[1:-1] if char in ['\n', '\t', '\r', ' '] else char
        print(f"{display:6} | {prob:11.6f} | {code:10} | {length}")

    print("-" * 60)


def compare_with_ascii(original_text, encoded_file, codes_file):
    """Сравнение файлов по байтам"""
    if not original_text:
        return

    ascii_size = len(original_text)        # ASCII = 1 байт на символ
    fano_size = os.path.getsize(encoded_file) + os.path.getsize(codes_file)
    fano_size_encoded = os.path.getsize(encoded_file)

    saved = ascii_size - fano_size
    eff = (saved / ascii_size) * 100 if ascii_size > 0 else 0

    print("\n📊 СРАВНЕНИЕ (в байтах):")
    print(f"Исходный файл: {ascii_size} Б")
    print(f"Фано (данные + коды): {fano_size} Б")
    print(f"Фано (коды): {fano_size_encoded} Б")
    print(f"Экономия: {saved} Б  ({eff:.1f}%)")


def read_file(filename):
    encodings = ['utf-8', 'cp1251', 'latin-1']
    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    return None


def write_file(filename, content):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except:
        return False


def save_codes_to_file(filename):
    global codes_dict, probabilities_list
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({'codes': codes_dict, 'frequencies': probabilities_list}, f, ensure_ascii=False)
        return True
    except:
        return False


def load_codes_from_file(filename):
    global codes_dict, reverse_codes_dict, probabilities_list
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        codes_dict = data['codes']
        probabilities_list = data['frequencies']
        reverse_codes_dict = {v: k for k, v in codes_dict.items()}
        return True
    except:
        return False


def get_file_path(filename, extension):
    base = os.path.splitext(filename)[0]
    return f"{base}{extension}"


def show_files_in_directory():
    print("\n📁 ФАЙЛЫ В ПАПКЕ:")
    for f in os.listdir():
        if os.path.isfile(f):
            print(f"  {f} ({os.path.getsize(f)} Б)")


def main():
    global codes_dict, reverse_codes_dict, probabilities_list

    print("🐍 АЛГОРИТМ ФАНО 🐍")

    while True:
        print("\n1. Закодировать файл")
        print("2. Декодировать файл")
        print("3. Показать файлы")
        print("4. Выход")

        choice = input("Ваш выбор: ").strip()

        if choice == '1':
            filename = input("Введите имя файла: ").strip()
            text = read_file(filename)
            if not text:
                print("Ошибка чтения файла!")
                continue

            codes_dict = {}
            reverse_codes_dict = {}
            probabilities_list = calculate_frequencies(text)

            Fano(0, len(probabilities_list) - 1, 0)

            reverse_codes_dict = {v: k for k, v in codes_dict.items()}

            print_codes_table()
            encoded = encode_text(text)

            encoded_file = get_file_path(filename, "_encoded.bin")
            codes_file = get_file_path(filename, "_codes.json")

            write_binary_file(encoded_file, encoded)
            save_codes_to_file(codes_file)
            compare_with_ascii(text, encoded_file, codes_file)

        elif choice == '2':
            bin_file = input("Введите .bin файл: ").strip()
            if not os.path.exists(bin_file):
                print("Файл не найден!")
                continue

            codes_file = get_file_path(bin_file, "_codes.json")
            if not os.path.exists(codes_file):
                codes_file = input("Введите файл с кодами: ").strip()

            if not load_codes_from_file(codes_file):
                print("Ошибка загрузки кодов!")
                continue

            encoded_text = read_binary_file(bin_file)
            decoded = decode_text(encoded_text)
            out = get_file_path(bin_file, "_decoded.txt")
            write_file(out, decoded)
            print(f"🎉 Декодировано! Сохранено в {out}")

        elif choice == '3':
            show_files_in_directory()

        elif choice == '4':
            print("Завершение.")
            break

        else:
            print("Ошибка! Выберите 1-4.")


if __name__ == "__main__":
    main()










