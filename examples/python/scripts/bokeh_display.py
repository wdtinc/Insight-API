import json
from collections import OrderedDict
from bokeh.io import output_file, show
from bokeh.models import (GMapPlot, GMapOptions, DataRange1d,
                          ColumnDataSource, Patch)


def create_plot():
    map_options = GMapOptions(lat=35.0078, lng=-99.0929,
                              map_type="satellite", zoom=6)
    plot = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(),
                    map_options=map_options,
                    api_key="AIzaSyDehpUIZvAd-otTjK7jQ0vCR6ldDPr1JD8")
    plot.title.text = "Oklahoma Precipitation"
    return plot


color_coding = OrderedDict(sorted({
    100: '#DBDCF6',
    150: '#B7B9ED',
    200: '#9396E5',
    250: '#6F73DC',
    300: '#4B50D3',
    350: '#282ECB'
}.items(), key=lambda t: t[0]))


def plot_asset(plot, asset):

    def color(value):
        """ Returns the color range for your value."""
        color = '#FFFFFF'
        for k, v in color_coding.items():
            if value > k:
                color = v
        return color

    # The Datasource Tells Bokeh How to Plot Our Assets
    lat = [c[1] for c in asset['shape']['coordinates'][0][0]]
    lon = [c[0] for c in asset['shape']['coordinates'][0][0]]
    source = ColumnDataSource(data=dict(
        lat=lat,
        lon=lon
    ))
    patch = Patch(x="lon", y="lat", fill_color=color(asset['average_precip']))
    plot.add_glyph(source, patch)


def main():

    # Create Plot
    plot = create_plot()

    # Load Asset Glyphs
    with open('asset_data.json', 'r') as f:
        asset_json = json.loads(f.read())
    for asset in asset_json['assets']:
        plot_asset(plot, asset)

    # Display Plot
    output_file("county_map.html")
    show(plot)


if __name__ == '__main__':
    main()
