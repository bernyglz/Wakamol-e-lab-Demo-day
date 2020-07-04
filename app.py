# API conect HTML - GeoRef and Predeict (USE: python -m http.server)

## Dependencies and Setup
import pandas as pd
import numpy as np
import requests
import scipy.stats as stats
import json
from flask import Flask, jsonify, render_template, request, url_for
import joblib
#from geopy.geocoders import Nominatim

# Google developer API key
from api_keys_all import google_api_key

## 

app = Flask(__name__)

#Call Models:
model_cdmx = joblib.load('cdmx_72.sav')

model_gdl = joblib.load('gdl_81.sav')

model_mty = joblib.load('mty_80.sav')

#Call Scalers:
X_Scaler_cdmx = joblib.load('X_scaler_cdmx.sav')
y_Scaler_cdmx = joblib.load('y_scaler_cdmx.sav')

X_Scaler_gdl = joblib.load('X_scaler_gdl.sav')
y_Scaler_gdl = joblib.load('y_scaler_gdl.sav')

X_Scaler_mty = joblib.load('X_scaler_mty.sav')
y_Scaler_mty = joblib.load('y_scaler_mty.sav')

#################################################
# Flask Routes
#################################################

@app.route('/')
def home():
    "Rutas disponibles:"
    "http://127.0.0.1:5000/predict/<room>/<bathroom>/<construction>/<terrain>/<direction>/<casa>/<casa_en_c>/<depto>/<nuevo>/<remate>"
    "http://127.0.0.1:5000/datos"
    return render_template('index.html')

#################################################
#@app.route('/predict/<room>/<bathroom>/<construction>/<terrain>/<direction>/<casa>/<casa_en_c>/<depto>/<nuevo>/<remate>', methods=['GET'])
@app.route('/predict/<room>/<bathroom>/<construction>/<terrain>/<direction>/<casa>/<casa_en_c>/<depto>/<nuevo>/<remate>')
def predict(room, bathroom, construction, terrain, direction, casa, casa_en_c, depto, nuevo, remate):
    
    # Datos Dummy:
    ###### 
    # http://127.0.0.1:5000/predict/2/1/80/80/Parque%Espa%C3%B1a%20la%Condesa/0/0/1/1/0
    
    # Búsqueda
    ## Function: Locate address
    # Build URL using the Google Maps API
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": direction, "key": google_api_key}
    #loop to get all locations from locaitions
    lat = []
    lon = []
    
    try:
        response = requests.get(base_url, params={"address": direction,"key": google_api_key})
        geo      = response.json()
        lat.append(geo["results"][0]["geometry"]["location"]["lat"])
        lon.append(geo["results"][0]["geometry"]["location"]["lng"])
            
    except (KeyError, IndexError):
        notfound.append(index)
       
    # Revisamos que coordenadas esten en los tres casos posibles: ZMVM, MTY, GDL
    if (lat[0] > 19.1) & (lat[0] < 19.8) & (lon[0] > - 99.4) & (lon[0] < - 98.8):
        
        # Modelo CDMX + Estado de México
        float_features = [room, bathroom, construction, terrain, lon[0], lat[0], nuevo, remate, casa, casa_en_c, depto]
        float_features = np.array(float_features).reshape(1, -1)
        float_features = X_Scaler_cdmx.transform(float_features)
        prediction = model_cdmx.predict(float_features)
        prediction = y_Scaler_cdmx.inverse_transform(prediction)
        
        output = round(prediction[0], 2)
        
    elif (lat[0] > 20.39) & (lat[0] < 20.82) & (lon[0] > - 103.59) & (lon[0] < - 103.18):
        # Modelo GDL
        float_features = [room, bathroom, construction, terrain, lon[0], lat[0], nuevo, remate, casa, casa_en_c, depto]
        float_features = np.array(float_features).reshape(1, -1)
        float_features = X_Scaler_gdl.transform(float_features)
        prediction = model_gdl.predict(float_features)
        prediction = y_Scaler_gdl.inverse_transform(prediction)
        
        output = round(prediction[0], 2)
        
    elif (lat[0] > 25.51) & (lat[0] < 25.85) & (lon[0] > - 100.53) & (lon[0] < - 100.07):
        # Modelo MTY
        float_features = [room, bathroom, construction, terrain, lon[0], lat[0], nuevo, remate, casa, casa_en_c, depto]
        float_features = np.array(float_features).reshape(1, -1)
        float_features = X_Scaler_mty.transform(float_features)
        prediction = model_mty.predict(float_features)
        prediction = y_Scaler_mty.inverse_transform(prediction)
        
        output = round(prediction[0], 2)
    
    else:
        output = 0
    
    # Return
    
    #return jsonify(output, lon, lat)
    return jsonify(output)

#################################################

if __name__ == "__main__":
    app.run(debug=True)
    
#