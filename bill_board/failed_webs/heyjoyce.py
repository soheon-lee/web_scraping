import requests
import sys
from bs4 import BeautifulSoup

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import *
e = sys.exit

engine = create_engine('sqlite:///heyjoyce.db')
Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    schedule    = Column(String(50))
    name        = Column(String(50))
    description = Column(String(50))

Event.__table__.create(bind=engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

req = requests.get(
    'https://heyjoyce.com/program/event'
)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

schedule = soup.select(
    '#scrollElement > a > div > div:nth-child(2) > div > div.jss6.jss25 > div > div'
)

name = soup.select(
    'aa#scrollElement > a > div > div:nth-child(2) > div > div.title'
)
print(name)
e()
description = soup.select(
)


FAQ_list = []

for item in faq:
    FAQ_list.append(
    {
        'question' : item.text
    })

for element in FAQ_list:
    print('question : ',element['question'])
    result = FAQ(
        question = element['question'],
    )
    session.add(result)
    session.commit()

#request = session.query(FAQ).all()
e()
for row in request:
    print(row.rank,'|', row.song,'|' ,row.singer)
