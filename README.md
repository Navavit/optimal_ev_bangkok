# 🚩 EV Station Placement Optimization (Bangkok Case Study)

An advanced geospatial analysis project designed to identify and prioritize optimal locations for new Electric Vehicle (EV) charging stations in Bangkok. This project integrates **OpenStreetMap (OSM)**, **Google Earth Engine (GEE)**, and **Integer Programming (Optimization)**.

## 🖼 Preview
![Project Preview](https://github.com/Navavit/optimal_ev_bangkok/raw/main/Exsample.png)

---

## 💡 Inspiration
This project is inspired by the conceptual framework and codebase of [Aditya9111/optimal_charging_location](https://github.com/Aditya9111/optimal_charging_location). It adapts the core logic for the Thailand context, integrating dynamic population density data from Google Earth Engine and implementing a specific "Existing Station Exclusion" constraint to ensure urban planning efficiency.

---

## 📐 Mathematical Models & Equations

### 1. Distance Calculation (Haversine Formula)
To calculate the shortest distance between two points on the Earth's surface (Great-circle distance):

$$
d = 2R \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta\phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right)}\right)
$$

* **R**: Earth's radius (6,371 km)
* **$\phi, \lambda$**: Latitude and Longitude in radians

### 2. Neighbourhood Score
Evaluates the potential of a candidate site $j$ within a 0.5 km radius using a Weighted Sum Model based on Points of Interest (POI):

$$
S_j = (\alpha \cdot P_j) + (\beta \cdot Q_j) + (\gamma \cdot R_j) + (\delta \cdot S_j)
$$

* **$P, Q, R, S$**: Counts of Restaurants, Fuel Stations, Malls, and Apartments.
* **Weights**: $\alpha=1.5, \beta=2.0, \gamma=1.2, \delta=0.8$

### 3. Benefit Score
Combines physical infrastructure potential with social demand (Population Density) extracted from GEE:

$$
\text{Benefit}_j = (0.5 \times \text{Population}_j) + (10 \times S_j)
$$

### 4. Integer Programming Optimization
Utilizes the `PuLP` library to select the best sites through a binary decision variable $y_j \in \{0, 1\}$.

**Objective Function:**

$$
\text{Minimize} \quad Z = \sum_{j \in J} (f_j \cdot y_j) - \sum_{j \in J} (\text{Benefit}_j \cdot y_j)
$$

**Constraints:**
* **Spatial Exclusion:** If distance $d(j, \text{existing}) < 0.5$ km, then $y_j = 0$.
* **Min Station Supply:** $\sum_{j \in J} y_j \ge 50$.

---

## 🛠 Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/Navavit/optimal_ev_bangkok.git](https://github.com/Navavit/optimal_ev_bangkok.git)
   cd optimal_ev_bangkok


2. Install the required dependencies using requirements.txt::
   ```bash
   pip install -r requirements.txt


[!IMPORTANT]
A Google Earth Engine account and a registered project are required for authentication via ee.Authenticate().

---

## 📊 Workflow
1.Data Extraction: Fetches POIs via OSMnx and Population Density via GEE.

2.Spatial Scoring: Computes the Neighbourhood Score for all potential candidates.

3.Conflict Checking: Identifies existing EV stations to create "Protection Buffers."

4.Optimization: Runs the PuLP solver to find the optimal set of locations.

5.Visualization: Generates an interactive Folium map.

---

**Acknowledgment:** Inspired by Aditya9111/optimal_charging_location

**Data Sources:** OpenStreetMap, Google Earth Engine

**Tooling:** Python, PuLP, Geemap, OSMnx, Folium

