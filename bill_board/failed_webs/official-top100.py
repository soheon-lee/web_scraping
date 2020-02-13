import requests
import sys
from bs4 import BeautifulSoup

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import *
e = sys.exit

engine = create_engine('sqlite:///music_official_100.db')
Base = declarative_base()

class Music(Base):
    __tablename__ = 'musics'
    id = Column(Integer, primary_key=True)
    rank = Column(String(50))
    song = Column(String(50))
    singer = Column(String(50))

Music.__table__.create(bind=engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

req = requests.get('https://www.officialcharts.com/charts/') # http request 보내는 거
html = req.text
soup = BeautifulSoup(html, 'html.parser')

print(soup)
rank = soup.select(
    '#main > article > div > div.grid__cell.unit-2-3--desktop > section > table > tbody > tr:nth-child(2) > td:nth-child(1) > span'
#    '#charts > div > div.chart-list.container > ol > li > button > span.chart-element__rank.flex--column.flex--xy-center.flex--no-shrink > span.chart-element__rank__number'
)

print(rank)
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
