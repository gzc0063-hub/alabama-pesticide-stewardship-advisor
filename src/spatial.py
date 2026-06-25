import geopandas as gpd
from shapely.geometry import Point


WGS84 = "EPSG:4326"
CONUS_ALBERS = "EPSG:5070"
METERS_PER_MILE = 1609.344


def _point_gdf(lat: float, lon: float) -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame({"id": [1]}, geometry=[Point(lon, lat)], crs=WGS84)


def point_in_polygons(lat: float, lon: float, polygons: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if polygons.empty:
        return polygons
    point = Point(lon, lat)
    source = polygons
    if source.crs is None:
        source = source.set_crs(WGS84)
    return source[source.geometry.contains(point)]


def nearest_feature_distance_miles(lat: float, lon: float, polygons: gpd.GeoDataFrame) -> float | None:
    if polygons.empty:
        return None
    source = polygons
    if source.crs is None:
        source = source.set_crs(WGS84)
    projected_polygons = source.to_crs(CONUS_ALBERS)
    projected_point = _point_gdf(lat, lon).to_crs(CONUS_ALBERS).geometry.iloc[0]
    meters = projected_polygons.geometry.distance(projected_point).min()
    return float(meters / METERS_PER_MILE)
