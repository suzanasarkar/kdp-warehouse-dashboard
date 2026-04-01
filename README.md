# KDP Warehouse Re-Slotting Dashboard

MSBA Internship Capstone Project for Keurig Dr Pepper Distribution Center in Sumner, Washington | University of Washington

An interactive warehouse slotting dashboard built for the KDP Sumner Distribution Center (224,000 sq ft, 5,617 bins, 281 active FG SKUs), developed as part of a client-facing internship engagement with the KDP operations team.

---

> ⚠️ DEMO VERSION - REPRESENTATIVE DATA ONLY
>
> This project was developed as a client-facing internship engagement with Keurig Dr Pepper's Sumner Distribution Center operations team. All data used in the production version of this project is proprietary and was provided directly by KDP 
>
> 
> The production version of this dashboard connects to a secure Azure SQL database containing real operational data and is intended for active use by the KDP Sumner DC operations team. That version is not publicly accessible.
> 
> All bin locations, SKU names, outbound values, ABC classifications, and warehouse metrics shown in this public demo are randomly generated and have absolutely no correlation to real KDP warehouse data, real SKU inventory, or actual Keurig Dr Pepper operations.

---

## Live Demo

[Open the Dashboard](https://kdp-warehouse-dashboard.streamlit.app/)

---

## What It Does

- Interactive bin grid - every bin in the warehouse plotted by zone and lane, color-coded by ABC classification
- Real-time search - search any SKU by name or ID and the map filters instantly
- Hover tooltips - hover over any bin to see SKU name, outbound value, zone, placement quality
- KPI dashboard - live metrics for bin utilization, zone breakdown, ABC distribution
- Warehouse floor plan - SVG map of the Sumner DC showing all zones and dock doors

---

## Color Coding

| Color | Meaning |
|---|---|
| Red | Class A - top 80% outbound value |
| Green | Class B - next 15% outbound value |
| Cyan | Class C - remaining SKUs |
| Dark grey | Empty bin |
| Gold | Blocked bin |

---

## Project Context

This dashboard is part of a year-long MSBA internship capstone project optimizing warehouse storage at KDP's Sumner Distribution Center. The full solution includes:

- ABC + Speed Classification - 281 SKUs ranked by outbound value and movement frequency
- 9-Box Priority Matrix - cross-classification driving zone assignment
- Bin Assignment Engine - priority-ranked greedy algorithm assigning every SKU to its optimal bin
- Quarterly Re-Slotting Toolkit - automated SQL pipeline to refresh assignments each quarter
- Azure SQL Database - full ETL pipeline from SAP MB51 exports

---

## Tech Stack

| Layer | Tool |
|---|---|
| Application | Python / Streamlit |
| Database | Azure SQL Server (Microsoft ODBC Driver 18) |
| Visualization | Tableau (zone heatmap, warehouse map, quarterly toolkit dashboards) |
| Language | SQL / T-SQL (Azure Data Studio) |

---

## Team

Suzana Sarkar, Sushmitha Sirigina, Evelyn Vasquez, Yeni Bakinde, Solongo Boldtseren, Bryson Chandler

University of Washington Tacoma - MSBA Program 2025-2026
