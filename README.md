# Overview of Wrangle OpenStreetMap Data Project
By Vicky Fang<br>
### Contents:
* **OpenStreetMap.md:** A report that documents the data wrangling process
* **audit_post_code.py:** Python code to audit post codes in the dataset
* **update_post_codes.py:** Python code to improve post codes and save the data in *"map_bellevue_clean.osm"*
* **audit_street_names.py:** Python code to audit street names in the dataset
* **update_street_names.py:** Python code to imporve street names in the dataset and save the data in *"map_bellevue_clean.osm"*
* **prepare_for_db.py:** Python code to prepare the data to be inserted  into a SQL database. Parse the elements in the OSM XML file, transforming them from document format to tabular format, thus making it possible to write to .csv files.
* **import_csv_to_db.py:** Python code to import csv files and insert them to a SQL database.
* **import_csv_to_db.py:** Python code to import csv files and insert them to a SQL database.
* **import_csv_to_db.py:** Python code to import csv files and insert them to a SQL database.
* **schema.py:** Shema for the csv files and the eventual tables.

### Reference:
* [11.13. sqlite3 — DB-API 2.0 interface for SQLite databases](https://docs.python.org/2/library/sqlite3.html)

* [OpenStreetMap Map Features](https://wiki.openstreetmap.org/wiki/Map_Features)

* [19.7. xml.etree.ElementTree — The ElementTree XML API](https://docs.python.org/2/library/xml.etree.elementtree.html)

* [Writing a csv file into SQL Server database using python](https://stackoverflow.com/questions/21257899/writing-a-csv-file-into-sql-server-database-using-python)
