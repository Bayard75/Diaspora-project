import requests
from urllib.parse import quote

from flask import Flask, render_template, request, jsonify, make_response
from datetime import datetime

import pandas as pd
import os

app = Flask(__name__)
TOKEN = os.environ.get('FB_TOKEN')
print(TOKEN)

def get_behaviors():
    behaviors = [{
                    "id": "6023422105983",
                    "name": "A vécu en Côte d’Ivoire (anciennement Expats - Côte d’Ivoire)",
                    "short_name": "Cote d'Ivoire"
                },
                {
                    "id":"6023357000583",
                    "name": "A vécu au Sénégal (anciennement Expats - Sénégal)",
                    "short_name": "Senegal"
                }]
    return behaviors


def get_countries():
    countries = [{
        "code": "FR",
        "name": "France"
    },{
        "code": "GB",
        "name": "Royaume-Uni"
    },{
        "code": "IT",
        "name": "Italie"
    },{
        "code": "ES",
        "name": "Espagne"
    },{
        "code": "CA",
        "name": "Canada"
    },{
        "code": "US",
        "name": "Etats-Unis"
    },{
        "code": "SN",
        "name": "Senegal"
    },{
        "code": "CI",
        "name": "Cote d'Ivoire"
    },{
        "code": "BE",
        "name": "Belgique"
    },{
        "code": "CH",
        "name": "Suisse"
    },{
        "code": "DE",
        "name": "Allemagne"
    },{
        "code": "PT",
        "name": "Portugal"
    },{
        "code": "BF",
        "name": "Burkina Faso"
    },{
        "code": "GN",
        "name": "Guinee"
    },{
        "code": "MA",
        "name": "Maroc"
    },{
        "code": "GA",
        "name": "Gabon"
    }]
    return countries


def get_estimate(gender, residence_code, origine_id, origine_name, age_max=65, age_min=13):
    targeting_spec = '{"genders":[%s],"age_max":%s,"age_min":%s,"geo_locations":{"countries":["%s"],"location_types":["home","recent"]},"flexible_spec":[{"behaviors":[{"id":"%s","name":"%s"}]}]}' % (gender, age_max, age_min, residence_code, origine_id, origine_name)
    params = quote(targeting_spec, safe='')
    url = f'https://graph.facebook.com/v7.0/act_1047742262329813/reachestimate?access_token=EAABsbCS1iHgBAAspvjIZCwE1mqv6tE3xitQ8dZARWvsWvK10EPZBZBcItZBheyfM6eaBVVA33ujzcd7ghQ57ZAbmmIWx76joAFLvtKccziDnMMgFKFw1LWX8krb18r7YJcdYcfEOUZBerJbeFmZCC407bmZAmBwhBlj0ZD&__cppo=1&__activeScenarioIDs=%5B%5D&__activeScenarios=%5B%5D&_app=ADS_MANAGER&_index=104&_reqName=adaccount%2Freachestimate&_reqSrc=AdsTargetingEstimatedReach.react&_sessionID=6702a31bb3abbac2&include_headers=false&locale=fr_FR&method=get&pretty=0&suppress_http_code=1&targeting_spec={params}&xref=f15b2e07c0f6394'
    res = requests.get(url)
    return res.json()['data']['users']

@app.route("/")
@app.route("/home",  methods=['POST'])
def home():
    if request.method == 'POST':
        residence_wanted = request.get_json()["residence"]
        origine_wanted = request.get_json()["origine"]
        age_ranges = request.get_json()['age_ranges']
        path = generate_csv(residence_wanted, origine_wanted,
                            age_ranges)
        return make_response(jsonify({'status': 'ok', "path": path}))

    behaviors = get_behaviors()
    countries = get_countries()
    return render_template('index.html', behaviors=behaviors, countries=countries)


def generate_csv(residence_wanted, origine_wanted, age_ranges):
    df = pd.DataFrame(columns=['Pays de residence', "Pays d'origine", "Age Minimum", "Age Maximum", "Nombre d'utilisateur Total", "Hommes", "Femmes"])
    for residence in residence_wanted:
        for origine in origine_wanted:
            for ages in age_ranges:
                age_min = ages[0]
                age_max = ages[1]
                for gender in range(0, 3):
                    if gender == 0:
                        users_total = get_estimate(gender, residence['id'], origine['id'], origine["name"], age_max, age_min)
                    elif gender == 1:
                        male_users = get_estimate(gender, residence['id'], origine['id'], origine["name"], age_max, age_min)
                    elif gender == 2:
                        femele_users = get_estimate(gender, residence['id'], origine['id'], origine["name"], age_max, age_min)
                        new_row = {"Pays de residence": residence["name"],
                                    "Pays d'origine": origine["short_name"],
                                    "Age Minimum": age_min, "Age Maximum": age_max,
                                    "Nombre d'utilisateur Total" : users_total, 
                                    "Hommes": male_users,  "Femmes": femele_users}
                        df = df.append(new_row, ignore_index=True)
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")

    df.to_csv(f'static/assets/Diaspora_{dt_string}.csv')
    return f'static/assets/Diaspora_{dt_string}.csv'

if __name__ == '__main__':
    app.run(debug=True)
