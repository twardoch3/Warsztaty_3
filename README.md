# Warsztaty_3.1 - Django Basics Module - Conference Rooms Application
This Application allows to manage conference rooms and their reservations (add, edit or delete rooms, reservations).

### Requirements
Program requires PostgreSQL database and Django.

### Installing
Create database 'warsztaty_django1' with tables for rooms and reservations. Install requirements  with command :
```
pip install -r requirements.txt
```
### Running the program
Apply the migrations:
```
python manage.py migrate
```
Start a development Web server on the local machine with command:
```
python manage.py runserver
```

### Usage Examples:
Create a room:
```
http://127.0.0.1:8000/room/new/
```
Check room reservations:
```
http://127.0.0.1:8000/reservations/<int:room_id>/
```
