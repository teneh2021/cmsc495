# cmsc495
# Weight tracking application projectfiles

# Setting up the environment
# NOTE: Program only supports Python3


Clone the git repo main branch
```
git clone https://github.com/criggins1/cmsc495.git
```

cd into the directory of the repo after cloning
```
cd cmsc495
```

Create your python virtual environment (Note "env" is just the name of the virutal environment and can be anything you want it to be)
```
python -m venv env
```

Start the virutal envrionment. (If you name it something else. replace the "env" with the name of your virutal environment)

Windows:
```
env\Scripts\activate
```
OSX:
```
source env/bin/activate
```

Install the requirments into your virtual environment
```
python -m pip install -r requirements.txt
```
Your environment is now set up. The next steps will start the project.
--------------------------------------------
Move into the WeightTracker Directory
```
cd WeightTrackers
```
Start the server
```
python manage.py runserver
```
Open a browser and go to the development server (usually is 127.0.0.1:8000)
