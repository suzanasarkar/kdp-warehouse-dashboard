KDP Warehouse Re-Slotting Dashboard
MSBA Capstone Project for Keurig Dr Pepper Distribution Center in Sumner, Washington, University of Washington
An interactive warehouse slotting dashboard built for the KDP Sumner Distribution Center (224,000 sq ft, 5,617 bins, 281 active FG SKUs).


⚠️ DEMO VERSION - REPRESENTATIVE DATA ONLY
All bin locations, SKU names, outbound values, ABC classifications, and warehouse metrics shown in this application are randomly generated and have absolutely no correlation to real KDP warehouse data, real SKU inventory, or actual Keurig Dr Pepper operations.
This is a portfolio demonstration of the analytical framework and interactive dashboard built as part of the MSBA Capstone Project at the University of Washington Tacoma. The production version of this application connects to a secure Azure SQL database with real operational data that is not publicly accessible.


Live Demo
[Open the Dashboard](https://kdp-warehouse-dashboard.streamlit.app/)

What It Does

Interactive bin grid - every bin in the warehouse plotted by zone and lane, color-coded by ABC classification
Real-time search - search any SKU by name or ID and the map filters instantly
Hover tooltips - hover over any bin to see SKU name, outbound value, zone, placement quality
KPI dashboard - live metrics for bin utilization, zone breakdown, ABC distribution
Warehouse floor plan - SVG map of the Sumner DC showing all zones and dock doors


Color Coding
Red: Class A - top 80% outbound value Green: Class B - next 15% outbound value Cyan: Class C - remaining SKUs Dark grey: Empty bin Gold: Blocked bin

Project Context
This dashboard is part of a year-long MSBA capstone project optimizing warehouse storage at KDP's Sumner Distribution Center. The full solution includes:

ABC + Speed Classification - 281 SKUs ranked by outbound value and movement frequency
9-Box Priority Matrix - cross-classification driving zone assignment
Bin Assignment Engine - priority-ranked greedy algorithm assigning every SKU to its optimal bin
Quarterly Re-Slotting Toolkit - automated SQL pipeline to refresh assignments each quarter
Azure SQL Database - full ETL pipeline from SAP MB51 exports


Tech Stack
LayerToolApplicationPython / StreamlitDatabaseAzure SQL Server (Microsoft ODBC Driver 18)VisualizationTableau (zone heatmap, warehouse map, quarterly toolkit dashboards)LanguageSQL / T-SQL (Azure Data Studio)

Team Members:
Suzana Sarkar, Sushmitha Sirigina, Evelyn Vasquez, Yeni Bakinde, Solongo Boldtseren, Bryson Chandler
University of Washington Tacoma - MSBA Program 2025-2026
