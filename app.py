from flask import Flask, render_template

from bs4 import BeautifulSoup
import requests
import json

app = Flask(__name__)


def create_plot():
    html_doc = requests.get('https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Indonesia')

    soup = BeautifulSoup(html_doc.text, 'html.parser')

    case_by_province = soup.find(attrs={'class': 'wikitable float sortable'}).find('tbody').findAll('tr')

    _confirmed = []
    _recovered = []
    _death = []
    _active = []
    _provinces = []

    for cbp in case_by_province:
        if cbp.find('th') is not None:
            if cbp.find('th').find('a') is not None and len(cbp.find('th').findAll('a')) > 1:
                province = cbp.find('th').findAll('a')[1].text.strip()
                confirmed = cbp.findAll('td')[2].text.strip()
                recovered = cbp.findAll('td')[3].text.strip()
                death = cbp.findAll('td')[4].text.strip()
                active = cbp.findAll('td')[5].text.strip()
                _confirmed.append(confirmed)
                _recovered.append(recovered)
                _death.append(death)
                _active.append(active)
                _provinces.append(province)

    records = [
        {
            'name': 'Confirmed',
            'values': _confirmed,
            'provinces': _provinces
        },
        {
            'name': 'Recovered',
            'values': _recovered,
            'provinces': _provinces
        },
        {
            'name': 'Death',
            'values': _death,
            'provinces': _provinces
        },
        {
            'name': 'Active',
            'values': _active,
            'provinces': _provinces
        }
    ]

    return records


@app.route('/')
def index():
    bar = create_plot()
    return render_template('index.html', data=json.dumps(bar))


if __name__ == '__main__':
    app.run()
