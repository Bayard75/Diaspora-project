import requests
import json
from urllib.parse import quote

token = "EAABsbCS1iHgBAHTmw316FuXn1YmFCwT5qZCy7ZAG3AuADr7yCW861uTQzYt5VPdj76EOrBi5GwXcH5ta9nfkhwUZB659YL7Eg8jtavWZAmT9FJFkIYsPKAjRKME4q3W6lKQ3cYAwCy4tiCv69OzrBRaQnHOu5ngDzygkiZBcGrgZDZD"

behavior_requets = requests.get('https://graph.facebook.com/v7.0/act_1047742262329813/targetingsuggestions?access_token=EAABsbCS1iHgBAHTmw316FuXn1YmFCwT5qZCy7ZAG3AuADr7yCW861uTQzYt5VPdj76EOrBi5GwXcH5ta9nfkhwUZB659YL7Eg8jtavWZAmT9FJFkIYsPKAjRKME4q3W6lKQ3cYAwCy4tiCv69OzrBRaQnHOu5ngDzygkiZBcGrgZDZD&_app=ADS_MANAGER&_index=36&_reqName=adaccount%2Ftargetingsuggestions&_reqSrc=AdsUnifiedSuggestionsDataSource&_sessionID=7f5b870e4df0a349&countries=%5B%22FR%22%5D&include_headers=false&locale=fr_FR&method=get&pretty=0&regulated_categories=%5B%5D&session_id=1409807087955&suppress_http_code=1&targeting_list=%5B%7B%22id%22%3A%226019564340583%22%2C%22type%22%3A%22behaviors%22%7D%5D&xref=f353c77137ae35')
expats_options = behavior_requets.json()

for i in expats_options['data']:
    print(f'name : {i["name"]}, id : {i["id"]}')
print('choose number ')
choice = input()
chosen = expats_options['data'][int(choice)+1]
targeting_spec= '{"genders":[0],"age_max":65,"age_min":45,"geo_locations":{"countries":["FR"],"location_types":["home","recent"]},"flexible_spec":[{"behaviors":[{"id":"%s","name":"%s"}]}]}' % (chosen['id'], chosen['name'])

params = quote(targeting_spec, safe='')


url = f'https://graph.facebook.com/v7.0/act_1047742262329813/reachestimate?access_token={token}&__activeScenarioIDs=[]&__activeScenarios=[]&_app=ADS_MANAGER&_index=163&_reqName=adaccount%2Freachestimate&_reqSrc=AdsTargetingEstimatedReach.react&_sessionID=377669edb48eb987&include_headers=false&locale=fr_FR&method=get&pretty=0&suppress_http_code=1&targeting_spec={params}&xref=f2fd6fe30bbdf3'
res = requests.get(url)

countrys = requests.get(f'https://graph.facebook.com/v2.11/search?type=adgeolocation&location_types=["country"]&access_token={token}')

