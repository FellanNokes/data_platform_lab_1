# data_platform_lab_1
Data ingestion, manipulation and workflow

# Teori

## peka ut ingest —> storage —> transform —> access

____
### Ingest
Där vi tar in datan
* Tar in en fil (Json, CSV, XML, Parquet)
* Tar in data från en databas (PostgreSQL, mySQL, DuckDB)
* Tar in bigdata från streaming tex Kafka

____
### Storage
Där vi lagrar datan
* Data lake lagrar rådata oftast i molntjänster tex Azure eller Google Cloud Storage
* Data Warehouse lagrar strukturerad och optimerad data tex Snowflake, PostgreSQL eller DuckDB
* Databaser för applikationer PostgreSQL och MySQL med fokus inom Transaktioner med snabba inserts och updates

____
### Transform
Där vi tar hand om rå data som vi ska behandla för att göra redo för analys

I den här labben transformerar vi:
* Konverterar price till numeric
* fixar datumformat
* skapar reject/review
* räknar ut snittpris


 * **Cleaning**
   * Tar bort whitespace
   * Konverterar typer (string -> float)
   * Hanterar saknade värden
   * Standardiserar format (2025/02/03 -> 2025-02-03)
 

* **Validering**
  * Flagga extrema priser
  * Rejectar saknade värden som pris eller ID
  * Identifiera outliers
  

* **Strukturering**
  * Byta kolumnnamn
  * Skapa ny kolumner
  * Dela upp eller slå ihop fält


* **Aggregation**
  * Räkna ut snitt
  * Median
  * Gruppindelning
  * Summering


* **Business logic**
  * "Luxury product" om price > 30000
  * "Free" om price == 0
  * Skapa status-kolumner


* **Transform i olika verktyg**
  * Pandas
  * SQL
  * dbt
  * Python
  * Warehouse queries

____
### Access
Access handlar om
* Läsbarhet
* Prestanda
* Tillgänglighet
* Säkerhet (vem får tillgång till vad)


* Exempel
  * Dashboards (Power BI, Tableau)
  * CSV-export (Som i den här labben)
  * En API som returnerar data
  * En rapport

## Igenkänning av teknologityper Psycopg3, Pandas, pydantic

### Psycopg3