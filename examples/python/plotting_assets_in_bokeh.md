Displaying Assets with Bokeh
============================

In this tutorial, we're going to create a [choropleth map](https://en.wikipedia.org/wiki/Choropleth_map) using [Bokeh](http://bokeh.pydata.org/en/latest/).

Prereqs
-------

- Complete the [Oklahoma Counties Tutorial](/examples/python/creating_assets_from_geojson.md) to create our county assets.
- `pip install bokeh skywise-insight` if you haven't already.
- [Sign Up](https://developers.google.com/maps/documentation/javascript/get-api-key) for a Google Maps API Key.

*We recommend following along in a [Jupyter Notebook](http://jupyter.org/) for this tutorial.*

Create a Bokeh Map
------------------

We'll start off by using Bokeh's [GMapPlot](http://bokeh.pydata.org/en/0.11.1/docs/user_guide/geo.html#google-maps-support) to create a base map of Oklahoma.

```python
from bokeh.io import output_file, show
from bokeh.models import GMapPlot, GMapOptions, DataRange1d

map_options = GMapOptions(lat=35.0078, lng=-99.0929,
                          map_type="satellite", zoom=6)

plot = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(),
                map_options=map_options, 
                api_key="{YOUR_MAPS_API_KEY}")
plot.title.text = "Oklahoma Precipitation"

output_file("gmap_plot.html")
show(plot)
```

![img](/static/img/bokeh_empty_map.png)

If using Jupyter, you should see a map opened by `show()`. If not, you should be able to open up the newly created `gmap_plot.html` to see our map of Oklahoma.

Add Your Assets
---------------

We'll now retrieve our assets using the client library and create Bokeh [Patch Glyphs](http://bokeh.pydata.org/en/0.11.1/docs/user_guide/plotting.html#patch-glyphs) on the map:

```python
import json
from bokeh.models import ColumnDataSource, Patch
from skywiseinsight import Asset

assets = Asset.find()

for asset in assets:
    lat=[c[1] for c in asset.shape['coordinates'][0][0]]
    lon=[c[0] for c in asset.shape['coordinates'][0][0]]
    source = ColumnDataSource(data=dict(
        lat=lat,
        lon=lon    
    ))
    patch = Patch(x="lon", y="lat", fill_color="#a6cee3")
    plot.add_glyph(source, patch)

show(plot)
```

![img](/static/img/bokeh_counties_plotted.png)


Color Coding
------------

Our assets are loaded. Let's tweak the previous code to add some meaningful information. We're going to be looking at how much precipitation each county received on average over the last 3 months. The Daily Precipitation endpoint should work perfectly for this:

```python
import arrow
import json
from collections import OrderedDict
from bokeh.models import ColumnDataSource, Patch
from skywiseinsight import Asset, DailyPrecipitation

assets = Asset.find()

color_coding = OrderedDict(sorted({
    100: '#DBDCF6',
    150: '#B7B9ED',
    200: '#9396E5',
    250: '#6F73DC',
    300: '#4B50D3',
    350: '#282ECB'
}.items(), key=lambda t: t[0]))

start = arrow.get().replace(months=-3).datetime
end = arrow.get().replace(days=-1).datetime

for asset in assets:
    patch_lat=[c[1] for c in asset.shape['coordinates'][0][0]]
    patch_lon=[c[0] for c in asset.shape['coordinates'][0][0]]

    precip = DailyPrecipitation.asset(asset.id, start=start, end=end)
    average_precip = precip.accumulationStatistics['mean']

    # Create a 
    source = ColumnDataSource(data=dict(
        lat=patch_lat,
        lon=patch_lon    
    ))
    
    color = '#FFFFFF'
    for k, v in color_coding.items():
        if k < average_precip:
            color = v
    
    patch = Patch(x="lon", y="lat", fill_color=color)
    plot.add_glyph(source, patch)
    
    print "%s: %s, %s" % (asset.description, color, str(average_precip))

show(plot)
```

![img](/static/img/bokeh_color_coded.png)
