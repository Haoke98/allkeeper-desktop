rm -rf build dist *.egg-info service/build service/dist
find ./ -name '*.DS_Store' -delete
python setup.py py2app -A