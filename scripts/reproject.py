import argparse
import geopandas as gp

def main(args):
    gp.read_file(args.in_filename).to_crs(f'EPSG:{args.projection}').to_file(args.in_filename.replace('.geojson', f'_{args.projection}.geojson'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='reproject',
        description='Reproject GeoJSON files.'
    )

    parser.add_argument('in_filename', help='The source GeoJSON file to reproject.')
    parser.add_argument('projection', help='EPSG code of target projection.')

    args = parser.parse_args()
    main(args)