# Welcome to OnTrack

If you are installing this for the first time do the following  
virtualenv OnTrackSolution  
cd OnTrackSolution\Scripts  
activate 

Now go to the folder and run the following

pip install django  
REM pip install mysqlclient (1.4.4)  
cd..  
django-admin startproject OnTrackProject  

git init  
git remote add origin https://github.com/Skywalker-912/CompSciProject.git  
git fetch origin  
git checkout -b master --track origin/master   
git reset origin/master   

