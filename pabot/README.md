# GoIT-8


# Установка 

Вионайте послідовно в терміналі:


1. cd pabot
2. python setup.py install


# Використання

Програма запускається командою: pabot

Після запуску вам будуть доступні команди:

> hello
 
> help - show commands list

> add - add new contact in storage 
>>Example: add "name (only letters without spaces)" "phone number (only digits without spaces)"

> change - change existing contact 
>>Example: chnage "exist contact name (only letters without spaces)" "new phone number (only digits without spaces)"

> phone - show exist contact name and phone

> show all - show all existing contacts

> delete phone - remove entered phone from contact 
>>Example: delete phone "name (only letters without spaces)" "phone number (only digits without spaces)"

> delete - remove contact
>>Example: delete "name (only letters without spaces)" 

> good bye/close/exit - bye bye

> birthday - add birthday date to the contact 
>>Example: bithday name date(yyyy-mm-dd)

> days to birthday - show how much days left to the contact birthday 
>>Example: days to birthday name

> sort directory - just what it says 
>>Example: sort directory D:\\stuff\\python_projects

> create note - creates a new note 
>>Example: create note "name (only letters without spaces)"

> remove note - deletes a note by name 
>>Example: remove note "name"

> describe note - adds description to a note 
>>Example: describe note "name" "description"

> delete description - deletes the description of a note 

> alter description - changes the description of a note, if it exists

> tag - add a tag to the note 
>>Example: tag "name" "tag"

> untag - deletes a tag from a note, if it exists 
>>Example: untag "name" "tag"

> search notes - searches all notes for a match, prints out all matching notes

> notes - shows all recorded notes

> sort directory - just what it says 
>>Example: sort directory D:\\stuff\\python_projects\n

