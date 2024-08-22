rm -rf build dist *.egg-info service/build service/dist
find ./ -name '*.DS_Store' -delete
pyinstaller service-webssh/WebSSH.spec --distpath=./dist/services
pyinstaller service/allkeeper-django.spec --distpath=./dist/services
python setup.py py2app -A