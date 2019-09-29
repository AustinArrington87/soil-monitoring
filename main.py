from flask import Flask, render_template, request
import json
from datetime import datetime, timezone, timedelta
import statistics
import requests

# Teralytic Soil API 
token_url = "https://hydra.teralytic.io/oauth2/token"
client_id = 'ENTER_CLIENT_ID'
client_secret = 'ENTER_CLIENT_SECRET'
# soil API call
apiKey = 'ENTER API KEY'
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
        try:
            r = requests.get('https://carmack-api.teralytic.io/soildb/1.0.0/query?bounds=POINT('+Longitude+' '+Latitude+')&simplify_geometry=false&simplify_tolerance=0.5&intersection=true&geometry_fields=properties%2Cgeometry&map_unit_fields=attributes&component_fields=name%2Chorizons%2Cpercentage%2Cattributes&component_attrs=copmgrp%2Ctaxclname%2Ctaxorder%2Ctaxsuborder&horizon_fields=depth_top%2Cdepth_bottom%2Cattributes&units='+units, headers = headers)
            #print(r.json()[0])
            depthArray = []
            p1 = 0
            p2 = 0
            p3 = 0
            
            try:
                soilD1 = r.json()[0]['properties']['components'][1]['horizons'][0]['depth_top']
                print("soilD1: " + str(soilD1))
                depthArray.append(soilD1)
            except:
                pass
            try:
                soilD2 = r.json()[0]['properties']['components'][1]['horizons'][1]['depth_top']
                print("soilD2: " + str(soilD2))
                depthArray.append(soilD2)
            except:
                pass
            try:
                soilD3 = r.json()[0]['properties']['components'][1]['horizons'][2]['depth_top']
                print("soilD3: " + str(soilD3))
                depthArray.append(soilD3)
            except:
                pass
            try:
                soilD4 = r.json()[0]['properties']['components'][1]['horizons'][3]['depth_top']
                print("soilD4: " + str(soilD4))
                depthArray.append(soilD4)
            except:
                pass
            try:
                soilD5 = r.json()[0]['properties']['components'][1]['horizons'][4]['depth_top']
                print("soilD5: " + str(soilD5))
                depthArray.append(soilD5)
            except:
                pass
                
            print(depthArray)
            sortedDepth = sorted(depthArray)
            print(sortedDepth)
            try:
                p1 = sortedDepth[0]
                print("Position1: " + str(p1))
            except:
                pass
            try:
                p2 = sortedDepth[1]
                print("Position2: " + str(p2))
            except:
                pass
            try:
                p3 = sortedDepth[2]
                print("Position3: " + str(p3))
            except:
                pass
            try:
                p4 = sortedDepth[3]
                print("Position4: " + str(p4))
            except:
                pass
            try:
                p5 = sortedDepth[4]
                print("Position5: "  + str(p5))
            except:
                pass
            
            try:
                p1Index = depthArray.index(p1)
                print("p1 Index: " + str(p1Index))
            except:
                pass
            try:
                p2Index = depthArray.index(p2)
                print("p2 Index: " + str(p2Index))
            except:
                pass
            try:
                p3Index = depthArray.index(p3)
                print("p3 Index: " + str(p3Index))
            except:
                pass
            try:
                p4Index = depthArray.index(p4)
                print("p4 Index: " + str(p4Index))
            except:
                pass
            try:
                p5Index = depthArray.index(p5)
                print("p5 Index: " + str(p5Index))
            except:
                pass
                
            try:
                soilRes1 = r.json()[0]['properties']['components'][1]['horizons'][p1Index]
                print(soilRes1)
                OnedepthTop = r.json()[0]['properties']['components'][1]['horizons'][p1Index]['depth_top']
                OnedepthBottom = r.json()[0]['properties']['components'][1]['horizons'][p1Index]['depth_bottom']
                oneTex = r.json()[0]['properties']['components'][1]['horizons'][p1Index]['attributes']['chtexturegrp'][0]['texdesc']
                oneCaCo = r.json()[0]['properties']['components'][1]['horizons'][p1Index]['attributes']['caco3_r']
                oneOM = r.json()[0]['properties']['components'][1]['horizons'][p1Index]['attributes']['om_r']
                oneOM = round(oneOM,5)
                oneCEC = r.json()[0]['properties']['components'][1]['horizons'][p1Index]['attributes']['cec7_r']
                oneCEC = round(oneCEC,5)
                oneEC = r.json()[0]['properties']['components'][1]['horizons'][p1Index]['attributes']['ec_r']
                oneClay = r.json()[0]['properties']['components'][1]['horizons'][p1Index]['attributes']['claytotal_r']
                oneSand = r.json()[0]['properties']['components'][1]['horizons'][p1Index]['attributes']['sandtotal_r']
                oneSilt = r.json()[0]['properties']['components'][1]['horizons'][p1Index]['attributes']['silttotal_r']
                onePhWater = r.json()[0]['properties']['components'][1]['horizons'][p1Index]['attributes']['ph1to1h2o_r']
                onePhWater = round(onePhWater,5)
                onePhCaCl2 = r.json()[0]['properties']['components'][1]['horizons'][p1Index]['attributes']['ph01mcacl2_r']
                onePhCaCl2  = round(onePhCaCl2,5)
                oneCoarseSand = r.json()[0]['properties']['components'][1]['horizons'][p1Index]['attributes']['sandco_r']
                oneCoarseSand = round(oneCoarseSand,5)
                oneMedSand = r.json()[0]['properties']['components'][1]['horizons'][p1Index]['attributes']['sandmed_r']
                oneMedSand = round(oneMedSand,5)
                oneFineSand = r.json()[0]['properties']['components'][1]['horizons'][p1Index]['attributes']['sandfine_r']
                oneFineSand = round(oneFineSand,5)
                oneVCoarseSand = r.json()[0]['properties']['components'][1]['horizons'][p1Index]['attributes']['sandvc_r']
                oneVCoarseSand = round(oneVCoarseSand,5)
                oneVFineSand = r.json()[0]['properties']['components'][1]['horizons'][p1Index]['attributes']['sandvf_r']
                oneVFineSand = round(oneVFineSand,5)
            except:
                soilRes1 = None
                OnedepthTop = None
                OnedepthBottom = None
                oneTex = None
                oneCaCo = None
                oneOM = None
                oneCEC = None
                oneEC = None
                oneClay = None
                oneSand = None
                oneSilt = None
                onePhWater = None
                onePhCaCl2 = None
                oneCoarseSand = None
                oneMedSand = None
                oneFineSand = None
                oneVCoarseSand = None
                oneVFineSand = None
                
            ################################
            try:
                soilRes2 = r.json()[0]['properties']['components'][1]['horizons'][p2Index]
                print(soilRes2)
                TwodepthTop = r.json()[0]['properties']['components'][1]['horizons'][p2Index]['depth_top']
                TwodepthBottom = r.json()[0]['properties']['components'][1]['horizons'][p2Index]['depth_bottom']
                twoTex = r.json()[0]['properties']['components'][1]['horizons'][p2Index]['attributes']['chtexturegrp'][0]['texdesc']
                twoCaCo = r.json()[0]['properties']['components'][1]['horizons'][p2Index]['attributes']['caco3_r']
                twoOM = r.json()[0]['properties']['components'][1]['horizons'][p2Index]['attributes']['om_r']
                twoOM = round(twoOM,5)
                twoCEC = r.json()[0]['properties']['components'][1]['horizons'][p2Index]['attributes']['cec7_r']
                twoCEC = round(twoCEC,5)
                twoEC = r.json()[0]['properties']['components'][1]['horizons'][p2Index]['attributes']['ec_r']
                twoClay = r.json()[0]['properties']['components'][1]['horizons'][p2Index]['attributes']['claytotal_r']
                twoSand = r.json()[0]['properties']['components'][1]['horizons'][p2Index]['attributes']['sandtotal_r']
                twoSilt = r.json()[0]['properties']['components'][1]['horizons'][p2Index]['attributes']['silttotal_r']
                twoPhWater = r.json()[0]['properties']['components'][1]['horizons'][p2Index]['attributes']['ph1to1h2o_r']
                twoPhWater = round(twoPhWater,5)
                twoPhCaCl2 = r.json()[0]['properties']['components'][1]['horizons'][p2Index]['attributes']['ph01mcacl2_r']
                twoPhCaCl2  = round(twoPhCaCl2,5)
                twoCoarseSand = r.json()[0]['properties']['components'][1]['horizons'][p2Index]['attributes']['sandco_r']
                twoCoarseSand = round(twoCoarseSand,5)
                twoMedSand = r.json()[0]['properties']['components'][1]['horizons'][p2Index]['attributes']['sandmed_r']
                twoMedSand = round(twoMedSand,5)
                twoFineSand = r.json()[0]['properties']['components'][1]['horizons'][p2Index]['attributes']['sandfine_r']
                twoFineSand = round(twoFineSand,5)
                twoVCoarseSand = r.json()[0]['properties']['components'][1]['horizons'][p2Index]['attributes']['sandvc_r']
                twoVCoarseSand = round(twoVCoarseSand,5)
                twoVFineSand = r.json()[0]['properties']['components'][1]['horizons'][p2Index]['attributes']['sandvf_r']
                twoVFineSand = round(twoVFineSand,5)
            except:
                soilRes2 = None
                TwodepthTop = None
                TwodepthBottom = None
                twoTex = None
                twoCaCo = None
                twoOM = None
                twoCEC = None
                twoEC = None
                twoClay = None
                twoSand = None
                twoSilt = None
                twoPhWater = None
                twoPhCaCl2 = None
                twoCoarseSand = None
                twoMedSand = None
                twoFineSand = None
                twoVCoarseSand = None
                twoVFineSand = None
            ##############################
            try:
                soilRes3 = r.json()[0]['properties']['components'][1]['horizons'][p3Index]
                print(soilRes3)
                ThreedepthTop = r.json()[0]['properties']['components'][1]['horizons'][p3Index]['depth_top']
                ThreedepthBottom = r.json()[0]['properties']['components'][1]['horizons'][p3Index]['depth_bottom']
                threeTex = r.json()[0]['properties']['components'][1]['horizons'][p3Index]['attributes']['chtexturegrp'][0]['texdesc']
                threeCaCo = r.json()[0]['properties']['components'][1]['horizons'][p3Index]['attributes']['caco3_r']
                threeOM = r.json()[0]['properties']['components'][1]['horizons'][p3Index]['attributes']['om_r']
                threeOM = round(threeOM,5)
                threeCEC = r.json()[0]['properties']['components'][1]['horizons'][p3Index]['attributes']['cec7_r']
                threeCEC = round(threeCEC,5)
                threeEC = r.json()[0]['properties']['components'][1]['horizons'][p3Index]['attributes']['ec_r']
                threeClay = r.json()[0]['properties']['components'][1]['horizons'][p3Index]['attributes']['claytotal_r']
                threeSand = r.json()[0]['properties']['components'][1]['horizons'][p3Index]['attributes']['sandtotal_r']
                threeSilt = r.json()[0]['properties']['components'][1]['horizons'][p3Index]['attributes']['silttotal_r']
                threePhWater = r.json()[0]['properties']['components'][1]['horizons'][p3Index]['attributes']['ph1to1h2o_r']
                threePhWater = round(threePhWater,5)
                threePhCaCl2 = r.json()[0]['properties']['components'][1]['horizons'][p3Index]['attributes']['ph01mcacl2_r']
                threePhCaCl2  = round(threePhCaCl2,5)
                threeCoarseSand = r.json()[0]['properties']['components'][1]['horizons'][p3Index]['attributes']['sandco_r']
                threeCoarseSand = round(threeCoarseSand,5)
                threeMedSand = r.json()[0]['properties']['components'][1]['horizons'][p3Index]['attributes']['sandmed_r']
                threeMedSand = round(threeMedSand,5)
                threeFineSand = r.json()[0]['properties']['components'][1]['horizons'][p3Index]['attributes']['sandfine_r']
                threeFineSand = round(threeFineSand,5)
                threeVCoarseSand = r.json()[0]['properties']['components'][1]['horizons'][p3Index]['attributes']['sandvc_r']
                threeVCoarseSand = round(threeVCoarseSand,5)
                threeVFineSand = r.json()[0]['properties']['components'][1]['horizons'][p3Index]['attributes']['sandvf_r']
                threeVFineSand = round(threeVFineSand,5)
            except:
                soilRes3 = None
                ThreedepthTop = None
                ThreedepthBottom = None
                threeTex = None
                threeCaCo = None
                threeOM = None
                threeCEC = None
                threeEC = None
                threeClay = None
                threeSand = None
                threeSilt = None
                threePhWater = None
                threePhCaCl2 = None
                threeCoarseSand = None
                threeMedSand = None
                threeFineSand = None
                threeVCoarseSand = None
                threeVFineSand = None
            ###########################################
            try:
                soilRes4 = r.json()[0]['properties']['components'][1]['horizons'][p4Index]
                print(soilRes4)
                FourdepthTop = r.json()[0]['properties']['components'][1]['horizons'][p4Index]['depth_top']
                FourdepthBottom = r.json()[0]['properties']['components'][1]['horizons'][p4Index]['depth_bottom']
                fourTex = r.json()[0]['properties']['components'][1]['horizons'][p4Index]['attributes']['chtexturegrp'][0]['texdesc']
                fourCaCo = r.json()[0]['properties']['components'][1]['horizons'][p4Index]['attributes']['caco3_r']
                fourOM = r.json()[0]['properties']['components'][1]['horizons'][p4Index]['attributes']['om_r']
                fourOM = round(fourOM,5)
                fourCEC = r.json()[0]['properties']['components'][1]['horizons'][p4Index]['attributes']['cec7_r']
                fourCEC = round(fourCEC,5)
                fourEC = r.json()[0]['properties']['components'][1]['horizons'][p4Index]['attributes']['ec_r']
                fourClay = r.json()[0]['properties']['components'][1]['horizons'][p4Index]['attributes']['claytotal_r']
                fourSand = r.json()[0]['properties']['components'][1]['horizons'][p4Index]['attributes']['sandtotal_r']
                fourSilt = r.json()[0]['properties']['components'][1]['horizons'][p4Index]['attributes']['silttotal_r']
                fourPhWater = r.json()[0]['properties']['components'][1]['horizons'][p4Index]['attributes']['ph1to1h2o_r']
                fourPhWater = round(fourPhWater,5)
                fourPhCaCl2 = r.json()[0]['properties']['components'][1]['horizons'][p4Index]['attributes']['ph01mcacl2_r']
                fourPhCaCl2  = round(fourPhCaCl2,5)
                fourCoarseSand = r.json()[0]['properties']['components'][1]['horizons'][p4Index]['attributes']['sandco_r']
                fourCoarseSand = round(fourCoarseSand,5)
                fourMedSand = r.json()[0]['properties']['components'][1]['horizons'][p4Index]['attributes']['sandmed_r']
                fourMedSand = round(fourMedSand,5)
                fourFineSand = r.json()[0]['properties']['components'][1]['horizons'][p4Index]['attributes']['sandfine_r']
                fourFineSand = round(fourFineSand,5)
                fourVCoarseSand = r.json()[0]['properties']['components'][1]['horizons'][p4Index]['attributes']['sandvc_r']
                fourVCoarseSand = round(fourVCoarseSand,5)
                fourVFineSand = r.json()[0]['properties']['components'][1]['horizons'][p4Index]['attributes']['sandvf_r']
                fourVFineSand = round(fourVFineSand,5)
            except:
                soilRes4 = None
                FourdepthTop = None
                FourdepthBottom = None
                fourTex = None
                fourCaCo = None
                fourOM = None
                fourCEC = None
                fourEC = None
                fourClay = None
                fourSand = None
                fourSilt = None
                fourPhWater = None
                fourPhCaCl2 = None
                fourCoarseSand = None
                fourMedSand = None
                fourFineSand = None
                fourVCoarseSand = None
                fourVFineSand = None
            try:
                soilRes5 = r.json()[0]['properties']['components'][1]['horizons'][p5Index]
                print(soilRes5)
                FivedepthTop = r.json()[0]['properties']['components'][1]['horizons'][p5Index]['depth_top']
                FivedepthBottom = r.json()[0]['properties']['components'][1]['horizons'][p5Index]['depth_bottom']
                fiveTex = r.json()[0]['properties']['components'][1]['horizons'][p5Index]['attributes']['chtexturegrp'][0]['texdesc']
                fiveCaCo = r.json()[0]['properties']['components'][1]['horizons'][p5Index]['attributes']['caco3_r']
                fiveOM = r.json()[0]['properties']['components'][1]['horizons'][p5Index]['attributes']['om_r']
                fiveOM = round(fiveOM,5)
                fiveCEC = r.json()[0]['properties']['components'][1]['horizons'][p5Index]['attributes']['cec7_r']
                fiveCEC = round(fiveCEC,5)
                fiveEC = r.json()[0]['properties']['components'][1]['horizons'][p5Index]['attributes']['ec_r']
                fiveClay = r.json()[0]['properties']['components'][1]['horizons'][p5Index]['attributes']['claytotal_r']
                fiveSand = r.json()[0]['properties']['components'][1]['horizons'][p5Index]['attributes']['sandtotal_r']
                fiveSilt = r.json()[0]['properties']['components'][1]['horizons'][p5Index]['attributes']['silttotal_r']
                fivePhWater = r.json()[0]['properties']['components'][1]['horizons'][p5Index]['attributes']['ph1to1h2o_r']
                fivePhWater = round(fivePhWater,5)
                fivePhCaCl2 = r.json()[0]['properties']['components'][1]['horizons'][p5Index]['attributes']['ph01mcacl2_r']
                fivePhCaCl2  = round(fivePhCaCl2,5)
                fiveCoarseSand = r.json()[0]['properties']['components'][1]['horizons'][p5Index]['attributes']['sandco_r']
                fiveCoarseSand = round(fiveCoarseSand,5)
                fiveMedSand = r.json()[0]['properties']['components'][1]['horizons'][p5Index]['attributes']['sandmed_r']
                fiveMedSand = round(fiveMedSand,5)
                fiveFineSand = r.json()[0]['properties']['components'][1]['horizons'][p5Index]['attributes']['sandfine_r']
                fiveFineSand = round(fiveFineSand,5)
                fiveVCoarseSand = r.json()[0]['properties']['components'][1]['horizons'][p5Index]['attributes']['sandvc_r']
                fiveVCoarseSand = round(fiveVCoarseSand,5)
                fiveVFineSand = r.json()[0]['properties']['components'][1]['horizons'][p5Index]['attributes']['sandvf_r']
                fiveVFineSand = round(fiveVFineSand,5)
            except:
                soilRes5 = None
                FivedepthTop = None
                FivedepthBottom = None
                fiveTex = None
                fiveCaCo = None
                fiveOM = None
                fiveCEC = None
                fiveEC = None
                fiveClay = None
                fiveSand = None
                fiveSilt = None
                fivePhWater = None
                fivePhCaCl2 = None
                fiveCoarseSand = None
                fiveMedSand = None
                fiveFineSand = None
                fiveVCoarseSand = None
                fiveVFineSand = None                
            ############################################
            ############################################
            farmland =  r.json()[0]['properties']['attributes']['farmlndcl']
            #print(farmland)
            mapunit = r.json()[0]['properties']['attributes']['muname']
        except:
            print("No horizon data for selected point")
            soilRes1 = None
            OnedepthTop = None
            OnedepthBottom = None
            oneTex = None
            oneCaCo = None
            oneOM = None
            oneCEC = None
            oneEC = None
            oneClay = None
            oneSand = None
            oneSilt = None
            onePhWater = None
            onePhCaCl2 = None
            oneCoarseSand = None
            oneMedSand = None
            oneFineSand = None
            oneVCoarseSand = None
            oneVFineSand = None
            oneVFineSand = None
            ################################
            soilRes2 = None
            TwodepthTop = None
            TwodepthBottom = None
            twoTex = None
            twoCaCo = None
            twoOM = None
            twoCEC = None
            twoEC = None
            twoClay = None
            twoSand = None
            twoSilt = None
            twoPhWater = None
            twoPhCaCl2 = None
            twoCoarseSand = None
            twoMedSand = None
            twoFineSand = None
            twoVCoarseSand = None
            twoVFineSand = None
            ##############################
            soilRes3 = None
            ThreedepthTop = None
            ThreedepthBottom = None
            threeTex = None
            threeCaCo = None
            threeOM = None
            threeCEC = None
            threeEC = None
            threeClay = None
            threeSand = None
            threeSilt = None
            threePhWater = None
            threePhWater = None
            threePhCaCl2 = None
            threeCoarseSand = None
            threeCoarseSand = None
            threeMedSand = None
            threeFineSand = None
            threeVCoarseSand = None
            threeVFineSand = None
            ############################
            soilRes4 = None
            FourdepthTop = None
            FourdepthBottom = None
            fourTex = None
            fourCaCo = None
            fourOM = None
            fourCEC = None
            fourEC = None
            fourClay = None
            fourSand = None
            fourSilt = None
            fourPhWater = None
            fourPhWater = None
            fourPhCaCl2 = None
            fourCoarseSand = None
            fourCoarseSand = None
            fourMedSand = None
            fourFineSand = None
            fourVCoarseSand = None
            fourVFineSand = None
            #############################
            soilRes5 = None
            FivedepthTop = None
            FivedepthBottom = None
            fiveTex = None
            fiveCaCo = None
            fiveOM = None
            fiveCEC = None
            fiveEC = None
            fiveClay = None
            fiveSand = None
            fiveSilt = None
            fivePhWater = None
            fivePhWater = None
            fivePhCaCl2 = None
            fiveCoarseSand = None
            fiveCoarseSand = None
            fiveMedSand = None
            fiveFineSand = None
            fiveVCoarseSand = None
            fiveVFineSand = None
            #############################
            farmland = None
            mapunit = None
            
            
        return render_template("result.html", result=result, farmland=farmland, mapunit=mapunit, soilRes1=soilRes1, soilRes2=soilRes2, soilRes3=soilRes3, soilRes4=soilRes4, oneTex=oneTex, oneCaCo=oneCaCo, oneOM=oneOM, oneCEC=oneCEC, oneEC=oneEC, oneClay=oneClay, oneSand=oneSand, oneSilt=oneSilt, onePhWater=onePhWater, onePhCaCl2=onePhCaCl2, oneCoarseSand=oneCoarseSand, oneMedSand=oneMedSand, oneFineSand=oneFineSand, oneVCoarseSand=oneVCoarseSand, oneVFineSand=oneVFineSand, OnedepthTop=OnedepthTop, OnedepthBottom=OnedepthBottom, twoTex=twoTex, twoCaCo=twoCaCo, twoOM=twoOM, twoCEC=twoCEC, twoEC=twoEC, twoClay=twoClay, twoSand=twoSand, twoSilt=twoSilt, twoPhWater=twoPhWater, twoPhCaCl2=twoPhCaCl2, twoCoarseSand=twoCoarseSand, twoMedSand=twoMedSand, twoFineSand=twoFineSand, twoVCoarseSand=twoVCoarseSand, twoVFineSand=twoVFineSand, TwodepthTop=TwodepthTop, TwodepthBottom=TwodepthBottom, threeTex=threeTex, threeCaCo=threeCaCo, threeOM=threeOM, threeCEC=threeCEC, threeEC=threeEC, threeClay=threeClay, threeSand=threeSand, threeSilt=threeSilt, threePhWater=threePhWater, threePhCaCl2=threePhCaCl2, threeCoarseSand=threeCoarseSand, threeMedSand=threeMedSand, threeFineSand=threeFineSand, threeVCoarseSand=threeVCoarseSand, threeVFineSand=threeVFineSand, ThreedepthTop=ThreedepthTop, ThreedepthBottom=ThreedepthBottom, fourTex=fourTex, fourCaCo=fourCaCo, fourOM=fourOM, fourCEC=fourCEC, fourEC=fourEC, fourClay=fourClay, fourSand=fourSand, fourSilt=fourSilt, fourPhWater=fourPhWater, fourPhCaCl2=fourPhCaCl2, fourCoarseSand=fourCoarseSand, fourMedSand=fourMedSand, fourFineSand=fourFineSand, fourVCoarseSand=fourVCoarseSand, fourVFineSand=fourVFineSand, FourdepthTop=FourdepthTop, FourdepthBottom=FourdepthBottom, fiveTex=fiveTex, fiveCaCo=fiveCaCo, fiveOM=fiveOM, fiveCEC=fiveCEC, fiveEC=fiveEC, fiveClay=fiveClay, fiveSand=fiveSand, fiveSilt=fiveSilt, fivePhWater=fivePhWater, fivePhCaCl2=fivePhCaCl2, fiveCoarseSand=fiveCoarseSand, fiveMedSand=fiveMedSand, fiveFineSand=fiveFineSand, fiveVCoarseSand=fiveVCoarseSand, fiveVFineSand=fiveVFineSand, FivedepthTop=FivedepthTop, FivedepthBottom=FivedepthBottom)

if __name__ == "__main__":
    app.run(debug=True)
