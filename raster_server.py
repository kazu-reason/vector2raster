from io import BytesIO
import os
import requests
import json
from flask import Flask, send_file, request
from geopandas import GeoDataFrame
from geojson2png import geojson2png
from geojsonDict2png import geojsonDict2png
from handle_mbtiles import read_tiles
import setting

app = Flask(__name__)

def serve_pil_image(pil_image):
    imageIO = BytesIO()
    pil_image.save(imageIO, 'PNG')
    imageIO.seek(0)
    return send_file(imageIO, mimetype='image/png')

def get_gpd_df(z,x,y):
    url = setting.GEOJSON_SRC_URL.format(z,x,y)
    response = requests.get(url)
    features = json.loads(response.text)["features"]
    df_gpd = GeoDataFrame.from_features(features).loc[:,["KEY_CODE", "geometry"]]
    im = geojson2png(
        df_gpd=df_gpd,
        tile_z=z,tile_x=x, tile_y=y,
        FIG_SIZE=256
    )

    return im


def get_geojsonDict(z,x,y,delta,table_name):
    z,x,y = int(z),int(x),int(y)
    tileCoordsList = [(z,x,y)]
    geojsonDict = read_tiles(mbtilesPath=setting.mbtiles["path"], tileCoordsList=tileCoordsList)
    im = geojsonDict2png(geojsonDict=geojsonDict[0], FIG_SIZE=256, delta=delta, table_name=table_name)

    return im

@app.route('/')
def hello():
    string = "Hellow Pillow app"
    return string

@app.route('/image-geojson/<z>/<x>/<y>')
def serve_img_geojson(z=None,x=None,y=None):
    y = y.replace('.png', '')
    im = get_gpd_df(z,x,y)
    send_content = serve_pil_image(im)
    
    return send_content


@app.route('/image-mbtiles/<z>/<x>/<y>')
def serve_img_mbtiles(z=None,x=None,y=None):
    delta = request.args.get("delta")
    date_info = request.args.get("date_info")
    table_name = f"layer_value_1_{date_info}"
    y = y.replace('.png', '')
    im = get_geojsonDict(z,x,y,delta=delta,table_name=table_name)
    send_content = serve_pil_image(im)
    
    return send_content

if __name__ == "__main__":
    app.run(debug=False)