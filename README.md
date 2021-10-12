# twitter-search

To run the project follow the following steps:

- Download autonomous datawarehouse wallet and extract contents into a folder named wallet in the current directory.
- Connect to database and execute the ddl.sql file.
- Update Constants.py with the Twitter Bearer token, api url and database details.
- Change into the project directory
- Execute the following commands:
    - docker build -t sentiment .
    - docker run sentiment
