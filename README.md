# static-maps
A nodejs REST api that accepts POST json and returns a static map image for use in custom report designs or whatever you want.

## Goals
- Simple
- Send a zoom level, center coordinate, and a baselayer param and get back and map.
- Optionally send markers, icons, lines, or polylines to be overlayed on the map

### Tech stack
- [ExpressJS/Node for the glue](https://github.com/expressjs/)
- [StaticMap Python Library for making the map images](https://github.com/komoot/staticmap) This library does all the heavy lifting.
- [PythonShell for talking to Python from Node](https://github.com/extrabacon/python-shell)
- [Makizushi for on the fly icons](https://github.com/mapbox/makizushi)

### Available Basemap Options
- 'stamen-topo': Stamen Terrain
- 'stamen-toner': Stamen Toner
- 'stamen-watercolor': Stamen Watercolor
- 'osm': OSM Mapnik
- 'outdoor': Thunderforest Outdoor (150,000 tile requests per month)
- 'custom': NOTE:If you pass the string 'custom' to baseLayer you MUST include the `customBaseURL` key in the JSON payload e.g.
```json
  "baseLayer": "custom",
  "customBaseURL": "http://tiles.wmflabs.org/hillshading/${z}/${x}/${y}.png",
  "zoom": 6,
```
### TODO 
- ~~configurable styles for lines and polygons~~ (DONE)
- ~~configurable custom tile server~~ (DONE)
- ???

### Caprover (Optional)
[Caprover](https://caprover.com/) is a platform as a service. Self described as "Heroku on steroids"
The captain-definition file in this repo should work for running this on caprover once you have a server setup and operational.

### POST json body to pass the following inputs
example body of post:

POST https://your.domain.com/getStaticMap HTTP/1.1
Content-Type: application/json

```json
{
  "key": "{key-asconfigured-in-app}",
  "baseLayer": "stamen-toner",
  "zoom": 6,
  "size": "800,800",
  "center": {
    "long": -81.81,
    "lat": 33.12
  },
  "icons": [
    {
      "size": "s",
      "tint": "fc3d03",
      "symbol": "bar",
      "long": -82.503,
      "lat": 32.107
    },
    {
      "size": "s",
      "tint": "00D000",
      "symbol": "car",
      "long": -82.99,
      "lat": 32.219
    }
  ],
  "staticIcons": [
    {
      "icon": "car-15",
      "color": "blue",
      "long": -82.503,
      "lat": 32.107
    },
    {
      "icon": "hospital-15",
      "color": "blue",
      "long": -82.99,
      "lat": 32.219
    }
  ],
  "markers": [
    {
      "size": 12,
      "color": "red",
      "long": -81.81,
      "lat": 33.12,
      "outline_size": 18,
      "outline_color": "white"
    },
    {
      "size": 12,
      "color": "green",
      "long": -83.991,
      "lat": 33.32,
      "outline_size": 18,
      "outline_color": "white"
    }
  ],
  "lines": [
    {
      "color": "red",
      "stroke": 2,
      "line": [
        [-83.991, 33.32],
        [-81.81, 33.12],
        [-82.503, 32.107],
        [-82.99, 32.219]
      ]
    },
    {
      "color": "red",
      "stroke": 2,
      "line": [
        [-82.503, 32.107],
        [-82.99, 32.219]
      ]
    },
    {
      "color": "red",
      "stroke": 2,
      "line": [
        [-83.991, 33.32],
        [-82.99, 32.219],
        [-81.81, 33.12]
      ]
    }
  ],
  "polygons": [
    {
      "fill_color": "green",
      "outline_color": "black",
      "polygon": [
        [-83.991, 33.32],
        [-81.81, 33.12],
        [-82.503, 32.107],
        [-82.99, 32.219],
        [-83.991, 33.32]
      ]
    },
    {
      "fill_color": "green",
      "outline_color": "red",
      "polygon": [
        [-82.503, 32.107],
        [-82.99, 32.219],
        [-81.81, 33.12],
        [-82.503, 32.107]
      ]
    },
    {
      "fill_color": "blue",
      "outline_color": "yellow",
      "polygon": [
        [-83.991, 33.32],
        [-82.99, 32.219],
        [-81.81, 33.12],
        [-83.991, 33.32]
      ]
    }
  ]
}
```

### Example Response
```json
{
  "filepath": "http://your.domain.com/49345625-6521-46a1-a543-3ccd9668f084.png"
}
```

### Example Images

!["Example USGS Image"](usgs-example.png?raw=true "Example USGS Image")
!["Example Stamen Toner Image"](stamen-toner-example.png?raw=true "Example Stamen Toner Image")
!["Example Stamen Topo Image"](stamen-topo-example.png?raw=true "Example Stamen Topo Image")
!["Example Stamen Watercolor Image"](stamen-watercolor-example.png?raw=true "Example Stamen Watercolor Image")
!["Example OSM Mapnik Image"](osm-example.png?raw=true "Example OSM Mapnik Image")
!["Example Thunderforest Outdoor Image"](thunderforest-outdoor-example.png?raw=true "Example Thunderforest Outdoor Image")
<br/>

!["I heard you like lines dawg"](i-heard-you-like-lines-dawg.png?raw=true "I heard you like lines dawg")
