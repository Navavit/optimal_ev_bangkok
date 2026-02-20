# 1. ติดตั้ง Library ที่จำเป็น
!pip install osmnx geemap earthengine-api geopandas pulp shapely branca

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

# 2. ยืนยันตัวตน Google Earth Engine
ee.Authenticate()
ee.Initialize(project='your_project_id') # โปรเจกต์ของคุณ

# --- ส่วนที่ 1: ฟังก์ชันคณิตศาสตร์ (Haversine Formula) ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # รัศมีโลก (กม.)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# --- ส่วนที่ 2: ดึงข้อมูลจาก OSM (รวมสถานีชาร์จที่มีอยู่แล้ว) ---
place_name = "Bangkok, Thailand"
print("1/5 กำลังดึงข้อมูลจาก OSM (รวมสถานีเดิม)...")

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

# แยกกลุ่มข้อมูล p, q, r, s
p_points = get_point_gdf(all_features, "amenity in ['food_court', 'restaurant']")
q_points = get_point_gdf(all_features, "amenity == 'fuel'")
r_points = get_point_gdf(all_features, "shop in ['mall', 'supermarket']")
s_points = get_point_gdf(all_features, "building == 'apartments'")

# --- จุดชาร์จที่มีอยู่เดิม (Existing EV Stations) ---
existing_ev = get_point_gdf(all_features, "amenity == 'charging_station'")
print(f"พบสถานีชาร์จเดิมใน OSM: {len(existing_ev)} จุด")

# จุดที่สามารถติดตั้งได้ (Candidates)
candidates = get_point_gdf(all_features, "amenity in ['fuel', 'parking'] or shop == 'mall'")

# --- ส่วนที่ 3: ดึงข้อมูลประชากรจาก GEE ---
print("2/5 ดึงข้อมูลประชากรจาก GEE...")
pop_dataset = ee.ImageCollection("CIESIN/GPWv411/GPW_Population_Density").filter(ee.Filter.date('2020-01-01', '2020-12-31')).first()
pop_layer = pop_dataset.select('population_density').clip(geemap.gdf_to_ee(ox.geocode_to_gdf(place_name)))

# --- ส่วนที่ 4: คำนวณ Neighbour Point และกรองจุดใกล้สถานีเดิม ---
print("3/5 คำนวณคะแนน Neighbour Point...")

alpha, beta, gamma, delta = 1.5, 2.0, 1.2, 0.8
radius_km = 0.5

def get_neighbour_score(row):
    lat_j, lon_j = row.geometry.y, row.geometry.x
    def count_in_radius(gdf):
        if gdf is None or gdf.empty: return 0
        dist = gdf.apply(lambda x: haversine(lat_j, lon_j, x.geometry.y, x.geometry.x), axis=1)
        return len(dist[dist <= radius_km])

    return (alpha * count_in_radius(p_points)) + \
            (beta * count_in_radius(q_points)) + \
            (gamma * count_in_radius(r_points)) + \
            (delta * count_in_radius(s_points))

candidates['neighbour_point'] = candidates.apply(get_neighbour_score, axis=1)

# รวมค่าจาก GEE
ee_candidates = geemap.gdf_to_ee(candidates[['neighbour_point', 'geometry']])
poi_with_pop = geemap.extract_values_to_points(ee_candidates, pop_layer, scale=100)
final_df = geemap.ee_to_gdf(poi_with_pop)

# --- ส่วนที่ 5: Optimization พร้อมเงื่อนไข "คัดออกจุดที่มีสถานีเดิม" ---
print("4/5 เริ่มกระบวนการ Optimization (ระบบคัดออกจุดใกล้สถานีเดิม)...")
f_j = 100000
prob = LpProblem("EV_Optimization_With_Existing", LpMinimize)
indices = final_df.index.tolist()
y = LpVariable.dicts("y", indices, cat='Binary')

# Objective: Minimize Cost - Benefit
final_df['benefit_score'] = (final_df['first'].fillna(0) * 0.5) + (final_df['neighbour_point'] * 10)
prob += lpSum([f_j * y[i] for i in indices]) - lpSum([final_df.loc[i, 'benefit_score'] * y[i] for i in indices])

# --- Constraint 1: ห้ามวางใกล้สถานีเดิม (รัศมี 500 เมตร) ---
min_dist_existing = 0.5 # 500 เมตร
excluded_count = 0

for i in indices:
    point_i = final_df.loc[i].geometry
    for _, ex_ev in existing_ev.iterrows():
        dist = haversine(point_i.y, point_i.x, ex_ev.geometry.y, ex_ev.geometry.x)
        if dist < min_dist_existing:
            prob += y[i] == 0 # บังคับไม่ให้เลือกจุดนี้
            excluded_count += 1
            break

