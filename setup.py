import os

# install requirements
os.system('pip install -r requirements.txt')
# unzip the data
os.system('unzip data/english.zip -d data/')
os.system('unzip data/german.zip -d data/')
