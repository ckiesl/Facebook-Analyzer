# -*- coding: utf-8 -*-
import os
import logging
from bs4 import BeautifulSoup
import re

'def'
import codecs
import functools
from pymongo import MongoClient
import datetime
import time

def  getMessage(threadId,sender, text, date):
    return {"threadId":threadId, "sender":sender, "text":text, "date":date}

def getThread(id,participants):
    return {"id":id, "participants":participants}




def main(input_filepath, output_filepath):
    client = MongoClient()
    db = client['facebook']
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    messages = codecs.open(input_filepath+'\\messages.htm', 'r', 'UTF-8')
        #messages = open(input_filepath+'\\messages.htm','r')
    soup = BeautifulSoup(messages, 'html.parser')
    divs = soup.find_all('div')
    nav = divs[0]
    content = divs[1]
    threads = content.find_all('div', class_ = 'thread')
    members = map(lambda x: re.findall('[0-9]*@facebook.com', str(x)),threads)
    members = map(lambda x: list(set(x)), members)
    messageAll = map(lambda x: zip(x.find_all('span', class_='user'), x.find_all('span',class_='meta'), x.find_all('p')), threads)
    #MessageAll now contains a list of threads, where each thread again contains a list of message in the form (user,meta,message)
    #members[i] contains the members of thread i
    #The next step is saving this information in a database
    
    #Mongodb
    messageCollection = db.messages
    i=0
    for (thread,participants) in zip(messageAll,members):
        print(participants)
        m = []
        for x in thread:
            text = str(x[2])[3:-4]
            user = str(x[0])[19:-7]
            meta = str(x[1])[19:-14].split(",")[1]
            meta = meta.replace("Januar","1.").replace("Februar","2.").replace("März","3.").replace("April","4.").replace("Mai","5.").replace("Juni","6.").replace("Juli","7.").replace("August","8.").replace("September","9.").replace("Oktober","10.").replace("November","11.").replace("Dezember","12.")
            meta = meta.replace(" ","").replace("um"," ")
            new_date = time.strptime(meta,'%d.%m.%Y %H:%M')
            m.append({"user":user,"meta":meta,"text":text})
        thread = {"_id":i, "members": participants, "messages":m}
        i = i+1
        if(i==2):
            return "1"
        messageCollection.insert_one(thread)
    
    

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
