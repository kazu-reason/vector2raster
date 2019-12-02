from io import BytesIO
import requests
import json
from flask import Flask, send_file
from geopandas import GeoDataFrame
from geojson2png import geojson2png

app = Flask(__name__)

def serve_pil_image(pil_image):
    imageIO = BytesIO()
    pil_image.save(imageIO, 'PNG')
    imageIO.seek(0)
    return send_file(imageIO, mimetype='image/png')

@app.route('/')
def hello():
    string = "Hellow Pillow app"
    return string

@app.route('/image/<z>/<x>/<y>')
def serve_img(z=None,x=None,y=None):
    y = y.replace('.png', '')
    url = "http://localhost:8081/data/japan_smallArea/{0}/{1}/{2}.geojson".format(z,x,y)
    response = requests.get(url)
    features = json.loads(response.text)["features"]
    df_gpd = GeoDataFrame.from_features(features).loc[:,["KEY_CODE", "geometry"]]
    print(df_gpd.head(1).loc[:,"KEY_CODE"])
    im = geojson2png(
        df_gpd=df_gpd,
        tile_x=x, tile_y=y, tile_z=z,
        FIG_SIZE=256
    )
    send_content = serve_pil_image(im)
    
    return send_content

if __name__ == "__main__":
    app.run(debug=False)