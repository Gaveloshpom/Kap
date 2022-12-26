from collections import UserDict
from datetime import datetime
import pickle
import re

# клас батько, для роботи з данними 
class Field:
    def __init__(self, value: str):
        self._value = None
        self.value = value
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
        
# клас нащадок, зберігає ім'я контакту, то провіряє на валідність   
class Name(Field):
    
    @Field.value.setter
    def value(self, name: str):
        if name.isnumeric():
            raise ValueError('Wrong name')
        self._value = name
        
# клас нащадок, зберігає номер контакту, провіряє на валідність і форматує          
class Phone(Field):
    
    @Field.value.setter
    def value(self, phone: str):
        if not phone.isnumeric():
            raise ValueError('Wrong phones')
        format_phone = self.format_phone_number(phone)
        if format_phone:
            self._value = format_phone
        
    @staticmethod
    def format_phone_number(phone: str):
        if len(phone) == 10:
            return f'+38{phone}'
        elif len(phone) == 12:
            return f'+{phone}'
        else:
            raise ValueError('Wrong phones')
        
# клас нащадок, зберігає email контакту, провіряє на валідність і форматує          
class Email(Field):
    
    @Field.value.setter
    def value(self, email: str):
        result = re.search(r"[a-zA-z][\w_.]+@[a-zA-z]+\.[a-zA-z]{2,}", email)
        if not result:
            raise ValueError('Wrong email')
        self._value = result.group()
        
    
# клас нащадок,  зберігає дату народження контакту, та перевіряє на валідність
class Birthday(Field):
    
    @Field.value.setter
    def value(self, birthday: str):
        current_date = datetime.now().date()
        birthday_date = datetime.strptime(birthday, '%Y-%m-%d').date()
        if birthday_date > current_date:
            raise ValueError("Your contact havent born yet")
        self._value = birthday
        
# клас для роботи з обєктами класів нащадків Field       
class Record:
    
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        
# вивід усієї доступної інформації про контакт        
    def get_info(self):
        birthday_info = ''
        phones_info = [phone.value for phone in self.phones]
        email_info = ''
        
        if self.birthday:
            birthday_info = f' Birthday: {self.birthday.value}'
            
        if self.email:
            email_info = f' Email: {self.email.value}'
            
        return f'{self.name.value} : {", ".join(phones_info)}{birthday_info}{email_info}'
    
# розрахунок кількості днів до дня народження контакту            
    def day_to_bithday(self):
        if not self.birthday:
            raise ValueError('This contact havent birthday date')
        
        current_date = datetime.now().date()
        
        birthday_date = datetime.strptime(self.birthday.value, '%Y-%m-%d').date()
        this_year_birthday = birthday_date.replace(year=current_date.year)
        
        if this_year_birthday < current_date:
           this_year_birthday = this_year_birthday.replace(year=current_date.year + 1)
            
        return (this_year_birthday - current_date).days
    
# додати телефон у список номерів        
    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))
        
# додати дату народження       
    def add_birthday(self, date: str):
        self.birthday = Birthday(date)
        
# додати email
    def add_contact_email(self, email: str):
        self.email = Email(email)
            
# видалити телефон  
    def delete_phone(self, phone: str):
        for record_phone in self.phones:
            if record_phone.value == phone:
                self.phones.remove(record_phone)
                return True
        return False
    
# замінити телефон
    def change_phone(self, phones):
        for phone in phones:
            if not self.delete_phone(phone):
                self.add_phone(phone)
    
        
    

class AdressBook(UserDict):
# загрузка стану із файла    
    def __init__(self):
        super().__init__()
        self.load_from_file()
        
# додати контак до книги із ключем ім'я контакту    
    def add_record(self, record: Record):
        self.data[record.name.value] = record

# повертає список ісіх обєктів класу Record
    def get_all_record(self):
        return self.data
    
# перевірка на існування обєкта по ключу
    def has_record(self, name):
        return bool(self.data.get(name))

# повертає обєкт класу Record по ключу
    def get_record(self, name) -> Record:
        return self.data.get(name)

# видаляє обєкт класу Record
    def remove_record(self, name):
        del self.data[name]
        
# шукає контакт по введеним даним користувача в іменах та номерах телефону
    def search(self, value):
        if self.has_record(value):
            return self.get_record(value)

        for record in self.get_all_record().values():
            for phone in record.phones:
                if phone.value == value:
                    return record

        raise ValueError("Contact with this value does not exist.")
    
# виводить контакти по 3 на сторінку   
    def iterator(self, count=3):
        result = []
        
        for contact in self.data.values():
            result.append(contact)
            if len(result) == count:
                yield result
                result = []
        
        if result:
            yield result

# зберігання контактів у файл          
    def save_to_file(self):
        with open('AdressBook.bin', 'wb') as fw:
            pickle.dump(self.data, fw)
            
# загрузка контактів із файлу
    def load_from_file(self):
        try:
            with open('AdressBook.bin', 'rb') as fr:
                self.data = pickle.load(fr)
        except FileNotFoundError:
            pass