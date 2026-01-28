rm -rf build dist *.egg-info service/build service/dist
find ./ -name '*.DS_Store' -delete
source build-services-django.sh
python setup.py py2app -A