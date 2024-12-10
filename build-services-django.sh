cd service
python ./manage.py collectstatic
pyinstaller ./allkeeper-django.spec --distpath=./services