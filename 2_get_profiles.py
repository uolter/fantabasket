#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from threading import Thread
import csv
import re
from datetime import datetime


CSV_IN_FILE_NAME = 'data/players.csv'
CSV_OUT_FILE_NAME = 'data/profiles_7.csv'

profiles = []

class ProfileReader(Thread):

    def __init__(self, player, url):

        self.url = url
        self.player = player
        super(ProfileReader, self).__init__()

    def _get_team(self, soup):

        team = soup.find_all('a', class_ ='w tdn')
        return team[0].text


    def _get_role(self, soup):

        try:
            role = soup.find_all('div', class_ ='role fl mt8')
            return role[0].text
        except IndexError, e:
            print e, role

    def _get_age(self, soup):

        birthday = soup.find(text=re.compile("Data di Nascita"))
        birthday = birthday.find_next('td')
        birthday = birthday.text[-10:11]
        try:
            delta = datetime.now() - datetime.strptime(birthday, "%d/%m/%Y") 

            return delta.days / 360
        except AttributeError, e:
            print e.message
            return 0
        except UnicodeEncodeError, e:
            print e.message
            return 0

    def _get_country(self, soup):

        country = soup.find(text=re.compile("Naz. di Nascita"))
        country = country.find_next('td')
        
        return country.text

    def _get_record(self, soup):

        tag = soup.find('tr', class_ ='latest_row_nohover4')
        
        if tag:
            while tag.find_next() and tag.find_next().name == 'td':
                tag = tag.find_next()
                yield tag.text.encode('utf-8')
        else:
            for x in range(30):
                yield ""


    def run(self):

        r = requests.get(self.url)
        soup = BeautifulSoup(r.text.encode('utf-8'))
        
        unicode(soup)

        p = [self.player]
        p.append(self._get_team(soup).encode('utf-8'))
        p.append(self._get_role(soup))
        p.append(self._get_age(soup))
        p.append(self._get_country(soup).encode('utf-8'))
        
        for rec in self._get_record(soup):
            # print rec
            p.append(rec)
        
        p.append(self.url)

        profiles.append(p)


def save_csv(players, file_name):

    print 'Start writing CSV', datetime.now()

    head =["Name", "Team", "Role", "Age", "Country", "Media", "PR", "PG", "SF", "PT", "MIN", "C", "S", "R", "T", "%", "SC", "R", 
            "T", "%", "R", "T", "%", "Off", "Dif", "Tot", "Dat", "Sub", "Per", 
            "Rec", "Ass", "Lega", "OER", "Adp", "+/-", "Url"]



    with open(file_name, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        writer.writerow(head)
        for r in players:
            try:
                writer.writerow(r)
            except UnicodeEncodeError:
                print "Error in saving ", r

    print 'End writing CSV', datetime.now()
    
def main():

    print 'start reading profiles ', datetime.now()

    threads = []
    with open(CSV_IN_FILE_NAME, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        i =0
        for row in reader:
            t = ProfileReader(row[0], row[1])
            threads.append(t)
            t.start()
            i += 1 
            #  i > 5: break
    

    for t in threads:
        t.join()

    print 'end reading profiles ', datetime.now()

    save_csv(profiles, CSV_OUT_FILE_NAME)

if __name__ == '__main__':

    main()
