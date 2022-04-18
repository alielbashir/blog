# blog
A social network built with FastAPI, MongoDB, and Vue.js

## Quickstart
1. Clone the repo
```
git clone https://github.com/alielbashir/blog
```

### Backend

2. Install poetry
```
cd backend
python3 -m pip install poetry
```
3. Install the dependencies using poetry and activate the venv
```
poetry install
poetry shell
```
4. Run the server with uvicorn
```
uvicorn src.main:app
```
