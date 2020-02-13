import requests
import sys
from bs4 import BeautifulSoup

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import *
e = sys.exit

engine = create_engine('sqlite:///data_go_kr.db')
Base = declarative_base()

class KoreaFile(Base):
    __tablename__ = 'koreafiles'
    id = Column(Integer, primary_key=True)
    title           = Column(String(50))
    date            = Column(String(50)) 
    category        = Column(String(50)) 

KoreaFile.__table__.create(bind=engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

req = requests.get('https://www.data.go.kr/useCase/exam/index.do') # http request 보내는 거임
html = req.text
soup = BeautifulSoup(html, 'html.parser')

title = soup.select(
    '#sub-main > div.container.old-view > div.content_wrap > form > div.ex_type > ul > li > div.con > p > a'
)
date = soup.select(
    '#sub-main > div.container.old-view > div.content_wrap > form > div.ex_type > ul > li > div.con > em'
)
category = soup.select(
    '#sub-main > div.container.old-view > div.content_wrap > form > div.ex_type > ul > li > div.con > dl > dt > div'
)
korea_file_list = []

for item in zip(title, date, category):
    korea_file_list.append(
    {
        'title'  : item[0].text,
        'date'  : item[1].text,
        'category': item[2].text,
    })

for element in korea_file_list:
    result = KoreaFile(
        title = element['title'].strip(),
        date = element['date'].strip(),
        category = element['category'].strip()[5:],
    )

    session.add(result)
    session.commit()

request = session.query(KoreaFile).all()

for row in request:
    print(row.date,'|', row.title,'|' ,row.category)
