import hashlib
import time
import itertools
import string
from concurrent.futures import ProcessPoolExecutor, as_completed

def get_hashes_from_user():
    print("Введите хэш-значения. Оставьте строку пустой, чтобы закончить ввод:")
    hashes = []
    while True:
        h = input()
        if h == '':
            break
        hashes.append(h.strip().lower())
    return hashes

def get_number_of_processes():
    while True:
        try:
            n = int(input("Введите количество потоков для использования: "))
            if n > 0:
                return n
            else:
                print("Пожалуйста, введите положительное целое число больше 0.")
        except ValueError:
            print("Пожалуйста, введите корректное целое число.")

def get_mode():
    while True:
        mode = input("Выберите режим работы:\n1 - Однопоточный\n2 - Многопоточный\nВведите 1 или 2: ")
        if mode in ['1', '2']:
            return int(mode)
        else:
            print("Пожалуйста, введите 1 или 2.")

def worker(passwords_chunk, target_hashes, hash_type):
    found = {}
    start_time = time.time()
    for pwd in passwords_chunk:
        pwd_str = ''.join(pwd)
        pwd_bytes = pwd_str.encode('utf-8')
        if hash_type == 'md5':
            pwd_hash = hashlib.md5(pwd_bytes).hexdigest()
        else:
            pwd_hash = hashlib.sha256(pwd_bytes).hexdigest()
        if pwd_hash in target_hashes:
            end_time = time.time()
            found[pwd_hash] = (pwd_str, end_time - start_time)
            target_hashes.remove(pwd_hash)
            if not target_hashes:
                break
    return found

def run_single_thread(hashes_to_find):
    found_passwords = {}
    letters = string.ascii_lowercase
    for hash_value in hashes_to_find:
        found = False
        start_time = time.time()
        hash_type = 'md5' if len(hash_value) == 32 else 'sha256'
        for pwd in itertools.product(letters, repeat=5):
            pwd_str = ''.join(pwd)
            pwd_bytes = pwd_str.encode('utf-8')
            if hash_type == 'md5':
                pwd_hash = hashlib.md5(pwd_bytes).hexdigest()
            else:
                pwd_hash = hashlib.sha256(pwd_bytes).hexdigest()
            if pwd_hash == hash_value:
                end_time = time.time()
                found_passwords[hash_value] = (pwd_str, end_time - start_time)
                found = True
                break
        if not found:
            found_passwords[hash_value] = (None, time.time() - start_time)
    return found_passwords

def run_multi_process(num_processes, hashes_to_find):
    letters = string.ascii_lowercase
    total_passwords = 26 ** 5
    chunk_size = total_passwords // num_processes
    found_passwords = {}

    for hash_value in hashes_to_find:
        start_time = time.time()
        target_hashes = set([hash_value])
        hash_type = 'md5' if len(hash_value) == 32 else 'sha256'
        with ProcessPoolExecutor(max_workers=num_processes) as executor:
            futures = []
            iterator = itertools.product(letters, repeat=5)
            while True:
                passwords_chunk = list(itertools.islice(iterator, chunk_size))
                if not passwords_chunk:
                    break
                futures.append(executor.submit(worker, passwords_chunk, target_hashes.copy(), hash_type))
            for future in as_completed(futures):
                result = future.result()
                if result:
                    pwd, time_taken = next(iter(result.values()))
                    found_passwords[hash_value] = (pwd, time_taken)
                    executor.shutdown(wait=False, cancel_futures=True)
                    break
            else:
                found_passwords[hash_value] = (None, time.time() - start_time)
    return found_passwords

def main():
    hashes = get_hashes_from_user()
    if not hashes:
        print("Хэш-значения не введены. Выход из программы.")
        return
    mode = get_mode()

    if mode == 1:
        print("\nОднопоточный режим запуска...")
        found_passwords = run_single_thread(hashes)
    else:
        num_processes = get_number_of_processes()
        print(f"\nМногопоточный режим запуска с {num_processes} потоками...")
        found_passwords = run_multi_process(num_processes, hashes)

    for h in hashes:
        pwd, time_taken = found_passwords[h]
        if pwd:
            print(f"Хэш: {h}\nПароль: {pwd}\nВремя подбора: {time_taken:.2f} секунд(ы)\n")
        else:
            print(f"Хэш: {h}\nПароль не найден. Время, затраченное на перебор: {time_taken:.2f} секунд(ы)\n")

    input("\nНажмите Enter, чтобы выйти...")

if __name__ == "__main__":
    main()
