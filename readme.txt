1. Install python3 and python3-pip
2. git clone https://github.com/humblesami/cable.git

If you have already setup all (virtual environment, installed requirements, copied config.json) then just do
python manage.py reset other follow these

3. make virtual environment
On macOS and Linux:
python3 -m venv /path/to/any_name_of_env
On Windows: py -m venv /path/to/any_name_of_env

Activate venv
source /path/to/any_name_of_env/bin/activate
4. cd cable (go inside ur project root folder)
5. copy example.config.json to config.json (same directory)
6. update username,password
7. make database with name d5ja7hl6th93a2
8. pip install -r requirements.txt
9. python manage.py makemigrations
10. python manage.py migrate
11. python manage.py createsuperuser
12. python manage.py runserver
13. http://localhost:8000/admin

