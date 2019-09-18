from flask import Flask, render_template, request
import json
from datetime import datetime, timezone, timedelta
import statistics
import requests

# Teralytic Soil API 
token_url = "https://hydra.teralytic.io/oauth2/token"
client_id = '487o6q7tj7ep9bvdg9ar6h4th0'
client_secret = '7cebe3dgs8rgfbk0mknlsotvneuih4c29mmb1kf0ugpodih3h3h'
# soil API call
apiKey = 'arIu2Jgvjc669S40Gzqtq2t6eZtf3nnr1dpX6Ha0'
#step A, B - single call with client credentials as the basic auth header - will return access_token
data = {'grant_type': 'client_credentials', 'scope': 'teralytic.admin'}
access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
tokens = json.loads(access_token_response.text)
accessToken = tokens['access_token']

headers = {
	'Accept': 'application/json',
	'Authorization': 'Bearer '+str(accessToken),
	'x-api-key': str(apiKey)
	
}

units = 'cm'
################################################
#DarkSky
DSapikey = "4220aeb6ebb11c7abd00a31ae35cab06"

def weather(latitude, longitude):
    LOCATION = latitude, longitude
    with forecast(DSapikey, *LOCATION) as location:
        return(location['hourly']['data'][0])

midtown = weather(40.754932, -73.984016)
brooklyn = weather(40.650002, -73.949997)
queens = weather(40.742054, -73.769417)
statenisland = weather(40.579021, -74.151535)
bronx = weather(40.837048, -73.865433)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        print(result)
        resultDic = request.form.to_dict()
        Latitude = resultDic["Latitude"]
        Longitude = resultDic["Longitude"]
        print("Latitude: " + str(Latitude))
        print("Longitude: " + str(Longitude))
        r = requests.get('https://carmack-api.teralytic.io/soildb/1.0.0/query?bounds=POINT('+Longitude+' '+Latitude+')&simplify_geometry=false&simplify_tolerance=0.5&intersection=true&geometry_fields=properties%2Cgeometry&map_unit_fields=attributes&component_fields=name%2Chorizons%2Cpercentage%2Cattributes&component_attrs=copmgrp%2Ctaxclname%2Ctaxorder%2Ctaxsuborder&horizon_fields=depth_top%2Cdepth_bottom%2Cattributes&units='+units, headers = headers)
        #print(r.json()[0])
        #soilRes = r.json()[0]['properties']['components'][1]
        soilResTop = r.json()[0]['properties']['components'][1]['horizons'][2]
        print(soilResTop)
        TopdepthTop = r.json()[0]['properties']['components'][1]['horizons'][2]['depth_top']
        print(TopdepthTop)
        TopdepthBottom = r.json()[0]['properties']['components'][1]['horizons'][2]['depth_bottom']
        print(TopdepthBottom)
        topTex = r.json()[0]['properties']['components'][1]['horizons'][2]['attributes']['chtexturegrp'][0]['texdesc']
        #print(topTex)
        topCaCo = r.json()[0]['properties']['components'][1]['horizons'][2]['attributes']['caco3_r']
        #print(topCaCo)
        topOM = r.json()[0]['properties']['components'][1]['horizons'][2]['attributes']['om_r']
        topOM = round(topOM,5)
        #print(topOM)
        topCEC = r.json()[0]['properties']['components'][1]['horizons'][2]['attributes']['cec7_r']
        topCEC = round(topCEC,5)
        topEC = r.json()[0]['properties']['components'][1]['horizons'][2]['attributes']['ec_r']
        topClay = r.json()[0]['properties']['components'][1]['horizons'][2]['attributes']['claytotal_r']
        topSand = r.json()[0]['properties']['components'][1]['horizons'][2]['attributes']['sandtotal_r']
        topSilt = r.json()[0]['properties']['components'][1]['horizons'][2]['attributes']['silttotal_r']
        topPhWater = r.json()[0]['properties']['components'][1]['horizons'][2]['attributes']['ph1to1h2o_r']
        topPhWater = round(topPhWater,5)
        topPhCaCl2 = r.json()[0]['properties']['components'][1]['horizons'][2]['attributes']['ph01mcacl2_r']
        topPhCaCl2  = round(topPhCaCl2,5)
        topCoarseSand = r.json()[0]['properties']['components'][1]['horizons'][2]['attributes']['sandco_r']
        topCoarseSand = round(topCoarseSand,5)
        topMedSand = r.json()[0]['properties']['components'][1]['horizons'][2]['attributes']['sandmed_r']
        topMedSand = round(topMedSand,5)
        topFineSand = r.json()[0]['properties']['components'][1]['horizons'][2]['attributes']['sandfine_r']
        topFineSand = round(topFineSand,5)
        topVCoarseSand = r.json()[0]['properties']['components'][1]['horizons'][2]['attributes']['sandvc_r']
        topVCoarseSand = round(topVCoarseSand,5)
        topVFineSand = r.json()[0]['properties']['components'][1]['horizons'][2]['attributes']['sandvf_r']
        topVFineSand = round(topVFineSand,5)
        ################################
        soilResMid = r.json()[0]['properties']['components'][1]['horizons'][0]
        print(soilResMid)
        MiddepthTop = r.json()[0]['properties']['components'][1]['horizons'][0]['depth_top']
        print(MiddepthTop)
        MiddepthBottom = r.json()[0]['properties']['components'][1]['horizons'][0]['depth_bottom']
        print(MiddepthBottom)
        midTex = r.json()[0]['properties']['components'][1]['horizons'][0]['attributes']['chtexturegrp'][0]['texdesc']
        #print(botTex)
        midCaCo = r.json()[0]['properties']['components'][1]['horizons'][0]['attributes']['caco3_r']
        #print(botCaCo)
        midOM = r.json()[0]['properties']['components'][1]['horizons'][0]['attributes']['om_r']
        midOM = round(midOM,5)
        #print(midOM)
        midCEC = r.json()[0]['properties']['components'][1]['horizons'][0]['attributes']['cec7_r']
        midCEC = round(midCEC,5)
        midEC = r.json()[0]['properties']['components'][1]['horizons'][0]['attributes']['ec_r']
        midClay = r.json()[0]['properties']['components'][1]['horizons'][0]['attributes']['claytotal_r']
        midSand = r.json()[0]['properties']['components'][1]['horizons'][0]['attributes']['sandtotal_r']
        midSilt = r.json()[0]['properties']['components'][1]['horizons'][0]['attributes']['silttotal_r']
        midPhWater = r.json()[0]['properties']['components'][1]['horizons'][0]['attributes']['ph1to1h2o_r']
        midPhWater = round(midPhWater,5)
        midPhCaCl2 = r.json()[0]['properties']['components'][1]['horizons'][0]['attributes']['ph01mcacl2_r']
        midPhCaCl2  = round(midPhCaCl2,5)
        midCoarseSand = r.json()[0]['properties']['components'][1]['horizons'][0]['attributes']['sandco_r']
        midCoarseSand = round(midCoarseSand,5)
        midMedSand = r.json()[0]['properties']['components'][1]['horizons'][0]['attributes']['sandmed_r']
        midMedSand = round(midMedSand,5)
        midFineSand = r.json()[0]['properties']['components'][1]['horizons'][0]['attributes']['sandfine_r']
        midFineSand = round(midFineSand,5)
        midVCoarseSand = r.json()[0]['properties']['components'][1]['horizons'][0]['attributes']['sandvc_r']
        midVCoarseSand = round(midVCoarseSand,5)
        midVFineSand = r.json()[0]['properties']['components'][1]['horizons'][0]['attributes']['sandvf_r']
        midVFineSand = round(midVFineSand,5)
        ##############################
        soilResBot = r.json()[0]['properties']['components'][1]['horizons'][1]
        print(soilResBot)
        BotdepthTop = r.json()[0]['properties']['components'][1]['horizons'][1]['depth_top']
        print(BotdepthTop)
        BotdepthBottom = r.json()[0]['properties']['components'][1]['horizons'][1]['depth_bottom']
        print(BotdepthBottom)
        botTex = r.json()[0]['properties']['components'][1]['horizons'][1]['attributes']['chtexturegrp'][0]['texdesc']
        #print(botTex)
        botCaCo = r.json()[0]['properties']['components'][1]['horizons'][1]['attributes']['caco3_r']
        #print(botCaCo)
        botOM = r.json()[0]['properties']['components'][1]['horizons'][1]['attributes']['om_r']
        botOM = round(botOM,5)
        #print(botOM)
        botCEC = r.json()[0]['properties']['components'][1]['horizons'][1]['attributes']['cec7_r']
        botCEC = round(botCEC,5)
        botEC = r.json()[0]['properties']['components'][1]['horizons'][1]['attributes']['ec_r']
        botClay = r.json()[0]['properties']['components'][1]['horizons'][1]['attributes']['claytotal_r']
        botSand = r.json()[0]['properties']['components'][1]['horizons'][1]['attributes']['sandtotal_r']
        botSilt = r.json()[0]['properties']['components'][1]['horizons'][1]['attributes']['silttotal_r']
        botPhWater = r.json()[0]['properties']['components'][1]['horizons'][1]['attributes']['ph1to1h2o_r']
        botPhWater = round(botPhWater,5)
        botPhCaCl2 = r.json()[0]['properties']['components'][1]['horizons'][1]['attributes']['ph01mcacl2_r']
        botPhCaCl2  = round(botPhCaCl2,5)
        botCoarseSand = r.json()[0]['properties']['components'][1]['horizons'][1]['attributes']['sandco_r']
        botCoarseSand = round(botCoarseSand,5)
        botMedSand = r.json()[0]['properties']['components'][1]['horizons'][1]['attributes']['sandmed_r']
        botMedSand = round(botMedSand,5)
        botFineSand = r.json()[0]['properties']['components'][1]['horizons'][1]['attributes']['sandfine_r']
        botFineSand = round(botFineSand,5)
        botVCoarseSand = r.json()[0]['properties']['components'][1]['horizons'][1]['attributes']['sandvc_r']
        botVCoarseSand = round(botVCoarseSand,5)
        botVFineSand = r.json()[0]['properties']['components'][1]['horizons'][1]['attributes']['sandvf_r']
        botVFineSand = round(botVFineSand,5)
        ############################################
        farmland =  r.json()[0]['properties']['attributes']['farmlndcl']
        #print(farmland)
        mapunit = r.json()[0]['properties']['attributes']['muname']
        
        return render_template("result.html", result=result, farmland=farmland, mapunit=mapunit, soilResTop=soilResTop, soilResMid=soilResMid, soilResBot=soilResBot, topTex=topTex, topCaCo=topCaCo, topOM=topOM, topCEC=topCEC, topEC=topEC, topClay=topClay, topSand=topSand, topSilt=topSilt, topPhWater=topPhWater, topPhCaCl2=topPhCaCl2, topCoarseSand=topCoarseSand, topMedSand=topMedSand, topFineSand=topFineSand, topVCoarseSand=topVCoarseSand, topVFineSand=topVFineSand, TopdepthTop=TopdepthTop, TopdepthBottom=TopdepthBottom, midTex=midTex, midCaCo=midCaCo, midOM=midOM, midCEC=midCEC, midEC=midEC, midClay=midClay, midSand=midSand, midSilt=midSilt, midPhWater=midPhWater, midPhCaCl2=midPhCaCl2, midCoarseSand=midCoarseSand, midMedSand=midMedSand, midFineSand=midFineSand, midVCoarseSand=midVCoarseSand, midVFineSand=midVFineSand, MiddepthTop=TopdepthTop, MiddepthBottom=MiddepthBottom, botTex=midTex, botCaCo=midCaCo, botOM=botOM, botCEC=botCEC, botEC=botEC, botClay=botClay, botSand=botSand, botSilt=botSilt, botPhWater=botPhWater, botPhCaCl2=botPhCaCl2, botCoarseSand=botCoarseSand, botMedSand=botMedSand, botFineSand=botFineSand, botVCoarseSand=botVCoarseSand, botVFineSand=botVFineSand, BotdepthTop=BotdepthTop, BotdepthBottom=BotdepthBottom)

if __name__ == "__main__":
    app.run(debug=True)