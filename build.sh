rm -rf build dist *.egg-info service/build service/dist
find ./ -name '*.DS_Store' -delete
source build-services-django.sh
pyinstaller service-webssh/WebSSH.spec --distpath=./services
python setup.py py2app -A