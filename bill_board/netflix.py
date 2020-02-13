import requests
import sys
from bs4 import BeautifulSoup

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import *
e = sys.exit

engine = create_engine('sqlite:///netflix.db')
Base = declarative_base()

class FAQ(Base):
    __tablename__ = 'FAQs'
    id = Column(Integer, primary_key=True)
    question = Column(String(50))

FAQ.__table__.create(bind=engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

req = requests.get(
    'https://www.netflix.com/kr/'
)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

faq = soup.select(
    '#faq > div.our-story-card-text > ul > li > button'
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

request = session.query(FAQ).all()
for row in request:
    print(row.name,'|', row.song,'|' ,row.singer)
