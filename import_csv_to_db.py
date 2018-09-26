import sqlite3
import csv

conn = sqlite3.connect('map_bellevue.db')
conn.text_factory = str
c = conn.cursor()

def create_tables():
    c.execute('CREATE TABLE IF NOT EXISTS nodes(id INTEGER PRIMARY KEY NOT NULL, lat REAL, lon REAL, user TEXT, uid INTEGER, version INTEGER, changeset INTEGER, timestamp TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS nodes_tags(id INTEGER, key TEXT, value TEXT, type TEXT, FOREIGN KEY (id) REFERENCES nodes(id))')
    c.execute('CREATE TABLE IF NOT EXISTS ways(id INTEGER PRIMARY KEY NOT NULL, user TEXT, uid INTEGER, version TEXT, changeset INTEGER, timestamp TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS ways_tags(id INTEGER NOT NULL, key TEXT NOT NULL, value TEXT NOT NULL, type TEXT, FOREIGN KEY (id) REFERENCES ways(id))')
    c.execute('CREATE TABLE IF NOT EXISTS ways_nodes(id INTEGER NOT NULL,node_id INTEGER NOT NULL, position INTEGER NOT NULL, FOREIGN KEY (id) REFERENCES ways(id), FOREIGN KEY (node_id) REFERENCES nodes(id))')
    
create_tables()

# insert nodes.csv to nodes table
def insert_nodes():
    
    # read in the data - read in the csv file as a dictionary,
    # format the data as a list of tuples:
    
    with open('nodes.csv','r') as csvfile:
        # csv.DictReader uses first line in file for column headings by default
        reader = csv.DictReader(csvfile) # comma is default delimiter
        
        to_db = [(r['id'], r['lat'],r['lon'], r['user'], r['uid'], r['version'], r['changeset'], r['timestamp']) for r in reader]
    
    # insert the data
    c.executemany('INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);', to_db)
    # commit the changes
    conn.commit()

# insert nodes_tags.cv to nodes_tags table
def insert_nodes_tags():
    
    # read in the data - read in the csv file as a dictionary,
    # format the data as a list of tuples:
    
    with open('nodes_tags.csv','r') as csvfile:
        # csv.DictReader uses first line in file for column headings by default
        reader = csv.DictReader(csvfile) # comma is default delimiter
        
        to_db = [(r['id'], r['key'],r['value'], r['type']) for r in reader]
    
    # insert the data
    c.executemany('INSERT INTO nodes_tags(id, key, value,type) VALUES (?, ?, ?, ?);', to_db)
    # commit the changes
    conn.commit()

# insert ways.csv to ways table
def insert_ways():
    
    # read in the data - read in the csv file as a dictionary,
    # format the data as a list of tuples:
    
    with open('ways.csv','r') as csvfile:
        # csv.DictReader uses first line in file for column headings by default
        reader = csv.DictReader(csvfile) # comma is default delimiter
        
        to_db = [(r['id'], r['user'], r['uid'], r['version'], r['changeset'], r['timestamp']) for r in reader]
    
    # insert the data
    c.executemany('INSERT INTO ways(id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);', to_db)
    # commit the changes
    conn.commit()
    
# insert ways_tags.csv to ways_tags table
def insert_ways_tags():
    
    # read in the data - read in the csv file as a dictionary,
    # format the data as a list of tuples:
    
    with open('ways_tags.csv','r') as csvfile:
        # csv.DictReader uses first line in file for column headings by default
        reader = csv.DictReader(csvfile) # comma is default delimiter
        
        to_db = [(r['id'], r['key'],r['value'], r['type']) for r in reader]
    
    # insert the data
    c.executemany('INSERT INTO ways_tags(id, key, value,type) VALUES (?, ?, ?, ?);', to_db)
    # commit the changes
    conn.commit()

# insert ways_nodes.csv to ways_nodes table
def insert_ways_nodes():
    
    # read in the data - read in the csv file as a dictionary,
    # format the data as a list of tuples:
    
    with open('ways_nodes.csv','r') as csvfile:
        # csv.DictReader uses first line in file for column headings by default
        reader = csv.DictReader(csvfile) # comma is default delimiter
        
        to_db = [(r['id'], r['node_id'],r['position']) for r in reader]
    
    # insert the data
    c.executemany('INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?);', to_db)
    # commit the changes
    conn.commit()

# execute all functions to insert data to sql tables
insert_nodes()
insert_nodes_tags()
insert_ways()
insert_ways_nodes()
insert_ways_tags()

conn.close()