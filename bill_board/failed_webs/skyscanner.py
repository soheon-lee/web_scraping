import requests
import sys
from bs4 import BeautifulSoup

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import *
e = sys.exit

engine = create_engine('sqlite:///skyscanner.db')
Base = declarative_base()

class Flight(Base):
    __tablename__ = 'flights'
    id = Column(Integer, primary_key=True)
    price       = Column(String(50))
    destination = Column(String(50))

Flight.__table__.create(bind=engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

req = requests.get('https://www.skyscanner.co.kr/transport/flights-from/sela?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=0&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&oym=2002') # http request 보내는 거
html = req.text
soup = BeautifulSoup(html, 'html.parser')
 
destination = soup.select(
    '#destinations > ul > li:nth-child(1) > a > div.browse-data-route > p'
)

print(destination)
e()

song = soup.select(
    '#charts > div > div.chart-list.container > ol > li > button > span.chart-element__information > span.chart-element__information__song.text--truncate.color--primary'
)
singer = soup.select(
    '#charts > div > div.chart-list.container > ol > li > button > span.chart-element__information > span.chart-element__information__artist.text--truncate.color--secondary'
)

music_chart = []

for item in zip(rank, song, singer):
    music_chart.append(
    {
        'rank'  : item[0].text,
        'song'  : item[1].text,
        'singer': item[2].text,
    })

    for i in music_chart:
        print (i)

for element in music_chart:
     result = Music(rank = element['rank'],
                    song = element['song'],
                    singer = element['singer'],
     )
     session.add(result)
     session.commit()

request = session.query(Music).all()

for row in request:
    print(row.rank,'|', row.song,'|' ,row.singer)
