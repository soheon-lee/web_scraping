import requests
import sys
from bs4 import BeautifulSoup

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import *
e = sys.exit

engine = create_engine('sqlite:///wecode_mentor.db')
Base = declarative_base()

class Mentor(Base):
    __tablename__ = 'mentors'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    title = Column(String(50))
    description = Column(String(50)) 

Mentor.__table__.create(bind=engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

req = requests.get('https://wecode.co.kr/') # http request 보내는 거임
html = req.text
soup = BeautifulSoup(html, 'html.parser')

name = soup.select(
    '#root > div > div.main > div.content.mentor-container > div > div:nth-child(2) > div.mentor-title-wrap > div > p.name'
)
print(name)
e()

singer = soup.select(
    'li > button > span.chart-element__information > span.chart-element__information__artist.text--truncate.color--secondary'
)
music_chart_2 = []

for item in zip(rank, song, singer):
    music_chart_2.append(
    {
        'rank'  : item[0].text,
        'song'  : item[1].text,
        'singer': item[2].text,
    })

    for i in music_chart_2:
        print (i)
        
for element in music_chart_2:
     result = Music(rank = element['rank'],
                    song = element['song'],
                    singer = element['singer'],
     )
     session.add(result)
     session.commit()

request = session.query(Music).all()

for row in request:
    print(row.rank,'|', row.song,'|' ,row.singer)
