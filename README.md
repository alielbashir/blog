# blog
A social network built with FastAPI, MongoDB, and Vue.js

## Setup
1. Clone the repo
```
git clone https://github.com/alielbashir/blog
cd blog
```

### Backend
2. Install poetry
```
cd backend/app
python3 - m pip install poetry
```
3. Install the dependencies using poetry
```
poetry install
```
4. Run the server with uvicorn
```
uvicorn main:app --host 127.0.0.1 --port 8000
```
