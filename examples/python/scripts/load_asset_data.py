import arrow
import json
from skywiseinsight import Asset, DailyPrecipitation

start = arrow.get('2016-04-01').datetime
end = arrow.get('2016-06-30').datetime


def main():
    with open('asset_ids.json', 'r') as f:
        assets_ids_json = json.loads(f.read())

    # Gather Assets
    assets = []
    for asset_id in assets_ids_json['asset_ids']:
        asset = Asset.find(asset_id)
        assets.append(asset)

    # Collect Precipitation Data
    asset_precip = []
    for asset in assets:
        precip = DailyPrecipitation.asset(asset.id, start=start, end=end)
        average_precip = precip.accumulationStatistics['mean']
        asset_precip.append({
            'id': asset.id,
            'average_precip': average_precip,
            'shape': asset.shape
        })
        print "%s: %.2f mm" % (asset.description, average_precip)

        # Write Precip Data to JSON File
    with open('asset_data.json', 'w') as f:
        asset_data_json = json.dumps({
            'assets': asset_precip
        })
        f.write(asset_data_json)


if __name__ == '__main__':
    main()
