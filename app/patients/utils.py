import os
import sys
import django
import pandas as pd
from django.utils import timezone

# Определяем базовый каталог проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # Переходим на уровень выше

# Добавляем пути в sys.path
sys.path.append(PROJECT_ROOT)  # Корень проекта (DendriticCells)
sys.path.append(BASE_DIR)  # Папка app

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

try:
    django.setup()
    print("Django успешно инициализирован")
except Exception as e:
    print(f"Ошибка инициализации Django: {e}")
    sys.exit(1)

from patients.models import Patient


def convert_pd_datetime(value):
    """Конвертирует pandas Timestamp в datetime или возвращает None для NaT"""
    if pd.isna(value) or value is pd.NaT:
        return None
    return value


def convert_pd_num(value):
    """Конвертирует pandas Timestamp в datetime или возвращает None для NaT"""
    if pd.isna(value):
        return None
    return value


def import_patients():
    file_path = os.path.join(PROJECT_ROOT, 'Для Ярослава.xlsx')
    try:
        df = pd.read_excel(file_path)
        print(f"Файл успешно загружен: {file_path}")
        df.info()
    except Exception as e:
        print(f"Ошибка загрузки файла: {e}")
        return

    # Конвертируем даты
    date_columns = ['Год рождения', 'last contact/дата смерти', 'Дата события', 'DateDiag', 'ДАТА операции']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')


    numeric_columns = [
        'stage',
        't',
        'n',
        'm',
        'g',
        'p16',
        'Размер ПО, см',
        'Размер л/У, см',
        'ДК',
        'Нейтрофилы',
        'Лимфоциты',
        'Тромбоциты'
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    patients_to_create = []
    existing_count = 0
    error_count = 0

    for index, row in df.iterrows():
        try:
            # Проверяем обязательное поле
            if pd.isna(row.get('FIO')):
                print(f"Пропуск строки {index}: отсутствует ФИО")
                error_count += 1
                continue

            # Проверяем существование пациента
            if Patient.objects.filter(fio=row['FIO']).exists():
                print(f"Пациент уже существует: {row['FIO']}")
                existing_count += 1
                continue

            # Обработка значений
            dendritic_value = pd.isna(row.get('ДК'))
            cure_order = convert_pd_num(row.get('primary1/recurrent2'))

            patient = Patient(
                fio=row['FIO'],
                birthday=convert_pd_datetime(row.get('Год рождения')),
                sex=convert_pd_num(row.get('sex')),
                cure_order=cure_order,
                actual_date=timezone.now(),
                last_contact_date=convert_pd_datetime(row.get('last contact/дата смерти')),
                statendyr=1,
                prrecid_date=convert_pd_datetime(row.get('Дата события')),
                datediag=convert_pd_datetime(row.get('DateDiag')),
                mkb10=row.get('МКБ-10'),
                txtdiag=row.get('txtdiag'),
                stage=convert_pd_num(row.get('stage')),
                t=convert_pd_num(row.get('t')),
                n=convert_pd_num(row.get('n')),
                m=convert_pd_num(row.get('m')),
                g=convert_pd_num(row.get('g')),
                p16=convert_pd_num(row.get('p16')),
                focus_size=convert_pd_num(row.get('Размер ПО, см')),
                node_size=convert_pd_num(row.get('Размер л/У, см')),
                note_txt=row.get('Возникший процесс'),
                oper_date=convert_pd_datetime(row.get('ДАТА операции')),
                oper_txt=row.get('Текст операции'),
                oper_complications=row.get('Послеоперационные осложнения'),
                dendritic=dendritic_value,
                kindlech_txt=row.get('Вид специального лечения'),
                fk_after=row.get('ФК после'),
                fk_last=row.get('ФК последнее'),
                neut=convert_pd_num(row.get('Нейтрофилы')),
                limph=convert_pd_num(row.get('Лимфоциты')),
                plt=convert_pd_num(row.get('Тромбоциты')),
            )
            patients_to_create.append(patient)
            print(f"Подготовлен пациент: {row['FIO']}")

        except Exception as e:
            print(f"Ошибка в строке {index}: {str(e)}")
            error_count += 1

    # Пакетное сохранение
    if patients_to_create:
        try:
            Patient.objects.bulk_create(patients_to_create, batch_size=100)
            print(f"Успешно создано {len(patients_to_create)} новых пациентов")
        except Exception as e:
            print(f"Ошибка при пакетном сохранении: {str(e)}")
            error_count += len(patients_to_create)

    print("\nИтоги импорта:")
    print(f"- Новых пациентов: {len(patients_to_create)}")
    print(f"- Уже существует: {existing_count}")
    print(f"- Ошибки: {error_count}")


if __name__ == '__main__':
    import_patients()