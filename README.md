# 🚩 EV Station Placement Optimization (Bangkok Case Study)

An advanced geospatial analysis project designed to identify and prioritize optimal locations for new Electric Vehicle (EV) charging stations in Bangkok. This project integrates **OpenStreetMap (OSM)**, **Google Earth Engine (GEE)**, and **Integer Programming (Optimization)** to ensure strategic placement that maximizes benefit while avoiding redundancy with existing infrastructure.



## 💡 Inspiration

This project is inspired by the conceptual framework and codebase of [Aditya9111/optimal_charging_location](https://github.com/Aditya9111/optimal_charging_location). It adapts the core logic for the Thailand context, integrating dynamic population density data from Google Earth Engine and implementing a specific "Existing Station Exclusion" constraint.



## 🛠 Installation

```bash
pip install osmnx geemap earthengine-api geopandas pulp shapely branca folium

```

*Note: A [Google Earth Engine](https://earthengine.google.com/) account and a registered project are required for authentication (`ee.Authenticate()`).*



## 📐 Mathematical Models & Equations

The project utilizes Geographic Information Systems (GIS) principles combined with mathematical optimization:

### 1. Distance Calculation (Haversine Formula)

To calculate the shortest distance between two points on the Earth's surface (Great-circle distance), ensuring higher accuracy than Euclidean distance:

* **:** Earth's radius (6,371 km)
* **:** Latitude and Longitude in radians

### 2. Neighbourhood Score

Evaluates the potential of a candidate site () within a  km radius using a Weighted Sum Model based on Points of Interest (POI):

* **:** Counts of Restaurants, Fuel Stations, Malls, and Apartments.
* **Weights:** 

### 3. Benefit Score

Combines physical infrastructure potential with social demand (Population Density):

### 4. Integer Programming Optimization

Utilizes the `PuLP` library to select the best sites through a binary decision variable .

**Objective Function:**



*(The model aims to minimize installation costs  while maximizing the total Benefit Score.)*

**Constraints:**

* **Spatial Exclusion:** If distance  km, then  (Prevents clustering near existing stations).
* **Min Station Supply:**  (Ensures at least 50 new stations are recommended).



## 📊 Workflow

1. **Data Extraction:** Fetches POIs via OSMnx and Population Density (GPWv4) via Google Earth Engine.
2. **Spatial Scoring:** Computes the Neighbourhood Score for all potential candidates (parking lots, gas stations, etc.).
3. **Conflict Checking:** Identifies existing EV stations from OSM to create "Protection Buffers."
4. **Optimization:** Runs the Linear Programming solver to find the optimal set of locations.
5. **Visualization:** Generates an interactive Folium map with toggleable layers.



## 🗺 Visualization Layers

* **Population Heatmap:** Global population density (White  Red).
* **Unselected Candidates:** Potential sites that were not prioritized by the model (Gray).
* **Existing Stations:** Current EV infrastructure from OSM (Purple).
* **Optimal Sites:** Recommended new locations (Color-coded by Benefit Score).



## 🚀 Usage

1. Set your GEE Project ID in `ee.Initialize(project='your-project-id')`.
2. Define the target area in `place_name` (e.g., "Bangkok, Thailand").
3. Execute the script; the interactive map will be displayed automatically in your notebook environment.



**Acknowledgment:** Inspired by [optimal_charging_location](https://github.com/Aditya9111/optimal_charging_location)
**Data Sources:** OpenStreetMap (OSM), Google Earth Engine (CIESIN/GPWv411)
**Tooling:** Python, PuLP, Geemap, OSMnx, Folium
