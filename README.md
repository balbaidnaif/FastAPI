# backend-fastapi

## Installing python dependancies

Make sure to use a virtual enviourment, if you don't know what that is follow the following:

```Termnial
python -m venv venv
source venv/bin/activate.bat
```

And the to install python dependancy use the following command:

```
pip install -r requirements.txt
or
python -m pip install -r requirements.txt
```

## Running the server

To run the server use the following command:

```
uvicorn main:app --reload
or
python -m uvicorn main:app --reload
```
