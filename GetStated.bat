@echo off

python -m venv v_cic


.\v_cic\scripts\python -m pip install --upgrade pip

.\v_cic\scripts\python -m pip install pandas

.\v_cic\scripts\python -m pip install openpyxl

.\v_cic\scripts\python -m pip install django

.\v_cic\scripts\python -m pip install xmltodict

.\v_cic\scripts\python -m pip install thefuzz

.\v_cic\scripts\python -m pip install fiscalyear

.\v_cic\scripts\python .\cityinvitecalc\manage.py makemigrations

.\v_cic\scripts\python .\cityinvitecalc\manage.py migrate 

.\v_cic\scripts\python .\cityinvitecalc\manage.py createsuperuser

.\v_cic\scripts\python .\scripts\InsertStaticData.py


echo "Done Creating, insert data into the Data Folder"
echo "Continue with CreateLeaderboard"
PAUSE
