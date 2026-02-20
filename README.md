This is a fantastic project—geospatial optimization is a high-impact area, especially for urban planning in a city as dense as Bangkok. To make your README/Documentation pop, I’ve cleaned up the hierarchy, added visual markers, and organized the technical specs into more readable segments.

---

# 🚩 EV Station Placement Optimization

### *Bangkok Case Study*

An advanced geospatial analysis project designed to identify and prioritize optimal locations for new Electric Vehicle (EV) charging stations in Bangkok. This project integrates **OpenStreetMap (OSM)**, **Google Earth Engine (GEE)**, and **Integer Programming** to ensure strategic placement that maximizes utility while avoiding infrastructure redundancy.

---

## 🛠 Installation & Setup

```bash
pip install osmnx geemap earthengine-api geopandas pulp shapely branca folium

```

*Note: A **Google Earth Engine** account and a registered project are required for authentication via `ee.Authenticate()`.*

---

## 📐 Mathematical Framework

The project balances physical infrastructure with social demand using GIS principles and mathematical optimization.

### 1. Distance Calculation (Haversine Formula)

To ensure accuracy over the Earth's curvature, we calculate the Great-circle distance rather than simple Euclidean distance:

* ****: Earth's radius (6,371 km)
* ****: Latitude and Longitude in radians

### 2. The Scoring Models

We evaluate potential sites within a **0.5 km radius** using a two-tier scoring system:

| Metric | Formula / Components |
| --- | --- |
| **Neighbourhood Score ()** |  |
| **Weights** |  (Rest.),  (Fuel),  (Malls),  (Apt.) |
| **Benefit Score** |  |

### 3. Integer Programming Optimization

Utilizing the **PuLP** library, we define a binary decision variable .

**Objective Function:**


**Constraints:**

* **Spatial Exclusion:** If  km, then .
* **Supply Minimum:**  (Ensures a minimum of 50 new recommendations).

---

## 📊 Project Workflow

1. **Data Extraction:** Pulls POIs via **OSMnx** and Population Density (GPWv4) via **Google Earth Engine**.
2. **Spatial Scoring:** Computes the Neighbourhood Score for all potential candidates (parking lots, gas stations, etc.).
3. **Conflict Checking:** Identifies existing EV stations to create "Protection Buffers."
4. **Optimization:** Runs the Linear Programming solver to find the optimal set of locations.
5. **Visualization:** Generates an interactive **Folium** map with toggleable layers.

---

## 🗺 Visualization Layers

* 🔴 **Population Heatmap:** Global population density (White  Red).
* ⚪ **Unselected Candidates:** Potential sites not prioritized by the model.
* 🟣 **Existing Stations:** Current EV infrastructure from OSM.
* 🟢 **Optimal Sites:** Recommended locations (Color-coded by Benefit Score).

---

## 🚀 Quick Start

1. **Initialize GEE:** Set your Project ID in `ee.Initialize(project='your-project-id')`.
2. **Define Area:** Set `place_name = "Bangkok, Thailand"`.
3. **Run:** Execute the script to generate the interactive map in your notebook.

---

**💡 Inspiration:** This project adapts the core logic of [Aditya9111/optimal_charging_location](https://github.com/Aditya9111/optimal_charging_location) for the Thailand context, integrating dynamic GEE data and specific urban planning constraints.

**Data Sources:** OpenStreetMap (OSM), Google Earth Engine (CIESIN/GPWv411)

Would you like me to help you draft a specific **"Results & Discussion"** section based on the typical outputs of this Bangkok model?
