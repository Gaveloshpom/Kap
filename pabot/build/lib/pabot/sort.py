import os
import re
import shutil


# Створюємо словник для транслітерації
trans_dict = {1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd',
              1044: 'D', 1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z',
              1080: 'i', 1048: 'I', 1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm',
              1052: 'M', 1085: 'n', 1053: 'N', 1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R',
              1089: 's', 1057: 'S', 1090: 't', 1058: 'T', 1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h',
              1061: 'H', 1094: 'ts', 1062: 'TS', 1095: 'ch', 1063: 'CH', 1096: 'sh', 1064: 'SH', 1097: 'sch',
              1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '', 1101: 'e', 1069: 'E',
              1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je', 1028: 'JE', 1110: 'i', 1030: 'I', 1111: 'ji',
              1031: 'JI', 1169: 'g', 1168: 'G'}

# Строка для ітерації по символам кирилиці
cyrillic = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"


def normalize(name: str):
    # Функція, що проводить нормалізацію, але не розрізняє розширення
    tmp = []
    for el in name:
        if el in cyrillic or el in cyrillic.upper():
            tmp.append(el.translate(trans_dict))
        elif el.isalpha() or el.isdecimal():
            tmp.append(el)
        else:
            tmp.append("_")
    return "".join(tmp)


def rename_file(path: str, filename: str, suff: str):
    """
     Функція переіменовує файл. Приймає повний шлях до файлу, назву файлу (з розширенням) і розширення файлу.
     Повертає новий шлях до переіменованого файлу і нову назву файлу (з розширенням).
    """
    name = filename.removesuffix(suff)
    name = normalize(name)
    os.rename(os.path.join(path, filename), os.path.join(path, f"{name}{suff}"))
    return os.path.join(path, f"{name}{suff}"), f"{name}{suff}"


def ultimate_paths(path: str):
    """
    Повертає повні шляхи до директорій, в які сортуємо файли з основної папки.
    """
    return os.path.join(path, "images"), os.path.join(path, "video"), os.path.join(path, "documents"), \
        os.path.join(path, "audio"), os.path.join(path, "archives")


# Створюємо словник, для утримання всіх відомих і невідомих форматів файлів і їх назв
all_files = {
        "images": {".png": [], ".jpg": [], ".jpeg": [], ".svg": []},
        "video": {".avi": [], ".mp4": [], ".mov": [], ".mkv": []},
        "documents": {'.doc': [], '.docx': [], '.txt': [], '.pdf': [], '.xlsx': [], '.pptx': []},
        "audio": {'.mp3': [], '.ogg': [], '.wav': [], '.amr': []},
        "archives": {'.zip': [], '.gz': [], '.tar': []},
        "other": {}
    }


def sort_file(filename: str, path: str, images: str, video: str, documents: str, audio: str, archives: str):
    """
        Перевіряємо чи є поточний елемент файлом. Якщо так - створюємо окрему змінну для розширення цього файлу.
        Якщо розширення не існує - пропускаємо. Шукаємо розширення серед списку відомих нам розширень.

        Якщо це архів - переіменовуємо, розпаковуємо в новостворену папку і видаляємо оригінал.
        Додаємо до словника.

        Якщо відоме розширення - переіменовуємо, додаємо до словника інформацію про файл і сортуємо в відповідну
        директорію.

        Якщо розширення невідоме - створюємо новий елемент словника для утримання інформації про файл.
        Файл переіменовуємо, але не сортуємо.
    """
    tmp = re.findall(r"\.\w{2,}", filename)
    if not tmp:
        return
    tmp = tmp[-1]
    if tmp.lower() in ['.png', '.jpg', '.jpeg', '.svg']:
        abs_path, renamed = rename_file(path, filename, tmp)
        all_files["images"][tmp.lower()].append(renamed)
        shutil.move(abs_path, images)
    elif tmp.lower() in [".avi", ".mp4", ".mov", ".mkv"]:
        abs_path, renamed = rename_file(path, filename, tmp)
        all_files["video"][tmp.lower()].append(filename)
        shutil.move(abs_path, video)
    elif tmp.lower() in ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx']:
        abs_path, renamed = rename_file(path, filename, tmp)
        all_files["documents"][tmp.lower()].append(filename)
        shutil.move(abs_path, documents)
    elif tmp.lower() in ['.mp3', '.ogg', '.wav', '.amr']:
        abs_path, renamed = rename_file(path, filename, tmp)
        all_files["audio"][tmp.lower()].append(filename)
        shutil.move(abs_path, audio)
    elif tmp.lower() in ['.zip', '.gz', '.tar']:
        abs_path, renamed = rename_file(path, filename, tmp)
        all_files["archives"][tmp.lower()].append(renamed)
        new_dir = os.path.join(archives, renamed.removesuffix(tmp))
        os.mkdir(new_dir)
        shutil.unpack_archive(abs_path, new_dir, tmp[1:])
        os.remove(abs_path)
    elif tmp in all_files["other"].keys():
        abs_path, renamed = rename_file(path, filename, tmp)
        all_files["other"][tmp].append(renamed)
    else:
        abs_path, renamed = rename_file(path, filename, tmp)
        all_files["other"][tmp] = [renamed, ]


