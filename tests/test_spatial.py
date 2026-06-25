import geopandas as gpd
from shapely.geometry import Polygon

from src.spatial import nearest_feature_distance_miles, point_in_polygons


def sample_gdf():
    polygon = Polygon([(-86.7, 32.5), (-86.6, 32.5), (-86.6, 32.6), (-86.7, 32.6)])
    return gpd.GeoDataFrame({"name": ["sample"]}, geometry=[polygon], crs="EPSG:4326")


def test_point_in_polygons_detects_inside_point():
    result = point_in_polygons(32.55, -86.65, sample_gdf())
    assert len(result) == 1
    assert result.iloc[0]["name"] == "sample"


def test_point_in_polygons_returns_empty_for_outside_point():
    result = point_in_polygons(33.0, -87.0, sample_gdf())
    assert result.empty


def test_nearest_feature_distance_uses_projected_units():
    distance = nearest_feature_distance_miles(32.7, -86.65, sample_gdf())
    assert distance > 5
    assert distance < 15
