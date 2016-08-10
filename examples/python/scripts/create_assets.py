import geojson
import json
from glob import glob
from skywiseinsight import Asset

[asset.destroy() for asset in Asset.find()]

def create_asset(gj_filename):

    # Read County GeoJSON
    with open(gj_filename, 'r') as f:
        gj = geojson.loads(f.read())

    # Create and Save Asset
    asset = Asset()
    asset.description = gj['features'][0]['properties']['name']
    asset.shape = gj['features'][0]['geometry']
    asset.save()

    return asset

def main():
    asset_ids = []

    # Create Assets
    for filename in glob('./data/*geo.json'):
        asset = create_asset(filename)
        asset_ids.append(asset.id)
        print "%s: %s" % (asset.id, asset.description)

    # Write Asset IDs to JSON File
    with open('asset_ids.json', 'w') as f:
        asset_ids_json = json.dumps({
            'asset_ids': asset_ids
        })
        f.write(asset_ids_json)

if __name__ == '__main__':
    main()
