# data_platform_lab_1
Data ingestion, manipulation and workflow

# How to run the app
Om man vill se ifall CSV filerna skapas deleta allt i data FÖRUTOM `products_raw.csv`

# Teori

## peka ut ingest —> storage —> transform —> access

____
### Ingest
Där vi tar in data
* Tar in en fil (Json, CSV, XML, Parquet)
* Tar in data från en databas (PostgreSQL, mySQL, DuckDB)
* Tar in bigdata från streaming tex Kafka

____
### Storage
Där vi lagrar data
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
  * Avisar om vi saknade värden som pris eller ID
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
  * "Free" när price == 0
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

____
## Igenkänning av teknologityper Psycopg3, Pandas, pydantic

____
### Psycopg3
**Psycogp3 är ett library som hjälper oss att öppna connection(s) med en PostgreSQL server.**
* Då kan vi använda oss av SQL direkt i koden
* Är en PostgreSQL driver
* Hanterar connections/cursors
* Stödjer transaktioner
* Kan köras async
* Skyddar mot SQL-injections

____
### Pandas
**Pandas är ett library som användas för att skapa DataFrames från att ingesta tex CSV filer**

Pandas används för
* Data manipulation
* Data städning
* Data analys

Varför använder vi Pandas?
* Jobba med tabulär data (rader/kolumner)
* Snabb filtrering
* Gruppering
* Aggregering
* Datatransformation

Pandas DataFrame
* Liknar en tabell i SQL
* Rader och kolumner
* Slicing, filtering, joins

Data cleaning(det vi gör i denna laboration)
* Fixa datumformat(`to_datetime`)
* Konvertera typer(`to_numeric`)
* Trimma whitespace
* Se saknade värden(`isna`)
* Hantera outliers

Import/export
* CSV
* JSON
* Excel(xml)
* SQL-tabeller(vi psycopg)

____
### Pydantic
**Ett library som används för**

Datavalidering säkerställer inkommande data
* har rätt typ
* följer rätt format
* inte saknar obligatoriska fält

Pydantic använder BaseModel-klass där du beskriver din data som python-modell
```python
from pydantic import BaseModel

class Product(BaseModel):
    id: str
    price: float
    name: str
```

Detta göra att vi får Typ-säkerhet eftersom Python bara har "type hinting"
* om vi säger `price: float`
* så blir det konverterat till float
* eller så får vi valideringsfel

____
## Extract —> Transform —> Load (teori)

____
### Extract
Är ni vi Extraherar data från CSV, JSON, API, Parquet, Data lake osv
* Rådata
* Tar in data
* Från olika sources

____
### Transform
Transform är allt vi göra med data innan vi kan använda oss av data
* Städar rå data
* Validerar
* Formar om den
* Standardiserar 
* Aggregerar 
* Delar upp

____
### Load
Load är när vi anser att data är redo att användas, då flyttar vi den till data repository då den är redo för användning
* Efter transformation
* Data warehouse
* Tabeller

### Få ut information från en produkt. (Average mm.. mest sold osv..)
Average price: `df["price"].mean()`  
Median price: `df["price"].median()`  
Highest price: `df.sort_values("price", ascending=False).head(1)`  
Top 10 expensive: `df.nlargest(10, "price")`  
Count products: `len(df)`  
Missing price count: `df["price"].isna().sum()`  
Group count per category (om kategorier fanns): `df.groupby("category").size()`