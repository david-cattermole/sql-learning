# SQL Learning
Tools and libraries related to SQL database management systems. 

This project can be considered a constant work in progress, it is used for experimentation and testing with no functional goal in sight; only the goal of learning.

## Sub-Projects

Below are a list of sub-projects within this project. 

### MediaDB
Parses a file system, collects files and stores information.

Uses MySQL (or MariaDB) database, with MySQLdb python module bindings for MySQL support.

Goals:
- Operating System independent file path structure.
- Basic keyword / tag searching.
- Many-to-Many relationship example (using Foreign Keys)

#### Create Database

Create the database tables

```bash
# Usage: 
#  mediaDB_create.py  # no arguments needed
python mediaDB_create.py
```

#### Find Media

Searches the file system for media to add into the database.

```bash
# Usage:
#  mediaDB_find.py # no arguments needed
python mediaDB_find.py
```

#### Print Common Tags

Print tags, ordered by frequency, with a maximum number.

```bash
# Usage: 
#  mediaDB_countTags.py [max num of tags]
python mediaDB_countTags.py 10
```

#### Search

List all file paths that contain the given tags and has the given type.
The given tags must all exist against the path for the path to be returned.

Common types are:
- application
- image
- video
- audio

```bash
# Usage: 
#  mediaDB_findPathsFromTag.py [media type] [tag] [tag] [tag] ...
python mediaDB_findPathsFromTag.py image sky sunset
```

### MediaDB2

#### Create

Create (and reset?) the database.

```bash
# 
#
# Usage:
#  mediaDB2_test.py [reset table]
python mediaDB2_test.py 1
```

#### Print Common Tags

Print tags, ordered by frequency, with a maximum number.

```bash
# Usage:
#  mediaDB2_countTags.py [max num of tags]
python mediaDB2_countTags.py 10
```

#### Search

List all file paths that contain the given tags and has the given type.
The given tags must all exist against the path for the path to be returned.

Common types are:
- application
- image
- video
- audio

```bash
# Usage: 
#  mediaDB2_findPathsFromTag.py [media type] [tag] [tag] [tag] ...
python mediaDB2_findPathsFromTag.py image sky sunset
```

### AssetDB

An example design and structure of a Visual Effects Asset database.

Uses SQL Alchemy for Object Relation Mapping (ORM), and interact with the database with Python class objects. Supports either Postgres or MySQL database engines.

Goals:
- Well designed; normalised database structure.
- Store the least amount of (duplicate) data required. 
- Create a file-structure from database mappings.
- Operating system and studio independent.
- Allow version resolving, using various methods such as, 'approved', 'frozen', and 'latest'.
- Move away from file paths defining assets, use IDs to resolve tags into file paths. 
- Define examples of data needed for an asset system.

Please see file ./assetDB/design/assetDB.jpg for an example of the intended design. 'assetDB.graphml' can be opened and edited with [yEd](https://www.yworks.com/products/yed).

#### Create and Add Test Data

Create, reset and fill the database with semi-random data.

```bash
# Usage:
#  assetDB_test.py [reset table]
python assetDB_test.py 1
```

### AssetDB2

#### Create and Add Test Data

Create, reset and fill the database with semi-random data.

```bash
# Usage:
#  assetDB2_test.py [reset table] 
python assetDB2_test.py 1
```
