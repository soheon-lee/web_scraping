import requests
from bs4 import BeautifulSoup
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import *
engine = create_engine('sqlite:///music.db')
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
req = requests.get('https://www.billboard.com/charts/hot-100')
html = req.text
soup = BeautifulSoup(html, 'html.parser')
rank = soup.select(
   'li > button > span.chart-element__rank.flex--column.flex--xy-center.flex--no-shrink > span.chart-element__rank__number'
)
song = soup.select(
   'li > button > span.chart-element__information > span.chart-element__information__song.text--truncate.color--primary'
)
singer = soup.select(
   'li > button > span.chart-element__information > span.chart-element__information__artist.text--truncate.color--secondary'
)
music_chart = []
for item in zip(rank, song, singer):
    music_chart.append(
        {
            'rank'  : item[0].text,
            'song'  : item[1].text,
            'singer': item[2].text,
        }
    )
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
