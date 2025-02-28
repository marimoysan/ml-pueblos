## Data Sources  

This project relies on various datasets to analyze municipalities, hospitals, and educational facilities across Spain. The raw data can be found in "../data/raw".

The raw files have been processed, cleaned and standarized, and stored in "../data/processed" with the prefix "filtered_"


Below are the main data sources used:

| Notebook                  | Raw Files (source)                | Processed                         |
|---------------------------|-----------------------------------|-----------------------------------|
|  Transport: eda_transport.ipynb  |  Airports Coordinates [ArgisHUB]; Airports Traffic (WIKI); Trains (Ministry of transport)   | filtered_airports.csv, filtered_trains.csv        |
|  Transport: eda_transport.ipynb  |  Airports Coordinates [ArgisHUB]; Airports Traffic (WIKI); Trains (Ministry of transport)   | filtered_airports.csv, filtered_trains.csv        |
|  Transport: eda_transport.ipynb  |  Airports Coordinates [ArgisHUB]; Airports Traffic (WIKI); Trains (Ministry of transport)   | filtered_airports.csv, filtered_trains.csv        |
|  Transport: eda_transport.ipynb  |  Airports Coordinates [ArgisHUB]; Airports Traffic (WIKI); Trains (Ministry of transport)   | filtered_airports.csv, filtered_trains.csv        |
|  Transport: eda_transport.ipynb  |  Airports Coordinates [ArgisHUB]; Airports Traffic (WIKI); Trains (Ministry of transport)   | filtered_airports.csv, filtered_trains.csv        |








| Raw file                  | Source                            | Notebook                            |Processed                            |
|---------------------------|-----------------------------------|-----------------------------------|-----------------------------------|
| 68542.csv        | age | |filtered_airports.csv |
| connectivity_municipality.csv  | connectivity |          |filtered_airports.csv |
| coordinates_towns_spain.csv | [Business Intelligence](https://www.businessintelligence.info/varios/longitud-latitud-pueblos-espana.html)    |
| hospitals_spain.csv | [ArcGIS Hub](https://hub.arcgis.com/datasets/ComunidadSIG::hospitales-de-espa%C3%B1a/explore?location=34.913972%2C-6.829606%2C5.58)   |
| industry.csv | industry                                 |  |filtered_airports.csv |
| listado_completo_av_ld_md.csv| trains                                 |
| population_towns.csv |[INE (Instituto Nacional de Estadística)](https://ine.es/dynt3/inebase/es/index.htm?padre=525) |                            | | |filtered_airports.csv |
| pueblos_agoedores_rating.csv | pueblos acogedores                               |
| rent_municipality.csv | rent                               |
| spain_municipalities_climate_final.csv | climate                             | filtered_airports.csv |
| spanish_airports.geojson | schools                                 | filtered_airports.csv |
| spanish_schools.geojson | [ArcGIS Hub](https://hub.arcgis.com/datasets/1632db0c4f0848099f545e33b19c024d_0/explore)                                 | filtered_airports.csv |

## Data & Features  

This project relies on various datasets to analyze municipalities, hospitals, and educational facilities across Spain. Below are the main data sources used:

| Category                  | Source                            |
|---------------------------|-----------------------------------|
| Demographic Data             | [INE (Instituto Nacional de Estadística)](https://ine.es/dynt3/inebase/es/index.htm?padre=525) |
| Geographical Coordinates   | [Business Intelligence](https://www.businessintelligence.info/varios/longitud-latitud-pueblos-espana.html) |          |
| Healthcare Facilities      | Hospitals in Spain: [ArcGIS Hub](https://hub.arcgis.com/datasets/ComunidadSIG::hospitales-de-espa%C3%B1a/explore?location=34.913972%2C-6.829606%2C5.58)   |
| Educational Facilities     | Schools in Spain: [ArcGIS Hub](https://hub.arcgis.com/datasets/1632db0c4f0848099f545e33b19c024d_0/explore)     |
| Climate Information        | -                                 |
| Housing Prices             | Rent                                 |
| Transport                  | Airports in Spain         

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



