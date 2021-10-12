# twitter-search

To run the project follow the following steps:

* Download autonomous datawarehouse wallet and extract contents into the folder named wallet.
* Connect to database and execute the ddl.sql file.
* Update Constants.py with the Twitter Bearer token, api url and database details.
* change into the project directory
* execute the following commands:
    docker build -t sentiment .
    docker run sentiment