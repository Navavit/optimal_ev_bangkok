# ⚡ Optimal EV Charging Location: Bangkok Case Study

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Google Earth Engine](https://img.shields.io/badge/Data-Google%20Earth%20Engine-green)](https://earthengine.google.com/)

An end-to-end geospatial optimization framework designed to identify the most strategic locations for Electric Vehicle (EV) charging stations in Bangkok, Thailand. This project integrates urban geometry, demographic demand, and mathematical optimization.



## 📌 Project Overview
As Bangkok transitions toward sustainable mobility, the placement of charging infrastructure is critical. This project solves the "Optimal Location Problem" by integrating:
1.  **Urban Geometry:** POIs like malls, fuel stations, and apartments from OpenStreetMap (OSMNX).
2.  **Demographic Data:** Population density from NASA/CIESIN (GPWv4) via Google Earth Engine.
3.  **Mathematical Optimization:** Mixed-Integer Linear Programming (MILP) using the PuLP library.

---

## 📊 Scoring & Optimization Logic

The model evaluates candidate locations based on a two-tier scoring system.

### 1. Neighbour Point Score (Amenity Density)
For every candidate site, we calculate a "Neighbourhood Score" ($NP_j$) based on the count of amenities within a **500m radius**. Each amenity is weighted by its relevance to EV driver behavior:

$$NP_j = \alpha P_j + \beta Q_j + \gamma R_j + \delta S_j$$

| Parameter | Weight | Amenity Category (OSM Tags) | Rationale |
| :--- | :--- | :--- | :--- |
| **$\alpha$** | **1.5** | `food_court`, `restaurant` | High dwell time (eating while charging). |
| **$\beta$** | **2.0** | `fuel` | Established refueling traffic patterns. |
| **$\gamma$** | **1.2** | `mall`, `supermarket` | Combined shopping and charging utility. |
| **$\delta$** | **0.8** | `apartments` | Residential demand/overnight charging. |

### 2. Final Benefit Score
The final suitability of a site combines the local amenity score with the population density extracted from Google Earth Engine:

$$\text{Benefit Score} = (\text{Population Density} \times 0.5) + (NP_j \times 10)$$

### 3. Optimization Objective (MILP)
The model uses **Mixed-Integer Linear Programming** to solve the following:

$$\min \sum_{j} (f_j \cdot y_j) - \sum_{j} (\text{Benefit Score}_j \cdot y_j)$$

**Constraints:**
* **Minimum Target:** The model must select at least **100** optimal locations.
* **Competition Constraint:** New stations cannot be placed within **500m** of an existing EV charging station to prevent redundancy.



---

## 🚀 Getting Started

### 1. Prerequisites
* A Google Earth Engine account.
* A GEE Project ID (Required for authentication).

### 2. Installation
```bash
# Clone this repository
git clone [https://github.com/YOUR_USERNAME/optimal_ev_bangkok.git](https://github.com/YOUR_USERNAME/optimal_ev_bangkok.git)
cd optimal_ev_bangkok

# Install dependencies
pip install -r requirements.txt
