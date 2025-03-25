# Pueblos: Promoting Rural Repopulation in Spain

## Project Overview
Pueblos is a Data Science and AI project aimed at promoting repopulation and sustainable living in Spain. The project involves an in-depth data analysis of all towns across the country and the development of a smart recommendation engine that helps users discover the best rural towns to relocate based on their preferences and needs.

## Challenge Overview
Spain is experiencing depopulation in many rural towns, with younger generations migrating to urban centers. Our goal is to:
- Aggregate relevant data on **all small towns and villages** in Spain.
- Showcase that modern living is possible in rural areas.
- Develop a recommendation system that suggests optimal locations for relocation.

## Scope & Constraints
- Towns with **fewer than 6,000 inhabitants** are considered.
- Focus is on **mainland Spain** (islands are not included yet).
- The project currently uses a limited number of features, but the structure allows for **scalability**.

## Data Sources
The dataset aggregates multiple sources, including:
- **Instituto Nacional de Estadística (INE)**
- **Business Intelligence databases**
- **Spanish Airports & Train Stations (ArcGIS Hub, Renfe)**
- **Köppen Climate Classification**
- **ADSL Connectivity Zones**
- **Hospitals & Schools (ArcGIS Hub)**

## Project Structure

```
ML-PUEBLOS/
├── data/               # Raw and processed datasets
├── docs/               # Project documentation
├── frontend/           # User-facing components
│   ├── back_office/    # Tool to iterate and fine-tune clustering
│   ├── front_desk/     # User-facing recommendation tool
├── models/             # Trained ML models and pipelines
├── notebooks/          # Jupyter Notebooks with analysis and model development
├── references/         # External references and research materials
├── reports/            # Analysis and project reports
├── resources/          # Additional resources
├── scripts/            # Utility scripts for data processing & model training
├── .gitignore          # Git ignore file
├── .python-version     # Python version specification
├── LICENSE             # License file
├── README.md           # Project documentation
└── requirements.txt    # Dependencies for the project
```


## Methodology
1. **Data Processing**: Cleaning and structuring the dataset.
2. **Clustering**: Using unsupervised ML techniques to group towns based on relevant factors.
3. **Recommendation System**: Matching users with towns based on their preferences using a similarity graph.
4. **User Interface**: Building an interactive tool for users to explore town recommendations.

## Setup & Installation
Ensure you have Python installed. Then, set up the virtual environment and install dependencies.

### macOS/Linux
```sh
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

## Next Steps
- Analyze recommendation **performance and quality**.
- Tune the **recommendation algorithm**.
- Enhance the **web UI**.
- Introduce a **feedback loop** for user ratings to improve recommendations.

## License
This project is for educational and research purposes as part of a Data Science, Machine Learning, and AI initiative.

## Authors
**Marina Moya & Kay Gensmann**  
**Date:** March 2025
