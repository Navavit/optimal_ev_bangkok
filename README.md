# optimal_ev_bangkok
A geospatial optimization tool for EV charging infrastructure in Bangkok, combining OpenStreetMap data and GEE population density with Mixed-Integer Linear Programming.
# ⚡ Optimal EV Charging Location: Bangkok Case Study

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Google Earth Engine](https://img.shields.io/badge/Data-Google%20Earth%20Engine-green)](https://earthengine.google.com/)

An end-to-end geospatial optimization framework designed to identify the most strategic locations for Electric Vehicle (EV) charging stations in Bangkok, Thailand.



## 📌 Project Overview
As Bangkok transitions toward sustainable mobility, the placement of charging infrastructure is critical. This project solves the "Optimal Location Problem" by integrating:
1.  **Urban Geometry:** POIs like malls, fuel stations, and apartments from OpenStreetMap.
2.  **Demographic Data:** Real-time population density from NASA/CIESIN via Google Earth Engine.
3.  **Mathematical Optimization:** Mixed-Integer Linear Programming (MILP) to maximize coverage while minimizing redundancy.

## 🛠️ The Scoring Logic
The model evaluates candidate sites using a **Neighbour Point ($NP_j$)** scoring system. Each surrounding amenity is weighted based on its "dwell time" (how long a driver stays there):

$$NP_j = \alpha P_j + \beta Q_j + \gamma R_j + \delta S_j$$

| Weight | Feature | Category | Rationale |
| :--- | :--- | :--- | :--- |
| **1.5 ($\alpha$)** | Restaurants | Food | High dwell time (30-60 mins) |
| **2.0 ($\beta$)** | Fuel Stations | Traffic | Established refueling habits |
| **1.2 ($\gamma$)** | Malls | Shopping | High convenience factor |
| **0.8 ($\delta$)** | Apartments | Living | Overnight/Residential demand |



## 🚀 Getting Started

### 1. Prerequisites
* A Google Earth Engine account.
* A GEE Project ID (see [Authentication](https://developers.google.com/earth-engine/guides/auth)).

### 2. Installation
```bash
# Clone this repository
git clone [https://github.com/Navavit/optimal_ev_bangkok.git](https://github.com/YOUR_USERNAME/optimal_ev_bangkok.git)
cd optimal_ev_bangkok

# Install dependencies
pip install -r requirements.txt
