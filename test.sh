pip3 install pytest
cat ./tmp/junit-result.xml
python3 -m pytest --all -v --junitxml="./tmp/junit-result.xml"