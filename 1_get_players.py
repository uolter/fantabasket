# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import csv

PLAYERS_URL = 'http://195.56.77.208/player/'

CSV_FILE_NAME = 'players.csv'


def main():

    r = requests.get(PLAYERS_URL)

    if r.status_code == 200:

        soup = BeautifulSoup(r.text)

        links = soup.find_all('a', class_ ='sch_ris', href=True)

        with open(CSV_FILE_NAME, 'w') as csvfile:
            
            writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            for l in links:
                try: 
                    text = l.text if l.text else 'undefined'
                    writer.writerow([text.encode('utf-8'), l['href']])

                except UnicodeEncodeError, e:
                    print e.message
                    print l.txt, l['href']



if __name__ == "__main__":

    print 'Start creating CSV.'
    main()

    print 'End !!'
    


