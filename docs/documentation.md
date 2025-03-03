# 1. Cleaning of Raw Data  

This project relies on various datasets to analyze municipalities, hospitals, and educational facilities across Spain. The raw data can be found in `"../data/raw"`.

The raw files have been processed, cleaned and standarized, and stored in `"../data/processed/filtered_files"` with the prefix `"filtered_"`


Below are the main data sources and the cleaned (filtered) outcomes:

| Notebook                  | Raw Files (source)                | Processed                         |
|---------------------------|-----------------------------------|-----------------------------------|
|  **Main Info:** </br> `eda_municipalities_coordinates.ipynb`  |  [INE (Instituto Nacional de Estadística)](https://ine.es/dynt3/inebase/es/index.htm?padre=525) </br>  [Business Intelligence](https://www.businessintelligence.info/varios/longitud-latitud-pueblos-espana.html) | `filtered_municipalities.csv`      |
|  **Demographics:** </br> `eda_demographics.ipynb`  |  [INE (Instituto Nacional de Estadística)](https://ine.es/jaxi/Tabla.htm?path=/t20/e244/avance/p02/l0/&file=1mun00.px&L=0)   | `filtered_demographics.csv`    |
|  **Transport:** </br> `eda_transport.ipynb`  |  [Spanish Airports (ArcGIS Hub)](https://hub.arcgis.com/datasets/7232e84f53494f5e9b131b81f92534b8_0/explore) </br>  [Trains - AVE, Long Distance, Medium Distance (Renfe)](https://data.renfe.com/dataset/listado-estaciones-de-alta-velocidad-larga-distancia-y-media-distancia)  </br> [Trains - All regional stations (Renfe)](https://data.renfe.com/dataset/estaciones-listado-completo/resource/783e0626-6fa8-4ac7-a880-fa53144654ff)   | `filtered_airports.csv`, `filtered_trains.csv`, `filtered_regional_trains.csv`        |
|  **Climate:** </br> `eda_climate.ipynb`  |  [Köppen Climate Classification](https://koeppen-geiger.vu-wien.ac.at/) | `filtered_climate.csv`        |
|  **Connectivity:**</br> `eda_connectivity.ipynb`  |   [ADSL Zones](https://avancedigital.maps.arcgis.com/apps/webappviewer/index.html?id=0ac10917cf3d47fc91b6113ea92c9506)    |  `filtered_connectivity.csv`      |
|  **Industry:**</br> `eda_industry.ipynb`  |   [INE (Instituto Nacional de Estadística)](https://ine.es/dyngs/INEbase/es/categoria.htm?c=Estadistica_P&cid=1254735576715) | `filtered_industry.csv`     |
|  **Health:**</br> `eda_hospitals.ipynb`  |   [Spanish Hospitals (ArcGIS Hub)](https://hub.arcgis.com/datasets/ComunidadSIG::hospitales-de-espa%C3%B1a/explore?location=34.913972%2C-6.829606%2C5.58)   | `filtered_hospitals.csv`        |
|  **Education:** </br> `eda_schools.ipynb`  |  [Spanish Schools (ArcGIS Hub)](https://hub.arcgis.com/datasets/1632db0c4f0848099f545e33b19c024d_0/explore)   | `filtered_schools.csv`  |

</br>

</br>

# 2. Aggregation

## 2.1. Distances (Airports, Trains, Schools and Hospitals)

| Notebook                  | Comments                | Processed                         |
|---------------------------|-----------------------------------|-----------------------------------|
|  `CAREFUL_accessibility_eda.ipynb`  | This document calculates the distance from each town to the nearest hospital and the nearest school. The results will be used in subsequent analyses. </br> **Important Note:** Running this calculation is time-consuming, so execute it with caution. |  `filtered_distances.csv`      |


 
</br>

## 2.2. Aggregation of data

Al the processed data sets can be found in `"../noteboks/no_process/all_datasets.ipynb"`. 

| Notebook                  | Comments| |
|---------------------------|-----------------------------------|----------------------|
| `aggregation.ipynb`  | All files contained in the `filtered_files` folder are added to the aggregation notebook for merging on "cmun". Out of this notebook we get a dataframe that includes all available clean data form our raw sources, without any feature engineering.  | The file can be found with the rest of processed data as `../data/processed/aggregated_pueblos.csv`|


# 3. Feature Engineering

We have left out the islands for the MVP, as distance calculation was not accurate enough. 


## 3.1. Population

After calculating the outliers of the total population, we have left out all cities over 6000 habitants. (Cities bigger than 20000 habitants that can be found in file `../data/processed/split_cities.csv`, as they can be used as a feature for pueblos)

 `town_size`:
 
 *  **Big** (>3000), 
 *  **Medium** (between 500 and 3000), 
 *  **Small** (between 100 and 300), 
 *  **Very Small** (less than 100) 
 

## 3.2. Connectivity

 `connectivity_score`:

| **Factor**            | **New Weight (%)** | **Reasoning** |
|-----------------------|-------------------|--------------|
| *ftth*               | **50%**            | Fiber is the most important for stable, high-speed connectivity. |
| *reception_100mbps*  | **35%**            | Ensures fast broadband availability, even if not fiber. |
| *4g*                | **15%**            | Still essential for mobile broadband, but not the primary factor. |

</br>

 `connectivity_category`:
| **Score Range**  | **Category**          | **Description** |
|------------------|----------------------|----------------|
| **80 - 100**     | **Excellent**         | Strong fiber coverage and high-speed internet. |
| **60 - 79**      | **Good**              | Decent broadband with fiber or high-speed non-fiber options. |
| **40 - 59**      | **Moderate**          | Some high-speed coverage, but fiber may be limited. |
| **20 - 39**      | **Weak**              | Basic connectivity with limited high-speed access. |
| **0 - 19**       | **Poor**              | Very poor or no access to high-speed internet. |



## 3.3. Industry

 `economy_score`:

| **Factor**                      | **New Weight (%)** | **Reasoning** |
|--------------------------------|-------------------|------------------|
| *n_industry*               | **25%**            | The industrial sector is a major driver of economic output, employment, and local business ecosystems, especially in manufacturing-heavy towns. |
| *n_construction*             | **10%**            | Construction supports economic growth by enabling infrastructure development, but it is more cyclical and often depends on external investments. |
| *n_info_communications*      | **10%**            | The tech and communications sector is growing in importance, driving innovation, high-income jobs, and business services. |
| *n_financial_insurance*      | **10%**            | Financial services provide stability, capital, and investment to other sectors, but their direct impact on local economies varies. |
| *n_real_estate*              | **10%**            | The real estate sector reflects economic health through property development, market demand, and wealth accumulation. |
| *n_professional_technical*   | **15%**            | This sector includes consulting, R&D, and high-skilled jobs, contributing significantly to knowledge-based economies. |
| *n_education_health_social*  | **15%**            | Essential for workforce development, healthcare access, and social stability, making it a critical economic pillar. |
| *n_other*                   | **5%**            | A mix of various industries with a less direct but still relevant economic impact. |


 `economy_score_area`:

We calculate the towns in the vicinity (within a 40km raidus) and calculate the average economy_score of all towns in vicinity. 


</br>

## Naming Standards

Throughout the project, we adhere to the following Spanish naming conventions for the administrative divisions of municipalities, provinces, and autonomous communities. The names used follow the official and standardized format, ensuring clarity and consistency across all references.

**Municipality Names**: We use the full official name of each municipality, as recognized by local and national government institutions.
In cases where names appear with an inverted order (such as "Rozas, Las" or "Espang, L'"), we reorder them to the standard Spanish format. For example, 
- "Rozas, Las" is renamed to "Las Rozas"
- "Espang, L'" is corrected to "L'Espang"
- "Escorial, (El)" is corrected to "El Escorial"

**Province Names**: The names of the provinces are listed in their official Spanish form. Each autonomous community in Spain is made up of several provinces, and these are identified in the corresponding sections of the project.

**Autonomous Community Names**: We follow the official names of each of Spain's autonomous communities, ensuring the accurate representation of each region, as recognized in the Spanish Constitution and administrative documentation.

By using these standardized names, we ensure that the project maintains geographic accuracy and aligns with official naming conventions used across Spain.

| Community                           | Province                                                        |
|-------------------------------------|-----------------------------------------------------------------|
| Andalucía                           | Almería, Cádiz, Córdoba, Granada, Huelva, Jaén, Málaga, Sevilla |
| Aragón                              | Huesca, Teruel, Zaragoza                                        |
| Asturias                            | Asturias                                                        |
| Islas Baleares                      | Islas Baleares           |
| País Vasco                          | Álava, Gipuzkoa, Bizkaia                                        |
| Canarias                            | Las Palmas, Santa Cruz de Tenerife                              |
| Cantabria                           | Cantabria                                                 |
| Castilla-La Mancha                  | Albacete, Ciudad Real, Cuenca, Guadalajara, Toledo        |
| Castilla y León                     | Ávila, Burgos, León, Palencia, Salamanca, Segovia, Soria, Valladolid, Zamora |
| Cataluña                            | Barcelona, Girona, Lleida, Tarragona                      |
| Extremadura                         | Badajoz, Cáceres                                          |
| Galicia                             | A Coruña, Lugo, Ourense, Pontevedra                       |
| Madrid                              | Madrid                                                    |
| Murcia                              | Murcia                                                    |
| Navarra                             | Navarra                                                   |
| La Rioja                            | La Rioja                                                  |
| Comunidad Valenciana                | Alicante, Castellón, Valencia   



## Scoring  

This project relies on various datasets to analyze municipalities, hospitals, and educational facilities across Spain. Below are the main data sources used:

| Category                  | Source                            |
|---------------------------|-----------------------------------|
| Demographic Data             | [INE (Instituto Nacional de Estadística)](https://ine.es/dynt3/inebase/es/index.htm?padre=525) |
| Geographical Coordinates   | [Business Intelligence](https://www.businessintelligence.info/varios/longitud-latitud-pueblos-espana.html) |          |
| Healthcare Facilities      | Hospitals in Spain: [ArcGIS Hub](https://hub.arcgis.com/datasets/ComunidadSIG::hospitales-de-espa%C3%B1a/explore?location=34.913972%2C-6.829606%2C5.58)   |
| Educational Facilities     | Schools in Spain: [ArcGIS Hub](https://hub.arcgis.com/datasets/1632db0c4f0848099f545e33b19c024d_0/explore)     |
| Climate Information        | -                                 |
| Housing Prices             | Rent                                 |
| Transport                  | Airports in Spain                                 |



