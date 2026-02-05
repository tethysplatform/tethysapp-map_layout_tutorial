import argparse
import geopandas as gp

def main(args):
    # Read the file
    gdf = gp.read_file(args.in_filename)

    # ---- DIAGNOSTICS ----
    print("Input file:", args.in_filename)
    print("CRS:", gdf.crs)
    print("Total features:", len(gdf))
    print("Empty geometries:", gdf.geometry.is_empty.sum())
    print("Null geometries:", gdf.geometry.isna().sum())
    print("----------------------")

    # Reproject
    gdf = gdf.to_crs(f"EPSG:{args.projection}")
    
    # Drop geometries that became invalid during reprojection
    gdf = gdf[gdf.geometry.notna()]
    gdf = gdf[~gdf.geometry.is_empty]
    gdf = gdf[gdf.is_valid]

    # Write output
    out_file = args.in_filename.replace(
        ".geojson", f"_{args.projection}.geojson"
    )
    gdf.to_file(out_file)
    print("Wrote:", out_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='reproject',
        description='Reproject GeoJSON files.'
    )

    parser.add_argument(
        'in_filename',
        help='The source GeoJSON file to reproject.'
    )
    parser.add_argument(
        'projection',
        help='EPSG code of target projection.'
    )

    args = parser.parse_args()
    main(args)
# import argparse
# import geopandas as gp

# def main(args):
#     gp.read_file(args.in_filename).to_crs(f'EPSG:{args.projection}').to_file(args.in_filename.replace('.geojson', f'_{args.projection}.geojson'))

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(
#         prog='reproject',
#         description='Reproject GeoJSON files.'
#     )

#     parser.add_argument('in_filename', help='The source GeoJSON file to reproject.')
#     parser.add_argument('projection', help='EPSG code of target projection.')

#     args = parser.parse_args()
#     main(args)
