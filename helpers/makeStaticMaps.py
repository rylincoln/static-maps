from staticmap import StaticMap, CircleMarker, IconMarker, Line, Polygon
import os
import shutil
from pathlib import Path
from datetime import datetime
import glob
import argparse
import json
from PIL import Image
import ast
import uuid

parser = argparse.ArgumentParser(description='Process some maps dawg.')
parser.add_argument('baseLayer')
parser.add_argument('center')
parser.add_argument('zoom')
parser.add_argument('size')
parser.add_argument('icons')
parser.add_argument('markers')
parser.add_argument('staticIcons')
parser.add_argument('lines')
parser.add_argument('polygons')
parser.add_argument('customBaseURL')

try:
    args = vars(parser.parse_args())

    size = args['size'].split(',')

    # which baselayer do they want? only topo at this time
    baseMapOptions = {
        # 'topo': 'https://tileify.server.com/tiles/{z}/{x}/{y}?url=https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer&transparent=true',
        'stamen-topo': 'http://tile.stamen.com/terrain/{z}/{x}/{y}.jpg',
        'stamen-toner': 'http://tile.stamen.com/toner/{z}/{x}/{y}.png',
        'stamen-watercolor': 'http://tile.stamen.com/watercolor/{z}/{x}/{y}.png',
        'osm': 'http://tile.openstreetmap.org/{z}/{x}/{y}.png',
        'outdoor': 'https://tile.thunderforest.com/outdoors/{z}/{x}/{y}.png?apikey=343191bc7cb343c083760cbcfb6a5f82',
        # 'esri-imagery': 'https://tileify.server.com/tiles/{z}/{x}/{y}?url=https%3A%2F%2Fservices.arcgisonline.com%2FArcGIS%2Frest%2Fservices%2FWorld_Imagery%2FMapServer&transparent=false',
        # 'esri-street': 'https://tileify.server.com/tiles/{z}/{x}/{y}?url=https%3A%2F%2Fservices.arcgisonline.com%2FArcGIS%2Frest%2Fservices%2FWorld_Street_Map%2FMapServer&transparent=false',
        # 'esri-lightgray': 'https://tileify.server.com/tiles/{z}/{x}/{y}?url=https%3A%2F%2Fservices.arcgisonline.com%2FArcGIS%2Frest%2Fservices%2FCanvas%2FWorld_Light_Gray_Base%2FMapServer&transparent=false',
        # 'esri-darkgray': 'https://tileify.server.com/tiles/{z}/{x}/{y}?url=https%3A%2F%2Fservices.arcgisonline.com%2FArcGIS%2Frest%2Fservices%2FCanvas%2FWorld_Dark_Gray_Base%2FMapServer&transparent=false',
        # 'esri-ocean': 'https://tileify.server.com/tiles/{z}/{x}/{y}?url=https%3A%2F%2Fservices.arcgisonline.com%2Farcgis%2Frest%2Fservices%2FOcean%2FWorld_Ocean_Base%2FMapServer&transparent=false',
        # 'tnm-imagery': 'https://tileify.server.com/tiles/{z}/{x}/{y}?url=https%3A%2F%2Fbasemap.nationalmap.gov%2Farcgis%2Frest%2Fservices%2FUSGSImageryOnly%2FMapServer&transparent=false',
        # 'tnm-imagery-topo': 'https://tileify.server.com/tiles/{z}/{x}/{y}?url=https%3A%2F%2Fbasemap.nationalmap.gov%2Farcgis%2Frest%2Fservices%2FUSGSImageryTopo%2FMapServer&transparent=false',
        # 'usgs-topo-old': 'https://tileify.server.com/tiles/{z}/{x}/{y}?url=https%3A%2F%2Fservices.arcgisonline.com%2FArcGIS%2Frest%2Fservices%2FUSA_Topo_Maps%2FMapServer&transparent=false',
        # 'shaded-relief': 'https://tileify.server.com/tiles/{z}/{x}/{y}?url=https%3A%2F%2Fbasemap.nationalmap.gov%2Farcgis%2Frest%2Fservices%2FUSGSShadedReliefOnly%2FMapServer&transparent=false',
        # 'noaa-charts': 'https://tileify.server.com/tiles/{z}/{x}/{y}?url=https%3A%2F%2Fseamlessrnc.nauticalcharts.noaa.gov%2Farcgis%2Frest%2Fservices%2FRNC%2FNOAA_RNC%2FMapServer&transparent=false',
        # 'delorme-world': 'https://tileify.server.com/tiles/{z}/{x}/{y}?url=https%3A%2F%2Fservices.arcgisonline.com%2FArcGIS%2Frest%2Fservices%2FSpecialty%2FDeLorme_World_Base_Map%2FMapServer&transparent=false',
        # 'nwi': 'https://tileify.server.com/tiles/{z}/{x}/{y}?url=https%3A%2F%2Fwww.fws.gov%2Fwetlands%2Farcgis%2Frest%2Fservices%2FWetlands%2FMapServer&transparent=true',
        # 'nhd': 'https://tileify.server.com/tiles/{z}/{x}/{y}?url=https%3A%2F%2Fbasemap.nationalmap.gov%2Farcgis%2Frest%2Fservices%2FUSGSHydroCached%2FMapServer&transparent=true',
        # 'esri-reference-world': 'https://tileify.server.com/tiles/{z}/{x}/{y}?url=https%3A%2F%2Fservices.arcgisonline.com%2FArcGIS%2Frest%2Fservices%2FReference%2FWorld_Boundaries_and_Places%2FMapServer&transparent=true',
        # 'esri-gray-reference': 'https://tileify.server.com/tiles/{z}/{x}/{y}?url=https%3A%2F%2Fservices.arcgisonline.com%2FArcGIS%2Frest%2Fservices%2FCanvas%2FWorld_Dark_Gray_Reference%2FMapServer&transparent=true',
        'custom': args['customBaseURL']
    }

    def getBaseMapURL(choice):
        return baseMapOptions.get(choice, 'topo')

    # initiate the static map
    m = StaticMap(int(size[0]), int(
        size[1]), url_template=getBaseMapURL(args['baseLayer']))

    # get current working directory
    cwd = os.getcwd()

    # add any icons
    icons = ast.literal_eval(args['icons'])
    if icons is not None:
        for icon in icons:
            img = Image.open(
                cwd + f"""/icons/{icon['symbol']}.png""").convert("RGBA")
            img.save(cwd + f"""/icons/{icon['symbol']}.png""", format="png")

            thisIcon = IconMarker((float(icon['long']), float(
                icon['lat'])), cwd + f"""/icons/{icon['symbol']}.png""", 18, 18)
            m.add_marker(thisIcon)

    # add any static Icons
    staticIcons = ast.literal_eval(args['staticIcons'])
    if staticIcons is not None:
        for icon in staticIcons:
            img = Image.open(
                cwd + f"""/icons/{icon['color']}/{icon['icon']}.png""").convert("RGBA")
            img.save(cwd + f"""/icons/{icon['color']}/{icon['icon']}.png""", format="png")

            thisIcon = IconMarker((float(icon['long']), float(
                icon['lat'])), cwd + f"""/icons/{icon['color']}/{icon['icon']}.png""", 18, 18)
            m.add_marker(thisIcon)

    # add any markers
    markers = ast.literal_eval(args['markers'])
    if markers is not None:
        for marker in markers:
            thisMarkerOutline = CircleMarker((float(marker['long']), float(
                marker['lat'])), marker['outline_color'], int(marker['outline_size']))
            m.add_marker(thisMarkerOutline)
            thisMarker = CircleMarker((float(marker['long']), float(
                marker['lat'])), marker['color'], int(marker['size']))
            m.add_marker(thisMarker)

    # add any lines
    lines = ast.literal_eval(args['lines'])
    if lines is not None:
        for line in lines:
            thisLine = Line(line['line'], line['color'], line['stroke'])
            m.add_line(thisLine)

    # add any polygons
    polygons = ast.literal_eval(args['polygons'])
    if polygons is not None:
        for polygon in polygons:
            thisPolygon = Polygon(polygon['polygon'], polygon['fill_color'], polygon['outline_color'])
            m.add_polygon(thisPolygon)

    z = int(args['zoom'])
    center = ast.literal_eval(args['center'])

    image = m.render(zoom=z, center=[float(
        center['long']), float(center['lat'])])

    filename = uuid.uuid4()

    p = Path(cwd + f"""/public/{str(filename)}.png""").absolute()
    image.save(p)

    print(f"""{str(filename)}.png""")

except (RuntimeError, TypeError, NameError) as e:
    print(e)
    pass
