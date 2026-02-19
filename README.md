# optimal_ev_bangkok
A geospatial optimization tool for EV charging infrastructure in Bangkok, combining OpenStreetMap data and GEE population density with Mixed-Integer Linear Programming.
⚡ Optimal EV Charging Location: Bangkok Case Study
An end-to-end geospatial optimization framework to determine the most strategic locations for Electric Vehicle (EV) charging stations in Bangkok.

📌 Project Overview
Finding the "perfect" spot for an EV station involves balancing demand, accessibility, and competition. This project uses Multi-Criteria Decision Analysis (MCDA) and Mixed-Integer Linear Programming (MILP) to automate this urban planning challenge.

Key Features

Dynamic Data Sourcing: Fetches real-time POIs (Points of Interest) from OpenStreetMap via OSMNX.

Demographic Integration: Pulls population density data from Google Earth Engine (GEE).

Mathematical Optimization: Uses the PuLP library to solve for the best 100+ locations based on benefit scores and distance constraints.

Interactive Visualization: Generates a multi-layer map with heatmaps and color-coded candidate sites.

🛠️ The Scoring Logic
The model calculates a Neighbour Point (NP) score for every potential site using the following weights:

NP 
j
​	
 =∑(αP 
j
​	
 +βQ 
j
​	
 +γR 
j
​	
 +δS 
j
​	
 )
Variable	Feature Type	Weight (α,β...)	Why?
P	Restaurants/Food	1.5	High dwell time (30-60 mins)
Q	Fuel Stations	2.0	Established traffic patterns
R	Malls/Supermarkets	1.2	Convenience & Shopping
S	Apartments	0.8	Overnight charging demand
🚀 Getting Started
1. Prerequisites

A Google Earth Engine account and project ID.

Python 3.8 or higher.

2. Installation

Clone the repository and install dependencies:

Bash
git clone https://github.com/YOUR_USERNAME/optimal_ev_bangkok.git
cd optimal_ev_bangkok
pip install -r requirements.txt
3. Environment Setup

Create a .env file in the root directory to store your GEE credentials securely:

Plaintext
GEE_PROJECT_ID=your-project-name-here
4. Running the Optimizer

Bash
python main.py
🗺️ Visualization
The script outputs an ev_optimization_map.html file featuring:

Population Heatmap: High-density areas in red/orange.

Existing Infrastructure: Current stations marked in purple.

Optimal Sites: New recommended locations color-coded by their "Benefit Score."

⚖️ License
Distributed under the MIT License. See LICENSE for more information.

🤝 Acknowledgments
Inspired by the work of Aditya9111.

Data provided by OpenStreetMap and CIESIN (via Google Earth Engine).

Pro-Tips for your GitHub:

Screenshots: Run your code, take a screenshot of the map, and save it as map_preview.png in your repo. Then update the image link in the README.

License File: Create a file named LICENSE and paste the MIT License text there.

Releases: Once it's working perfectly, use the "Create a Release" feature on GitHub to mark version v1.0.0.
