import os
import json
import datetime
import csv


# Вспомогательные функции для загрузки и сохранения данных
def load_data(file_path, default_data):
    if not os.path.exists(file_path):
        save_data(file_path, default_data)
        return default_data
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ----- Модуль заметок -----
NOTES_FILE = 'notes.json'


class Note:
    def __init__(self, note_id, title, content, timestamp):
        self.id = note_id
        self.title = title
        self.content = content
        self.timestamp = timestamp


class NoteManager:
    def __init__(self):
        self.notes = []
        self.load_notes()

    def load_notes(self):
        data = load_data(NOTES_FILE, [])
        self.notes = [Note(**note) for note in data]

    def save_notes(self):
        data = [note.__dict__ for note in self.notes]
        save_data(NOTES_FILE, data)

    def add_note(self, title, content):
        note_id = max([note.id for note in self.notes], default=0) + 1
        timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        new_note = Note(note_id, title, content, timestamp)
        self.notes.append(new_note)
        self.save_notes()
        print('Заметка успешно добавлена!')

    def list_notes(self):
        if not self.notes:
            print('Список заметок пуст.')
            return
        for note in self.notes:
            print(f'{note.id}. {note.title} (дата: {note.timestamp})')

    def view_note(self, note_id):
        note = self.get_note_by_id(note_id)
        if note:
            print(f'Заголовок: {note.title}')
            print(f'Содержимое: {note.content}')
            print(f'Дата создания/изменения: {note.timestamp}')
        else:
            print('Заметка не найдена.')

    def edit_note(self, note_id, new_title, new_content):
        note = self.get_note_by_id(note_id)
        if note:
            note.title = new_title
            note.content = new_content
            note.timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.save_notes()
            print('Заметка успешно обновлена!')
        else:
            print('Заметка не найдена.')

    def delete_note(self, note_id):
        note = self.get_note_by_id(note_id)
        if note:
            self.notes.remove(note)
            self.save_notes()
            print('Заметка успешно удалена!')
        else:
            print('Заметка не найдена.')

    def get_note_by_id(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                return note
        return None

    def export_notes_to_csv(self):
        if not self.notes:
            print('Список заметок пуст.')
            return
        file_name = 'notes_export.csv'
        with open(file_name, mode='w', encoding='utf-8', newline='') as csv_file:
            fieldnames = ['ID', 'Заголовок', 'Содержимое', 'Дата']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for note in self.notes:
                writer.writerow({
                    'ID': note.id,
                    'Заголовок': note.title,
                    'Содержимое': note.content,
                    'Дата': note.timestamp
                })
        print(f'Заметки успешно экспортированы в файл {file_name}')

    def import_notes_from_csv(self):
        file_name = input('Введите имя CSV-файла для импорта: ')
        if not os.path.exists(file_name):
            print('Файл не найден.')
            return
        with open(file_name, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                note_id = max([note.id for note in self.notes], default=0) + 1
                title = row.get('Заголовок', '')
                content = row.get('Содержимое', '')
                timestamp = row.get('Дата', datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
                new_note = Note(note_id, title, content, timestamp)
                self.notes.append(new_note)
            self.save_notes()
        print('Заметки успешно импортированы из CSV-файла.')


def notes_menu():
    manager = NoteManager()
    while True:
        print('\nУправление заметками:')
        print('1. Добавить новую заметку')
        print('2. Просмотреть список заметок')
        print('3. Просмотреть заметку')
        print('4. Редактировать заметку')
        print('5. Удалить заметку')
        print('6. Экспорт заметок в CSV')
        print('7. Импорт заметок из CSV')
        print('8. Назад')
        choice = input('Выберите действие: ')
        if choice == '1':
            title = input('Введите заголовок заметки: ')
            content = input('Введите содержимое заметки: ')
            manager.add_note(title, content)
        elif choice == '2':
            manager.list_notes()
        elif choice == '3':
            try:
                note_id = int(input('Введите ID заметки: '))
                manager.view_note(note_id)
            except ValueError:
                print('Некорректный ID.')
        elif choice == '4':
            try:
                note_id = int(input('Введите ID заметки: '))
                new_title = input('Введите новый заголовок заметки: ')
                new_content = input('Введите новое содержимое заметки: ')
                manager.edit_note(note_id, new_title, new_content)
            except ValueError:
                print('Некорректный ID.')
        elif choice == '5':
            try:
                note_id = int(input('Введите ID заметки: '))
                manager.delete_note(note_id)
            except ValueError:
                print('Некорректный ID.')
        elif choice == '6':
            manager.export_notes_to_csv()
        elif choice == '7':
            manager.import_notes_from_csv()
        elif choice == '8':
            break
        else:
            print('Некорректный выбор. Попробуйте снова.')


# ----- Модуль задач -----
TASKS_FILE = 'tasks.json'


class Task:
    def __init__(self, task_id, title, description, done=False, priority='Средний', due_date=None):
        self.id = task_id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        data = load_data(TASKS_FILE, [])
        self.tasks = [Task(**task) for task in data]

    def save_tasks(self):
        data = [task.__dict__ for task in self.tasks]
        save_data(TASKS_FILE, data)

    def add_task(self, title, description, priority, due_date):
        task_id = max([task.id for task in self.tasks], default=0) + 1
        new_task = Task(task_id, title, description, False, priority, due_date)
        self.tasks.append(new_task)
        self.save_tasks()
        print('Задача успешно добавлена!')

    def list_tasks(self, filter_by=None):
        if not self.tasks:
            print('Список задач пуст.')
            return
        filtered_tasks = self.tasks
        if filter_by == 'done':
            filtered_tasks = [task for task in self.tasks if task.done]
        elif filter_by == 'not_done':
            filtered_tasks = [task for task in self.tasks if not task.done]
        for task in filtered_tasks:
            status = 'Выполнена' if task.done else 'Не выполнена'
            print(f'{task.id}. {task.title} [{status}] (Приоритет: {task.priority}, Срок: {task.due_date})')

    def mark_task_done(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            task.done = True
            self.save_tasks()
            print('Задача отмечена как выполненная!')
        else:
            print('Задача не найдена.')

    def edit_task(self, task_id, title, description, priority, due_date):
        task = self.get_task_by_id(task_id)
        if task:
            task.title = title
            task.description = description
            task.priority = priority
            task.due_date = due_date
            self.save_tasks()
            print('Задача успешно обновлена!')
        else:
            print('Задача не найдена.')

    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print('Задача успешно удалена!')
        else:
            print('Задача не найдена.')

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def export_tasks_to_csv(self):
        if not self.tasks:
            print('Список задач пуст.')
            return
        file_name = 'tasks_export.csv'
        with open(file_name, mode='w', encoding='utf-8', newline='') as csv_file:
            fieldnames = ['ID', 'Название', 'Описание', 'Статус', 'Приоритет', 'Срок выполнения']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for task in self.tasks:
                writer.writerow({
                    'ID': task.id,
                    'Название': task.title,
                    'Описание': task.description,
                    'Статус': 'Выполнена' if task.done else 'Не выполнена',
                    'Приоритет': task.priority,
                    'Срок выполнения': task.due_date
                })
        print(f'Задачи успешно экспортированы в файл {file_name}')

    def import_tasks_from_csv(self):
        file_name = input('Введите имя CSV-файла для импорта: ')
        if not os.path.exists(file_name):
            print('Файл не найден.')
            return
        with open(file_name, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                task_id = max([task.id for task in self.tasks], default=0) + 1
                title = row.get('Название', '')
                description = row.get('Описание', '')
                status = row.get('Статус', 'Не выполнена')
                done = True if status == 'Выполнена' else False
                priority = row.get('Приоритет', 'Средний')
                due_date = row.get('Срок выполнения', None)
                new_task = Task(task_id, title, description, done, priority, due_date)
                self.tasks.append(new_task)
            self.save_tasks()
        print('Задачи успешно импортированы из CSV-файла.')


def tasks_menu():
    manager = TaskManager()
    while True:
        print('\nУправление задачами:')
        print('1. Добавить новую задачу')
        print('2. Просмотреть все задачи')
        print('3. Отметить задачу как выполненную')
        print('4. Редактировать задачу')
        print('5. Удалить задачу')
        print('6. Экспорт задач в CSV')
        print('7. Импорт задач из CSV')
        print('8. Назад')
        choice = input('Выберите действие: ')
        if choice == '1':
            title = input('Введите название задачи: ')
            description = input('Введите описание задачи: ')
            priority = input('Выберите приоритет (Высокий/Средний/Низкий): ')
            due_date = input('Введите срок выполнения (в формате ДД-ММ-ГГГГ): ')
            manager.add_task(title, description, priority, due_date)
        elif choice == '2':
            manager.list_tasks()
        elif choice == '3':
            try:
                task_id = int(input('Введите ID задачи: '))
                manager.mark_task_done(task_id)
            except ValueError:
                print('Некорректный ID.')
        elif choice == '4':
            try:
                task_id = int(input('Введите ID задачи: '))
                title = input('Введите новое название задачи: ')
                description = input('Введите новое описание задачи: ')
                priority = input('Выберите приоритет (Высокий/Средний/Низкий): ')
                due_date = input('Введите срок выполнения (в формате ДД-ММ-ГГГГ): ')
                manager.edit_task(task_id, title, description, priority, due_date)
            except ValueError:
                print('Некорректный ID.')
        elif choice == '5':
            try:
                task_id = int(input('Введите ID задачи: '))
                manager.delete_task(task_id)
            except ValueError:
                print('Некорректный ID.')
        elif choice == '6':
            manager.export_tasks_to_csv()
        elif choice == '7':
            manager.import_tasks_from_csv()
        elif choice == '8':
            break
        else:
            print('Некорректный выбор. Попробуйте снова.')


# ----- Модуль контактов -----
CONTACTS_FILE = 'contacts.json'


class Contact:
    def __init__(self, contact_id, name, phone, email):
        self.id = contact_id
        self.name = name
        self.phone = phone
        self.email = email


class ContactManager:
    def __init__(self):
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        data = load_data(CONTACTS_FILE, [])
        self.contacts = [Contact(**contact) for contact in data]

    def save_contacts(self):
        data = [contact.__dict__ for contact in self.contacts]
        save_data(CONTACTS_FILE, data)

    def add_contact(self, name, phone, email):
        contact_id = max([contact.id for contact in self.contacts], default=0) + 1
        new_contact = Contact(contact_id, name, phone, email)
        self.contacts.append(new_contact)
        self.save_contacts()
        print('Контакт успешно добавлен!')

    def search_contacts(self, query):
        results = [contact for contact in self.contacts if
                   query.lower() in contact.name.lower() or query in contact.phone]
        if results:
            for contact in results:
                print(f"{contact.id}. {contact.name} (Телефон: {contact.phone}, E-mail: {contact.email})")
        else:
            print('Контакты не найдены.')

    def edit_contact(self, contact_id, name, phone, email):
        contact = self.get_contact_by_id(contact_id)
        if contact:
            contact.name = name
            contact.phone = phone
            contact.email = email
            self.save_contacts()
            print('Контакт успешно обновлён!')
        else:
            print('Контакт не найден.')

    def delete_contact(self, contact_id):
        contact = self.get_contact_by_id(contact_id)
        if contact:
            self.contacts.remove(contact)
            self.save_contacts()
            print('Контакт успешно удалён!')
        else:
            print('Контакт не найден.')

    def get_contact_by_id(self, contact_id):
        for contact in self.contacts:
            if contact.id == contact_id:
                return contact
        return None

    def export_contacts_to_csv(self):
        if not self.contacts:
            print('Список контактов пуст.')
            return
        file_name = 'contacts_export.csv'
        with open(file_name, mode='w', encoding='utf-8', newline='') as csv_file:
            fieldnames = ['ID', 'Имя', 'Телефон', 'E-mail']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for contact in self.contacts:
                writer.writerow({
                    'ID': contact.id,
                    'Имя': contact.name,
                    'Телефон': contact.phone,
                    'E-mail': contact.email
                })
        print(f'Контакты успешно экспортированы в файл {file_name}')

    def import_contacts_from_csv(self):
        file_name = input('Введите имя CSV-файла для импорта: ')
        if not os.path.exists(file_name):
            print('Файл не найден.')
            return
        with open(file_name, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                contact_id = max([contact.id for contact in self.contacts], default=0) + 1
                name = row.get('Имя', '')
                phone = row.get('Телефон', '')
                email = row.get('E-mail', '')
                new_contact = Contact(contact_id, name, phone, email)
                self.contacts.append(new_contact)
            self.save_contacts()
        print('Контакты успешно импортированы из CSV-файла.')


def contacts_menu():
    manager = ContactManager()
    while True:
        print('\nУправление контактами:')
        print('1. Добавить новый контакт')
        print('2. Поиск контакта')
        print('3. Редактировать контакт')
        print('4. Удалить контакт')
        print('5. Экспорт контактов в CSV')
        print('6. Импорт контактов из CSV')
        print('7. Назад')
        choice = input('Выберите действие: ')
        if choice == '1':
            name = input('Введите имя контакта: ')
            phone = input('Введите номер телефона: ')
            email = input('Введите e-mail: ')
            manager.add_contact(name, phone, email)
        elif choice == '2':
            query = input('Введите имя или номер телефона для поиска: ')
            manager.search_contacts(query)
        elif choice == '3':
            try:
                contact_id = int(input('Введите ID контакта: '))
                name = input('Введите новое имя: ')
                phone = input('Введите новый номер телефона: ')
                email = input('Введите новый e-mail: ')
                manager.edit_contact(contact_id, name, phone, email)
            except ValueError:
                print('Некорректный ID.')
        elif choice == '4':
            try:
                contact_id = int(input('Введите ID контакта: '))
                manager.delete_contact(contact_id)
            except ValueError:
                print('Некорректный ID.')
        elif choice == '5':
            manager.export_contacts_to_csv()
        elif choice == '6':
            manager.import_contacts_from_csv()
        elif choice == '7':
            break
        else:
            print('Некорректный выбор. Попробуйте снова.')


# ----- Модуль финансов -----
FINANCE_FILE = 'finance.json'


class FinanceRecord:
    def __init__(self, record_id, amount, category, date, description):
        self.id = record_id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description


class FinanceManager:
    def __init__(self):
        self.records = []
        self.load_records()

    def load_records(self):
        data = load_data(FINANCE_FILE, [])
        self.records = [FinanceRecord(**record) for record in data]

    def save_records(self):
        data = [record.__dict__ for record in self.records]
        save_data(FINANCE_FILE, data)

    def add_record(self, amount, category, date, description):
        record_id = max([record.id for record in self.records], default=0) + 1
        new_record = FinanceRecord(record_id, amount, category, date, description)
        self.records.append(new_record)
        self.save_records()
        print('Запись успешно добавлена!')

    def list_records(self):
        if not self.records:
            print('Финансовых записей нет.')
            return
        for record in self.records:
            print(f'{record.id}. {record.date} | {record.amount} | {record.category} | {record.description}')

    def generate_report(self, start_date, end_date):
        try:
            start_date_obj = datetime.datetime.strptime(start_date, '%d-%m-%Y')
            end_date_obj = datetime.datetime.strptime(end_date, '%d-%m-%Y')
        except ValueError:
            print('Некорректный формат даты.')
            return

        filtered_records = [record for record in self.records if
                            start_date_obj <= datetime.datetime.strptime(record.date, '%d-%m-%Y') <= end_date_obj]
        income = sum(record.amount for record in filtered_records if record.amount > 0)
        expenses = sum(record.amount for record in filtered_records if record.amount < 0)
        balance = income + expenses
        print(f'Финансовый отчёт за период с {start_date} по {end_date}:')
        print(f'- Общий доход: {income}')
        print(f'- Общие расходы: {abs(expenses)}')
        print(f'- Баланс: {balance}')

        # Сохранение отчёта в CSV-файл
        report_file = f'report_{start_date}_{end_date}.csv'
        with open(report_file, mode='w', encoding='utf-8', newline='') as csv_file:
            fieldnames = ['ID', 'Дата', 'Сумма', 'Категория', 'Описание']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for record in filtered_records:
                writer.writerow({
                    'ID': record.id,
                    'Дата': record.date,
                    'Сумма': record.amount,
                    'Категория': record.category,
                    'Описание': record.description
                })
        print(f'Подробная информация сохранена в файле {report_file}')

    def delete_record(self, record_id):
        record = self.get_record_by_id(record_id)
        if record:
            self.records.remove(record)
            self.save_records()
            print('Запись успешно удалена!')
        else:
            print('Запись не найдена.')

    def get_record_by_id(self, record_id):
        for record in self.records:
            if record.id == record_id:
                return record
        return None

    def export_records_to_csv(self):
        if not self.records:
            print('Финансовых записей нет.')
            return
        file_name = 'finance_export.csv'
        with open(file_name, mode='w', encoding='utf-8', newline='') as csv_file:
            fieldnames = ['ID', 'Сумма', 'Категория', 'Дата', 'Описание']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for record in self.records:
                writer.writerow({
                    'ID': record.id,
                    'Сумма': record.amount,
                    'Категория': record.category,
                    'Дата': record.date,
                    'Описание': record.description
                })
        print(f'Финансовые записи успешно экспортированы в файл {file_name}')

    def import_records_from_csv(self):
        file_name = input('Введите имя CSV-файла для импорта: ')
        if not os.path.exists(file_name):
            print('Файл не найден.')
            return
        with open(file_name, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                record_id = max([record.id for record in self.records], default=0) + 1
                amount = float(row.get('Сумма', '0'))
                category = row.get('Категория', '')
                date = row.get('Дата', datetime.datetime.now().strftime('%d-%m-%Y'))
                description = row.get('Описание', '')
                new_record = FinanceRecord(record_id, amount, category, date, description)
                self.records.append(new_record)
            self.save_records()
        print('Финансовые записи успешно импортированы из CSV-файла.')


def finance_menu():
    manager = FinanceManager()
    while True:
        print('\nУправление финансовыми записями:')
        print('1. Добавить новую запись')
        print('2. Просмотреть все записи')
        print('3. Генерация отчёта')
        print('4. Удалить запись')
        print('5. Экспорт финансовых записей в CSV')
        print('6. Импорт финансовых записей из CSV')
        print('7. Назад')
        choice = input('Выберите действие: ')
        if choice == '1':
            try:
                amount = float(input('Введите сумму (доход — положительное число, расход — отрицательное): '))
                category = input('Введите категорию: ')
                date = input('Введите дату операции (в формате ДД-ММ-ГГГГ): ')
                description = input('Введите описание операции: ')
                manager.add_record(amount, category, date, description)
            except ValueError:
                print('Некорректный ввод суммы.')
        elif choice == '2':
            manager.list_records()
        elif choice == '3':
            start_date = input('Введите начальную дату (ДД-ММ-ГГГГ): ')
            end_date = input('Введите конечную дату (ДД-ММ-ГГГГ): ')
            manager.generate_report(start_date, end_date)
        elif choice == '4':
            try:
                record_id = int(input('Введите ID записи: '))
                manager.delete_record(record_id)
            except ValueError:
                print('Некорректный ID.')
        elif choice == '5':
            manager.export_records_to_csv()
        elif choice == '6':
            manager.import_records_from_csv()
        elif choice == '7':
            break
        else:
            print('Некорректный выбор. Попробуйте снова.')


# ----- Модуль калькулятора -----
def calculator_menu():
    print('\nКалькулятор')
    while True:
        expression = input('Введите выражение для вычисления или "назад" для возврата: ')
        if expression.lower() == "назад":
            break
        try:
            # Для безопасности можно использовать ast.literal_eval
            import ast
            result = eval(expression, {'__builtins__': None}, {})
            print(f'Результат: {result}')
        except Exception as e:
            print(f'Ошибка: {e}')


# ----- Основное меню -----
def main_menu():
    while True:
        print('\nДобро пожаловать в Персональный помощник!')
        print('Выберите действие:')
        print('1. Управление заметками')
        print('2. Управление задачами')
        print('3. Управление контактами')
        print('4. Управление финансовыми записями')
        print('5. Калькулятор')
        print('6. Выход')
        choice = input('Введите номер действия: ')
        if choice == '1':
            notes_menu()
        elif choice == '2':
            tasks_menu()
        elif choice == '3':
            contacts_menu()
        elif choice == '4':
            finance_menu()
        elif choice == '5':
            calculator_menu()
        elif choice == '6':
            print('До свидания!')
            break
        else:
            print('Некорректный выбор. Попробуйте снова.')


if __name__ == '__main__':
    main_menu()
