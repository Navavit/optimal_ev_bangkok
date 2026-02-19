import ee
import geemap
import osmnx as ox
import geopandas as gpd
import pandas as pd
import numpy as np
import folium
import math
import branca.colormap as cm
from pulp import *
from shapely.geometry import Point
from dotenv import load_dotenv
import os

# Load credentials from .env file
load_dotenv()
GEE_PROJECT = os.getenv("GEE_PROJECT_ID")

# 1. GEE Authentication
try:
    ee.Initialize(project=GEE_PROJECT)
except Exception:
    ee.Authenticate()
    ee.Initialize(project=GEE_PROJECT)

# --- Logic: Spatial Analysis & Optimization ---

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

place_name = "Bangkok, Thailand"
print("1/5 Extracting OSM features...")

tags = {
    'amenity': ['fuel', 'parking', 'food_court', 'restaurant', 'charging_station'],
    'shop': ['mall', 'supermarket'],
    'building': ['apartments']
}
all_features = ox.features_from_place(place_name, tags)

def get_point_gdf(gdf, query_filter):
    selected = gdf.query(query_filter).copy()
    if selected.empty: return selected
    selected['geometry'] = selected.geometry.centroid
    return selected

p_points = get_point_gdf(all_features, "amenity in ['food_court', 'restaurant']")
q_points = get_point_gdf(all_features, "amenity == 'fuel'")
r_points = get_point_gdf(all_features, "shop in ['mall', 'supermarket']")
s_points = get_point_gdf(all_features, "building == 'apartments'")
existing_ev = get_point_gdf(all_features, "amenity == 'charging_station'")
candidates = get_point_gdf(all_features, "amenity in ['fuel', 'parking'] or shop == 'mall'")

print("2/5 Fetching Population Data from GEE...")
pop_dataset = ee.ImageCollection("CIESIN/GPWv411/GPW_Population_Density").filter(ee.Filter.date('2020-01-01', '2020-12-31')).first()
pop_layer = pop_dataset.select('population_density').clip(geemap.gdf_to_ee(ox.geocode_to_gdf(place_name)))

print("3/5 Calculating Neighbour Scores...")
alpha, beta, gamma, delta = 1.5, 2.0, 1.2, 0.8
radius_km = 0.5 

def get_neighbour_score(row):
    lat_j, lon_j = row.geometry.y, row.geometry.x
    def count_in_radius(gdf):
        if gdf is None or gdf.empty: return 0
        dist = gdf.apply(lambda x: haversine(lat_j, lon_j, x.geometry.y, x.geometry.x), axis=1)
        return len(dist[dist <= radius_km])
    return (alpha * count_in_radius(p_points)) + (beta * count_in_radius(q_points)) + \
           (gamma * count_in_radius(r_points)) + (delta * count_in_radius(s_points))

candidates['neighbour_point'] = candidates.apply(get_neighbour_score, axis=1)
ee_candidates = geemap.gdf_to_ee(candidates[['neighbour_point', 'geometry']])
poi_with_pop = geemap.extract_values_to_points(ee_candidates, pop_layer, scale=100)
final_df = geemap.ee_to_gdf(poi_with_pop)

print("4/5 Running MILP Optimization (PuLP)...")
f_j = 100000 
prob = LpProblem("EV_Optimization", LpMinimize)
indices = final_df.index.tolist()
y = LpVariable.dicts("y", indices, cat='Binary')

final_df['benefit_score'] = (final_df['first'].fillna(0) * 0.5) + (final_df['neighbour_point'] * 10)
prob += lpSum([f_j * y[i] for i in indices]) - lpSum([final_df.loc[i, 'benefit_score'] * y[i] for i in indices])

for i in indices:
    point_i = final_df.loc[i].geometry
    for _, ex_ev in existing_ev.iterrows():
        if haversine(point_i.y, point_i.x, ex_ev.geometry.y, ex_ev.geometry.x) < 0.5:
            prob += y[i] == 0
            break

prob += lpSum([y[i] for i in indices]) >= 100 
prob.solve(PULP_CBC_CMD(msg=0)) # Quiet mode

final_df['selected'] = [value(y[i]) for i in indices]
selected_sites = final_df[final_df['selected'] == 1]

print("5/5 Generating Map...")
m = geemap.Map(center=[13.7563, 100.5018], zoom=11)
m.add_layer(pop_layer, {'min': 0, 'max': 15000, 'palette': ['white', 'yellow', 'orange', 'red']}, 'Population Density')
# (You can continue adding the Folium markers as per your previous design here)
m.save("ev_optimization_map.html")
print("Process Complete. Map saved to ev_optimization_map.html")
