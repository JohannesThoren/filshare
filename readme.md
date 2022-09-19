# LGJT-Fileshare
a open source files haring website, made to make it easier to set up file sharing/hosting services.


# basic setup
the server is very easy to setup, clone the repo and set some environment variables


### VARIABLES
| variables             | type         | description                                           |
| --------------------- | ------------ | ----------------------------------------------------- |
| DB_PATH               | str/filepath | filepath to the sqlite database file                  |
| FILE_STORAGE_LOCATION | str/filepath | location to the folder where the files will be stored |
| PORT                  | int          | the port the website will be hosted on                |
| HOSTNAME              | str          | the hostname the website will be hosted on            |