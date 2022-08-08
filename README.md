# blog
A social network built with FastAPI, MongoDB, and Vue.js

## Quickstart
1. Clone the repo
```
git clone https://github.com/alielbashir/blog
cd blog
```

### Backend

Install poetry
```
cd backend
python3 -m pip install poetry
```
Install the dependencies using poetry
```
python3 -m poetry install
```
Run the server with uvicorn
```
python3 -m poetry run uvicorn src.main:app
```

### Frontend

Install npm dependencies

```
cd frontend
yarn install
```

Run the server in development mode
```
yarn dev
```
