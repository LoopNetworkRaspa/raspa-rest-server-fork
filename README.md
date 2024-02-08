## Installation

Use the package manager [pipenv](https://pypi.org/project/pipenv/) to install packages.

```bash
pipenv install --deploy
```

## Set up the environment
Create an `.env` file and add these environment variables:
```
SQL_URI="postgresql://[user[:password]@][netloc][:port][/dbname]"
NODE_RPC_URI="[netloc][:port]"
ADDRESS_TYPE="raspadev"
NETWORK_NAME="raspa-devnet"
REGEX="^raspadev\:[a-z0-9]{61,63}$"
DROP_SQL_DB="false"
```
>**Note:** If you need to drop the database at application startup, set `true` for `DROP_SQL_DB`

## Run

```bash
pipenv run start
```
or
```bash
pipenv run gunicorn -b 0.0.0.0:8080 -w 1 -k uvicorn.workers.UvicornWorker main:app --timeout 120
```