def sort_dir(path: str, images: str, video: str, documents: str, audio: str, archives: str):
    """
        Функція для сортування файлів у директорії. Приймає шлях до цієї самої директорії.
        Викликає сама себе.
    """
    for filename in os.listdir(path):
        # Ітеруємо по всіх елементах директорії (файлам і папкам)
        if filename in all_files.keys():
            # Перевіряємо чи є поточна папка серед папок, в які проводимо сортування. Пропусаємо, якщо так.
            continue
        abs_path = os.path.join(path, filename)  # Створюємо повний шлях до поточного елемента

        if os.path.isdir(abs_path):
            # Якщо дирокторія пуста - видаляємо. Якщо ні - переіменовуємо і рекурсивно викликаємо знову.
            if not os.listdir(abs_path):
                os.rmdir(abs_path)
            else:
                renamed = normalize(filename)
                renamed = os.path.join(path, renamed)
                os.rename(abs_path, renamed)
                sort_dir(renamed, images, video, documents, audio, archives)

        elif os.path.isfile(abs_path):
            sort_file(filename, path, images, video, documents, audio, archives)

    # Кінець роботи. Функція нічого не повертає.


def remove_empty_dir(path: str, images: str, video: str, documents: str, audio: str, archives: str):
    """
        Ітеруємо по елементам основної папки знизу вверх. Виклик відбуваєть вже після сортування.
        Намагаємося видалити папки. Якщо папка не пуста - пропускаємо її.
    """
    for dir_path, _, _ in os.walk(path, topdown=False):
        if dir_path in [images, video, documents, audio, archives]:
            continue
        if dir_path == path:
            break
        try:
            os.rmdir(dir_path)
        except OSError:
            continue


def create_sorting_dir(categories: list[str]):
    """
        Створюємо підтеки, якщо вони ще не існують.
    """
    for elem in categories:
        if not os.path.exists(elem):
            os.mkdir(elem)


def print_results():
    # Функція для виводу результатів. Показує назву всіх файлів у кожній категорії і їх кількість.
    for category in all_files.keys():
        for keys, vals in all_files[category].items():
            if not vals:
                continue
            print(f"{category: <7}: {keys: <8}  |  {'Number of files': >8}:{len(vals): >2}")
            for val in vals:
                print("{:~^10}".format(val), end="     ")
            print("\n..................................................................\n")


def sort_files(data: str):
    main_path = data.strip()  # Виклик всіх функцій, що виконують програму. Запускається через командну строку
    if not os.path.isdir(main_path):
        return "Path doesn't lead to a directory."
    images, video, documents, audio, archives = ultimate_paths(main_path)
    create_sorting_dir([images, video, documents, audio, archives])
    sort_dir(main_path, images, video, documents, audio, archives)
    remove_empty_dir(main_path, images, video, documents, audio, archives)
    print_results()
    return "Sorting completed.\n"
