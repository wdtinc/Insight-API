Creating Assets from Geojson
============================

In this tutorial, we're going create assets from geojson for every county in Oklahoma using Insight's [Python client library](https://github.com/wdtinc/skywise-insight-py).

Later on, we'll show you how to create a [choropleth map](/examples/js/choropleth_map.md) using [Leaflet](http://leafletjs.com/) in your browser. 

Getting Started
---------------

Let's start off by creating a working directory and clean virtualenv:
 
```bash
mkdir tutorial && cd tutorial
virtualenv venv && source venv/bin/activate
pip install skywise-insight
```

Then, let's download and unpack our county geojson files: 

```bash
wget 