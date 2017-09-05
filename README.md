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