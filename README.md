Here is the complete, ready-to-copy README.md for your GitHub repository. It includes all the mathematical models in LaTeX format, a clear structure, and the proper acknowledgments.
🚩 EV Station Placement Optimization (Bangkok Case Study)
An advanced geospatial analysis project designed to identify and prioritize optimal locations for new Electric Vehicle (EV) charging stations in Bangkok. This project integrates OpenStreetMap (OSM), Google Earth Engine (GEE), and Integer Programming (Optimization) to ensure strategic placement that maximizes benefit while avoiding redundancy with existing infrastructure.
💡 Inspiration
This project is inspired by the conceptual framework and codebase of Aditya9111/optimal_charging_location. It adapts the core logic for the Thailand context, integrating dynamic population density data from Google Earth Engine and implementing a specific "Existing Station Exclusion" constraint to ensure urban planning efficiency.
🛠 Installation
Bash

pip install osmnx geemap earthengine-api geopandas pulp shapely branca folium
Note: A Google Earth Engine account and a registered project are required for authentication via ee.Authenticate().
📐 Mathematical Models & Equations
The project utilizes Geographic Information Systems (GIS) principles combined with mathematical optimization:
1. Distance Calculation (Haversine Formula)
To calculate the shortest distance between two points on the Earth's surface (Great-circle distance), ensuring higher accuracy than Euclidean distance:
$$d = 2R \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta\phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right)}\right)$$
$R$: Earth's radius (6,371 km)
$\phi, \lambda$: Latitude and Longitude in radians
2. Neighbourhood Score
Evaluates the potential of a candidate site $j$ within a 0.5 km radius using a Weighted Sum Model based on Points of Interest (POI):
$$S_j = (\alpha \cdot P_j) + (\beta \cdot Q_j) + (\gamma \cdot R_j) + (\delta \cdot S_j)$$
$P, Q, R, S$: Counts of Restaurants, Fuel Stations, Malls, and Apartments.
Weights: $\alpha=1.5, \beta=2.0, \gamma=1.2, \delta=0.8$
3. Benefit Score
Combines physical infrastructure potential with social demand (Population Density) extracted from GEE satellite data:
$$\text{Benefit}_j = (0.5 \times \text{Population}_j) + (10 \times S_j)$$
4. Integer Programming Optimization
Utilizes the PuLP library to select the best sites through a binary decision variable $y_j \in \{0, 1\}$.
Objective Function:
$$\text{Minimize} \quad Z = \sum_{j \in J} (f_j \cdot y_j) - \sum_{j \in J} (\text{Benefit}_j \cdot y_j)$$
(The model aims to minimize installation costs $f_j$ while maximizing the total Benefit Score.)
Constraints:
Spatial Exclusion: If distance $d(j, \text{existing}) < 0.5$ km, then $y_j = 0$ (Prevents clustering near existing stations).
Min Station Supply: $\sum_{j \in J} y_j \ge 50$ (Ensures at least 50 new stations are recommended).
📊 Workflow
Data Extraction: Fetches POIs via OSMnx and Population Density (GPWv4) via Google Earth Engine.
Spatial Scoring: Computes the Neighbourhood Score for all potential candidates (parking lots, gas stations, etc.).
Conflict Checking: Identifies existing EV stations from OSM to create "Protection Buffers."
Optimization: Runs the Linear Programming solver to find the optimal set of locations that satisfies all constraints.
Visualization: Generates an interactive Folium map with toggleable layers and color-coded Suitability Scores.
🗺 Visualization Layers
Population Heatmap: Global population density (White $\rightarrow$ Red).
Unselected Candidates: Potential sites that were not prioritized by the model (Gray).
Existing Stations: Current EV infrastructure from OSM (Purple).
Optimal Sites: Recommended new locations (Color-coded by Benefit Score from Red to Green).
🚀 Usage
Set your GEE Project ID in ee.Initialize(project='your-project-id').
Define the target area in place_name (e.g., "Bangkok, Thailand").
Execute the script; the interactive map will be displayed automatically in your notebook environment.
Acknowledgment: Inspired by optimal_charging_location
Data Sources: OpenStreetMap (OSM), Google Earth Engine (CIESIN/GPWv411)
Tooling: Python, PuLP, Geemap, OSMnx, Folium
Would you like me to generate a sample requirements.txt file to go along with this?
