# Django Scheduler App

### System requirements:
- Python 3.7

### Local setup:

Clone  
```bash
git clone https://github.com/AmalVijayan/Scheduler.git
```

Create virtualenv
```bash
cd Scheduler
python3 -m venv ve #or virtualenv ve
source ve/bin/activate #or ve\Scripts\acivate for windows
```

Install dependencies
```bash
pip install -r requirements.txt
```

Run existing migrations (creates a local sqlite3 DB file with tables)  
```bash
python manage.py migrate
```

Run Unit-tests:
```bash
python manage.py test scheduler_api

or 

python manage.py test
```

Load sample data:
```bash
python manage.py loaddata sample_data.json
```


Run server  
```bash
python manage.py runserver
```

Django automatic admin    
- [http://localhost:8000/admin/]()  
- username: admin
- password: admin123

### Postman API Collections:  
Download and import into postman:  
  [SchedulerApp.postman_collection.json](https://drive.google.com/file/d/14pSLTEhGQ2AsBgtAG_sXnqf8o3uRDU4W/view?usp=sharing)
  
## API TESTS

### 1. LIST ALL USERS
![](https://github.com/AmalVijayan/Scheduler/blob/master/artifacts/scheduler_1.png)

### 2. CREATE A SCHEDULE
![](https://github.com/AmalVijayan/Scheduler/blob/master/artifacts/scheduler_2.png)

### 3. CREATE A SCHEDULE (CONFLICT)
![](https://github.com/AmalVijayan/Scheduler/blob/master/artifacts/scheduler_3.png)