print(f"ตัดจุด Candidates ออก {excluded_count} จุด เนื่องจากใกล้สถานีเดิมเกินไป")

# --- Constraint 2: จำนวนสถานีขั้นต่ำที่ต้องการเพิ่ม ---
prob += lpSum([y[i] for i in indices]) >= 50

prob.solve()

final_df['selected'] = [value(y[i]) for i in indices]
selected_sites = final_df[final_df['selected'] == 1]

# --- ส่วนที่ 6: การแสดงผลขั้นสูง (Full Multi-Layer Visualization) ---
print("6/6 กำลังสร้างแผนที่ประมวลผลขั้นสูง...")

# 1. สร้าง Base Map
m = folium.Map(location=[13.7563, 100.5018], zoom_start=11, tiles='cartodbpositron')

# 2. เพิ่ม Layer: Heatmap ประชากรจาก GEE
# ใช้พาเลทสีขาว-เหลือง-แดง เพื่อแสดงความหนาแน่น
pop_vis = {'min': 0, 'max': 15000, 'palette': ['#ffffff', '#ffffb2', '#fd8d3c', '#e31a1c']}
map_id_dict = ee.Image(pop_layer).getMapId(pop_vis)
folium.TileLayer(
    tiles=map_id_dict['tile_fetcher'].url_format,
    attr='Google Earth Engine Population Data',
    name='1. ความหนาแน่นประชากร (Heatmap)',
    overlay=True,
    opacity=0.4
).add_to(m)

# 3. สร้างเฉดสีสำหรับจุดติดตั้งใหม่
min_score = selected_sites['benefit_score'].min()
max_score = selected_sites['benefit_score'].max()
colormap = cm.LinearColormap(
    colors=['red', 'orange', 'yellow', 'green', 'darkgreen'],
    vmin=min_score, vmax=max_score,
    caption='ระดับความเหมาะสม (Benefit Score)'
)
colormap.add_to(m)

# 4. เพิ่ม Layer: จุดที่ "ไม่ได้รับเลือก" (Unselected Candidates)
unselected_group = folium.FeatureGroup(name='2. จุดที่ไม่ได้รับเลือก (Candidates)').add_to(m)
for _, row in final_df[final_df['selected'] == 0].iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=3,
        color='gray',
        fill=True,
        fill_opacity=0.3,
        popup=f"Score: {row['benefit_score']:.2f} (ไม่ผ่านเกณฑ์)"
    ).add_to(unselected_group)

# 5. เพิ่ม Layer: สถานีชาร์จที่มีอยู่เดิม (Existing)
existing_group = folium.FeatureGroup(name='3. สถานีชาร์จเดิม (OSM)').add_to(m)
for _, row in existing_ev.iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=3,
        color='purple',
        fill=True,
        fill_opacity=0.3,
        popup="สถานีเดิม: มีรัศมีป้องกัน 500ม."
    ).add_to(existing_group)

# 6. เพิ่ม Layer: จุดติดตั้งใหม่ที่แนะนำ (Optimal Sites)
optimal_group = folium.FeatureGroup(name='4. จุดติดตั้งใหม่ (Optimal)').add_to(m)
for _, row in selected_sites.iterrows():
    score_color = colormap(row['benefit_score'])

    # สร้าง HTML Popup แสดงปัจจัยทั้งหมดที่ใช้ใน Code
    popup_html = f"""
    <div style="font-family: Arial; width: 250px;">
        <h4 style="color: green;">Optimal EV Station</h4>
        <hr>
        <b>คะแนนรวม (Benefit Score):</b> {row['benefit_score']:.2f}<br>
        <b>คะแนนสภาพแวดล้อม (Neighbour):</b> {row['neighbour_point']:.2f}<br>
        <b>ประชากร (GEE):</b> {row['first']:.0f} คน/ตร.กม.<br>
        <b>ละติจูด/ลองจิจูด:</b> {row.geometry.y:.5f}, {row.geometry.x:.5f}
        <p style="font-size: 11px; color: #666; margin-top: 10px;">
        *คำนวณตามโมเดล: f_j y_j - (GEE_Pop + Neighbour_Score)
        </p>
    </div>
    """

    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=9,
        color='black',
        weight=1,
        fill=True,
        fill_color=score_color,
        fill_opacity=0.8,
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"Score: {row['benefit_score']:.2f}"
    ).add_to(optimal_group)

# 7. เพิ่มระบบควบคุม Layer และแสดงผล
folium.LayerControl(collapsed=False).add_to(m)

print(f"สร้างแผนที่เสร็จสมบูรณ์! แสดงจุดติดตั้งใหม่ {len(selected_sites)} แห่ง")
display(m)
