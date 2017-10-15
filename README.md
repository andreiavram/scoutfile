scoutfile
=========

Software de manangement a unui grup de cercetași, dezvoltat pentru Centrul Local Axente Sever Alba Iulia din ONCR


development
===========

To get started with development, you need to do three things:


1. link your own local settings (`ln -s local_settings.local.py local_settings.py`)
2. start docker setup (`sudo docker-compose up -d` will do the trick)
3. create mysql db (`sudo docker-compose exec mysql echo "create database DB_NAME" | mysql -u root -p '"root123."'`) 
3. pull production database dump (`./manage.py seed_db`)

Then you can access the running app at `http://localhost:8000`
