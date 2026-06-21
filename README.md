# trekking-management-V2-project
This is the Trekking management system app made with vuejs frontend and flask backend and sqlite database. In which user can book trek for themself and staff will be assigned to them as a guide . and a admin who manage all of treks and staff 
# Virtual Environtment

Run the below commands to create python virtual environment and install all the dependencies

set up virtual environment

```bash
python -m venv venv
```
activate virtual environment

```bash
.\venv\Scripts\activate # Windows
source venv/bin/activate # linux
```
install all the requirements

```bash
pip install -r requirements.txt
```

if you want to add new package then after installing run this to update requirements.txt

```bash
pip freeze > requirements.txt
```

And then run the app both frontend and backend