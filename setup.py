import os

# install requirements
os.system('pip install -r requirements.txt')
# unzip the data
os.system('unzip data/english.zip -d data/')
os.system('unzip data/german.zip -d data/')
# create a temp file for writing trees to
if not os.path.exists('temp/'):
    os.mkdir('temp/')
