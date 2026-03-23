# KDP Sumner DC — Warehouse Re-Slotting Dashboard

**MSBA Team 3 | University of Washington Tacoma | Keurig Dr Pepper Capstone Project**

An interactive warehouse slotting dashboard built for the KDP Sumner Distribution Center (224,000 sq ft, 5,617 bins, 281 active FG SKUs).

## Live Demo

👉 **[Open the Dashboard](https://your-app-url.streamlit.app)** *(update this link after deployment)*

> This demo uses representative data. The production version connects live to the KDP Azure SQL database.

## What It Does

- **Interactive bin grid** — every bin in the warehouse plotted by zone and lane, color-coded by ABC classification
- **Real-time search** — search any SKU by name or ID and the map filters instantly
- **Hover tooltips** — click any bin to see SKU name, outbound value, zone, placement quality
- **KPI dashboard** — live metrics for bin utilization, zone breakdown, ABC distribution
- **Warehouse floor plan** — SVG map of the Sumner DC showing all zones and dock doors

## Color Coding

| Color | Meaning |
|-------|---------|
| 🔴 Red | Class A — top 80% outbound value |
| 🟢 Green | Class B — next 15% outbound value |
| 🔵 Cyan | Class C — remaining SKUs |
| ⬛ Dark grey | Empty bin |
| 🟡 Gold | Blocked bin |

## Project Context

This dashboard is part of a year-long MSBA capstone project optimizing warehouse storage at KDP's Sumner Distribution Center. The full solution includes:

- **ABC + Speed Classification** — 281 SKUs ranked by outbound value and movement frequency
- **9-Box Priority Matrix** — cross-classification driving zone assignment
- **Bin Assignment Engine** — priority-ranked greedy algorithm assigning every SKU to its optimal bin
- **Quarterly Re-Slotting Toolkit** — automated SQL pipeline to refresh assignments each quarter
- **Azure SQL Database** — full ETL pipeline from SAP MB51 exports

## Tech Stack

- Python / Streamlit
- Azure SQL Server (Microsoft ODBC Driver 18)
- Tableau (zone heatmap, warehouse map, quarterly toolkit dashboards)
- SQL / T-SQL (Azure Data Studio)

## Team

Suzana Sarkar, Sushmitha Sirigina, Evelyn Vasquez, Yeni Bakinde, Solongo Boldtseren, Bryson Chandler

*University of Washington Tacoma — MSBA Program 2025-2026*
