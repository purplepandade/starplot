import matplotlib
matplotlib.use('Agg')  # Set Matplotlib to use the 'Agg' backend
from datetime import datetime
from pytz import timezone
from starplot import ZenithPlot
from starplot.styles import PlotStyle, extensions
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from bs4 import BeautifulSoup

import importlib

app = Flask(__name__,
            static_url_path='/', 
            static_folder='static')
CORS(app)

@app.route('/img', methods=['GET','POST'])
def generate_image():
    if request.method == 'POST':
        data = request.get_json()
        lat = data.get('lat')
        lon = data.get('lon')
        is_dev_mode = data.get('dev')  # Check if 'dev' is set to 'true' in the request
        location_string = data.get('location')

        print(location_string)


        tz = timezone("America/Los_Angeles")
        dt = datetime(2023, 7, 13, 22, 0, tzinfo=tz)
        if is_dev_mode:
            # Reload the 'starplot.styles' module if 'dev' is set to 'true'
            importlib.reload(extensions)
        p = ZenithPlot(
            lat=lat,
            lon=lon,
            dt=dt,
            limiting_magnitude=4.6,
            style=PlotStyle().extend(
                extensions.GRAYSCALE
            ),
            resolution=2000,
            adjust_text=True,
            location = location_string

        )

        #PP: Add JSON DATA HERE
        data = {
            "name": "John Doe",
            "order": "9393939KC",
            "city": "New York",
            "heading": "Ich liebe dich!",
            "single": "Du bist die allerbeste auf der Welt, ohne dich wäre ich komplett verloren!",
            "name1": "Hasso",
            "name2": "HASSO"
        }

        order = json.dumps(data)

        image_path = "static/"+ data["order"] +".svg"
        p.export(image_path)

        with open(image_path, "r") as svgBild:
            svg_content = svgBild.read()

        with open("orders/template.html") as fp:
            fpraw = fp.read()
            newfpraw = fpraw.replace("[svg]", svg_content)
            soup = BeautifulSoup(newfpraw, 'html.parser')
            #print(soup)



        

        if "heading" in data:
            heading_div = soup.find('div', id='heading')
        if heading_div:
            heading_div.string = data.get("heading", "")

        if "single" in data:
            single_div = soup.find('div', id='single')
        if single_div:
            single_div.string = data.get("single", "")

        if "name1" in data:
            name1_div = soup.find('div', id='name1')
        if name1_div:
            name1_div.string = data.get("name1", "")

        if "name2" in data:
            name2_div = soup.find('div', id='name2')
        if name2_div:
            name2_div.string = data.get("name2", "")

        with open("orders/"+  data["order"] +".html", "w") as output_file:
            output_file.write(soup.prettify())

        return jsonify({"message": "Image generated successfully", "image_path": data["order"] +".svg"})


    elif request.method == 'GET':
        return "HI"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
