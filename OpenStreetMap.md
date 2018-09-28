
# Wrangle OpenStreetMap Data

## Map area

Bellevue, WA, United States
* https://www.openstreetmap.org/relation/237868

This is the map of the city I live in. I'm intersted to know what SQL queries would reveal about the database. 

## Problems encountered in the map

* [Problematic formats of postal codes](#postal-codes) (include street name, state, and problematic formats of postal codes, e.g., *"981-2"*, and *"980452"*.)
* [Inconsistent postal codes](#postal-codes) (Most postal codes are 5-digit, with some exceptions of 4-digit extensions following a hyphen.) 
* [Overabbreviated street names](#overabbreviated-and-misspelled-street-names)
* [Street names with "FIXME"](#fixme-street-names)

### Postal Codes

Running the data against *audit_post_code.py*, I get the following results:

```Python
{'980452': 1, '981-2': 1, 'W Lake Sammamish Pkwy NE': 1, 'WA': 2}
```
There are street name, state name, and problematic formats of zip codes in this dataset. First, I need to categorize the data correctly. For the street name and state name, I can change their 'k' values to 'addr:street' and 'addr:state' respectivley so that they won't appear as post codes. 

Then I try to figure out the correct zip codes for *"980452'* and *"981-2"*. Running the SQL query, I can get the latitude and longitude values of the node the *'addr:postcode'* tag is attached to. So here I first run the query with *"980452'*: 

```Sql
SELECT nodes.lat, nodes.lon
FROM nodes
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='980452') i
    ON nodes.id=i.id;
```
```Sql
47.6732445|-122.1196970
```
After searching the latituide and longitude values above in Google map, I get the correct zip code *98052* for *"980452'*. 

I try to change the value to *"981-2"* and run the code. However, I couldn't get anything by searching the nodes id when *'addr:postcode'* equals to *"981-2"*. It turns out that this zip code is under the *"relations"* structure. Considering the fact that the relations table is not included in the database file, I leave the value as it is. 

Below is the function I use to update the post codes:

```Python
mapping = { "980452": "98052"}

def update(postcode, mapping): 
    # update the entry with correct zip code:
    if postcode in mapping:
        postcode = mapping[postcode]
    else:  # update all 9-digit zip codes to 5 digits
        postcode = postcode.split("-")[0]  
    return postcode
```
This should update the incorrect post codes and make all post codes 5 digits. 

### Street Names

There are quite a few street names ending with house/apartment/suite numbers. There's a street name ending with "wa". The whole entry is *"144th pl ne bellevue wa"*. Here, "wa" should refer to the state name and "bellevue" is the city name. I would change this entry to "144 pl ne" when I clean the data. 

#### Overabbreviated and misspelled street names

I've created a *mapping* variable to map out the words that needs correction, e.g., words that are not capilized or misspelled and abbreviated. After having my *mapping* variable, I use the following function to correct them in *update_street_names.py*:

```Python
def update(name, mapping): 
	if name == "144th pl ne bellevue wa":
		name = "144th pl ne"
	words = name.split()
	for w in range(len(words)):
		if words[w].lower() in mapping:
			words[w] = mapping[words[w].lower()]
			if words[w] == "Suite":  # For example, don't update 'Suite E' to 'Suite East'
				break
	name = " ".join(words)
	return name
```
This would update all overabbreviated street names, i.e., *"144th pl ne"* becoming *"144th Place Northeast"*.

#### FIXME street names

In addition, there are 8 street names that have values as "FIXME". According to OpenStreetMap Wiki, it is a *"description of a (possible) error in the map"*. I try to look up the street names using the latitude and longitude values. 

```sql
sqlite> SELECT nodes.id, nodes.lat, nodes.lon
FROM nodes
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='FIXME') i
    ON nodes.id=i.id;
```
Below are the node latitude and longitude values of these *"FIXME"* tags:

```sql
1191705889|47.6170688|-122.0261962
1191705928|47.6171547|-122.0264728
1191705942|47.6171423|-122.0266199
1191705960|47.6170953|-122.0267518
1191705978|47.6170927|-122.0268947
1191705997|47.6171638|-122.0269996
1191706019|47.6172568|-122.0269602
1191706040|47.6172459|-122.0270917
```
Using google map, I've come to the conclusion that these nodes are all on the same street, *"235th Avenue Northeast"*.
So I add *{"FIXME": "235th Avenue Northeast"}* to my *mapping* variable before I start to clean the data.

## Overview of the Data

### File Sizes

```text
map_bellevue_clean.osm ......... 604 MB
map_bellevue.db .......... 335 MB
nodes.csv ............. 221 MB
nodes_tags.csv ........ 18.5 MB
ways.csv .............. 19.4 MB
ways_tags.csv ......... 46.7 MB
ways_nodes.cv ......... 71.5 MB 
```

### Number of nodes

```sql
sqlite> SELECT COUNT(*) FROM nodes;
```
2647742

### Number of ways

```sql
sqlite> SELECT COUNT(*) FROM ways;
```
325940

### Number of unique users

```sql
sqlite> SELECT COUNT(DISTINCT(e.uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;
```
1948

### Top 5 contributing users

```sql
sqlite> SELECT e.user, COUNT(*) as num
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
GROUP BY e.user
ORDER BY num DESC
LIMIT 5;
```

```sql
Glassman|650583
SeattleImport|465770
Glassman_Import|197787
Omnific|118191
sctrojan79|98812
```
### Number of users having 1 post

```sql
sqlite> SELECT COUNT(*)
FROM 
	(SELECT COUNT(*) as num
	FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
	GROUP BY e.user
	HAVING num = 1) u;
```
386

## Additional Data Exploration

### Top 10 appearing amenities

```sql
sqlite> SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='amenity'
GROUP BY value
ORDER BY num DESC
LIMIT 10;
```

```sql
bicycle_parking|2746
restaurant|1540
bench|1418
waste_basket|801
cafe|795
fast_food|445
parking_entrance|317
bar|225
bank|224
post_box|211
```
### Most popular cafes
Not surprisingly, cafe makes to the fifth place on the list. Since Seattle is the place where Starbucks is from, I wonder if there are also many Starbucks in Bellevue.

```sql
sqlite> SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='cafe') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='name'
GROUP BY nodes_tags.value
ORDER BY num DESC
LIMIT 5;
```
```sql
Starbucks|127
Top Pot Doughnuts|12
Caffe Ladro|11
Cherry Street Coffee House|9
Tully's Coffee|9
```
Starbucks is the most popular cafe in Bellevue. It has way 10 times more shops than the other cafes.

### Most popular cuisines

```sql
sqlite> SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='cuisine'
GROUP BY nodes_tags.value
ORDER BY num DESC
LIMIT 5;
```
```sql
pizza|111
mexican|110
thai|86
chinese|85
japanese|67
```
Asian restaurants seem popular in Bellevue. I also want to know if there's any good restaurant in the area. Therefor, I try to query for restaurant with stars.

```sql
sqlite> SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='stars'
GROUP BY nodes_tags.value
ORDER BY num DESC;
```
However, there's nothing returned after this query. *OpenStreetMap Wiki* tellls me that *"stars"* indicates restrant with Michelin star. No wonder the query is in vain. I think the bar for restaurant ranking is too high. I would recommend adding yelp ranking stars instead of Michelin. First of all, yelp has already included most restaurant data. Secondly, it's used by millions of users and it has some authority in restaurant reviews. The problem I would foresee is that yelp ranking is not fixed. You may see a restaurant is ranked at 5 stars today, but it drops to 4 stars tomorrow. This means that if we adopt the yelp ranking, the data probably needs to be constantly updated. So whether we should borrow the yelp ranking or use a customized ranking system remains a question. However, one thing for sure, the Michelin star ranking cannot be the only restaurant ranking. 

### Top 10 appearing tourism
```sql
sqlite> SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='tourism'
GROUP BY value
ORDER BY num DESC
LIMIT 10;
```
```sql
artwork|532
information|214
viewpoint|64
picnic_site|55
hotel|32
map;guidepost|25
attraction|22
museum|15
guest_house|7
gallery|4
```
### Attractions in Bellevue

```sql
sqlite> SELECT nodes_tags.value
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='attraction') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='name'
GROUP BY nodes_tags.value;
```
```sql
Betz Winery
Comedy Underground
Fantastic Erratic
Ferris Wheel
Gum Wall
Historic Carousel
Metropolitan Banquet Hall
Microsoft Visitor Center
Mystery Coke Machine
Public Market Clock
Roll Call
Sanitary Market Building
Seattle Escape Games
Seattle Great Wheel
Segis Pietertje Prospect
Sky View Observatory
Skyway Bowl
Smith Tower Observatory
Spooked in Seattle
Three Brick Monoliths
Underground Tour
Wings over Washington
Xanadu 2.0
```
### Schools in Bellevue

```sql
sqlite> SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='school') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='name'
GROUP BY nodes_tags.value
ORDER BY num DESC
LIMIT 10;
```
```sql
Huntington Learning Center|2
Interagency Ryther Center|2
Kumon|2
The Goddard School|2
4/4 School of Music|1
44 School of Music|1
A+ Alternative School|1
ALPS Language School|1
APP at Lincoln|1
Academy Schools|1
```
While searching all the schools in Bellevue, I've found that there are quite a few learning centers, i.e., *"Kumon"* and *"Huntington Learning Center"*. Since these learning centers provide tutoring services and test prep, I would suggest adding a new category, *"learning_center"* and grouping these institutes under the "learning_center" category, just as *"driving_school"* and *"language_school"*. Thus, when parents are searching schools for their kids in the area, they can exclude these options in their search results. Also, for those who are looking for tutoring services, they can easily locate the services. 

In addition, according to the [tags under *amenity=school*](https://wiki.openstreetmap.org/wiki/Tag:amenity%3Dschool) on *OpenStreetMap Wiki*, there seems no tag to indicate whether the school is private, public or charter, and the school ranking in the area. I think these are all useful information for parents who are researching schools in the area for their kids. While it's easy to decide whether the school is public, private or charter, it's not easy to rank schools, especially from pre-school to middle school. I did a quick search online and I have not found any standard school rankings. The Zillow website of *"[School Reviews for Bellevue](https://www.zillow.com/bellevue-wa/schools/)"* offers an interstring insight. You can see the average test scores of a selected school on Math and Reading and you can compare the scores to average test scores in Bellevue School Distric and the average in Washington state. This is one way to rank and compare schools. I think before we include school ranking in the area to improve the data, we need to either come up with a ranking system or decide on a generally-accepted ranking system. This also involves data analysis and research on the schools in the area.

# Conclusion

I’ve cleaned most parts of the data for this project. However, there are some parts that I didn’t touch. For instance, when I try to see the most popular cafes in Bellevue, I’ve discovered that some cafes have location in their names, e.g., “Zoka Coffee”, “Zoka Coffee - Kirkland”. I know that they are actually the same cafe, but since they have different location attached to the cafe name, SQL query counts them as two different cafes. If my analysis focuses on the cafes in Bellevue, I need to do a close auditing and cleaning on the cafe names.  

