import sys
import requests
import pandas as pd

from bs4                        import BeautifulSoup
from sqlalchemy                 import *
from sqlalchemy.sql             import *
from sqlalchemy.orm             import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

e = sys.exit

engine  = create_engine('sqlite:///seven_day_weather.db')
Base    = declarative_base()

class Weather(Base):
    __tablename__ = 'weathers'
    id          = Column(Integer, primary_key=True)
    period      = Column(String(50))
    temp        = Column(String(50))
    desc        = Column(String(50))
    short_desc  = Column(String(200))

Weather.__table__.create(bind=engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

page            = requests.get('https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168#.XkTU63UzY5k')
soup            = BeautifulSoup(page.content, 'html.parser')
seven_day       = soup.find(id="seven-day-forecast")
forecast_items  = seven_day.find_all(class_="tombstone-container")

periods     = [pt.get_text() for pt in seven_day.select(".tombstone-container .period-name")]
short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps       = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs       = [d['title'] for d in seven_day.select(".tombstone-container img")]

weather = pd.DataFrame({
    "period": periods,
    "short-desc": short_descs,
    "temp": temps,
    "desc": descs
})

weather_chart = []

for item in zip(periods, short_descs, temps, descs):
    print(item)
    weather_chart.append(
    {
        'period'    : item[0],
        'short-desc': item[1],
        'temp'      : item[2],
        'desc'      : item[3],
    })

    for element in weather_chart:
        result = Weather(
            period      = element['period'],
            temp        = element['temp'],
            short_desc  = element['short-desc'],
            desc        = element['desc'],
        )
        session.add(result)
        session.commit()

request = session.query(Weather).all()

for row in request:
    print(row.period, '|', row.temp, '|', row.short_desc, '|', row.desc)

