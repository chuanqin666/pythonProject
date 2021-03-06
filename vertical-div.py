from PIL import Image
import xml.etree.ElementTree as ET
from io import BytesIO
import webbrowser
import json
from jsonpath import jsonpath

with open(
          'json-doc/via_project_19Jul2022_22h46m_json_three_divs_vertical.json'
        ) as json_file:
    via_file = json.load(json_file)

# Extract element content from JSON #
filename_value = jsonpath(via_file, "$..filename")
size_value = jsonpath(via_file, "$..size")

name_shape_value = jsonpath(via_file, "$..shape_attributes.name")
x_value = jsonpath(via_file, "$..shape_attributes.x")
y_value = jsonpath(via_file, "$..shape_attributes.y")
width_value = jsonpath(via_file, "$..shape_attributes.width")
height_value = jsonpath(via_file, "$..shape_attributes.height")
element_region_value = jsonpath(via_file, "$..region_attributes.HTML element")

file_path = 'image/' + filename_value[0]

img = Image.open(file_path)
w = img.width
h = img.height


div = {}
div_css = ""

# Build ElementTree #
container = ET.Element("div")
container.set('class', 'container')

for i in range(len(x_value)):
    div[i] = ET.SubElement(container, "div")
    div[i].set('class', 'div'+str(i+1))
    div[i].text = str(i+1)

# Convert to XML #
tree = ET.ElementTree(container)
io = BytesIO()
tree.write(io)
xml = io.getvalue().decode('UTF8')

index_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        .container {
            position: relative;
            display: flex;
            flex-direction: column;
            background: url(""" + str(file_path) + """) no-repeat center;
            height: """ + str(h) + """px;
            width: """ + str(w) + """px;
            border: 5px solid black;
        }
        .div1 {
             order: 3;
             position: relative;
             text-align: center;
             font-size: 10px;
             background-color: transparent;
             height: """ + str(height_value[0]) + """px;
             width: """ + str(width_value[0]) + """px;
             margin-left: """ + str(x_value[0]) + """px;
             margin-top: """ + str(y_value[0]-y_value[2]-height_value[2]) + """px;
             outline: 5px solid yellow;

         }
        .div2 {
             order: 1;
             position: relative;
             text-align: center;
             font-size: 10px;
             background-color: transparent;
             height: """ + str(height_value[1]) + """px;
             width: """ + str(width_value[1]) + """px;
             margin-left: """ + str(x_value[1]) + """px;
             margin-top: """ + str(y_value[1]) + """px;
             outline: 5px solid yellow;

         }
        .div3 {
             order: 2;
             position: relative;
             text-align: center;
             font-size: 10px;
             background-color: transparent;
             height: """ + str(height_value[2]) + """px;
             width: """ + str(width_value[2]) + """px;
             margin-left: """ + str(x_value[2]) + """px;
             margin-top: """ + str(y_value[2]-y_value[1]-height_value[1]) + """px;
             outline: 5px solid yellow;
        }
    </style>
</head>
<body>
        """ + str(xml) + """
</body>
</html>
"""

GET_HTML = "vertical-div.html"
f = open(GET_HTML, 'w')
f.write(index_page)
f.close()

webbrowser.open("vertical-div.html")
