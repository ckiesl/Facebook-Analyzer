# -*- coding: utf-8 -*-
import os
import logging
from bs4 import BeautifulSoup
import re

'def'
import codecs
import functools


def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    print(input_filepath)
    print(output_filepath)
    messages = codecs.open(input_filepath+'\\messages.htm', 'r', 'UTF-8')
    print(type(messages))
        #messages = open(input_filepath+'\\messages.htm','r')
    soup = BeautifulSoup(messages, 'html.parser')
    divs = soup.find_all('div')
    nav = divs[0]
    content = divs[1]
    threads = content.find_all('div', class_ = 'thread')
    members = map(lambda x: re.findall('[0-9]*@facebook.com', str(x)),threads)
    messageAll = map(lambda x: zip(x.find_all('span', class_='user'), x.find_all('span',class_='meta'), x.find_all('p')), threads)
    #MessageAll now contains a list of threads, where each thread again contains a list of message in the form (user,meta,message)
    #members[i] contains the members of thread i
    #The next step is saving this information in a database

if __name__ == '__main__':
    os.chdir(os.getcwd())
    os.chdir('..')
    os.chdir('..')
    os.chdir('data')
    os.chdir('raw')
    os.chdir('html')
    html_dir = os.getcwd()
    os.chdir('..')
    os.chdir('..')
    os.chdir('processed')
    processed_dir = os.getcwd()

    main(html_dir,processed_dir)
