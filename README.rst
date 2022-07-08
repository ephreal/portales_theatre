************************
Portales Theatre Website
************************

Setup
#####

To set up your environment for fist time use, ensure you have the following installed.

1. MariaDB >= 10.7.3

2. Python >= 3.8

MariaDB setup
*************

1. Download and install MariaDB. This will vary depending on the OS you are using.

2. Once installed, ensure the mariadb service (sometimes called mysql) is running.

3. Log in with the root user using the password you created
::
    mysql -u root -p

4. Create the database
::
    create database portales_theatre;

5. Create the user for the database
::
    grant all privileges on portales_theatre.* to 'portales_theatre'@'localhost' identified by '123';

6. Close out mariadb. The rest will be handled through python.
::
    exit;

Altogether, the commands are
::
    mysql -u root -p
    create database portales_theatre;
    grant all privileges on portales_theatre.* to 'portales_theatre'@'localhost' identified by '123';
    exit;

Mariadb has been setup.

Python Setup
************

Download and install a python version that is >= 3.8. I personally used python 3.10.2, but any version greater than 3.8 should be compatible.

To run python code, it's best to use a virtual environment. This allows you to keep your python modules separate so you don't inadvertently cause trouble by trying to install incompatible modules into the same environment.

Open a terminal and navigate to the directory that this readme file is in. Then create a virtual environment.
::
    python -m venv env

Now that the environment has been setup, activate the environment. Anytime you want to run the website, you'll have to run this command.
::
    source env/bin/activate

NOTE: I know that the environment activation is different on Windows. You'll have to look online for information on how to do that.

Once activated, install the python module requirements through pip
::
    pip install -r requirements.txt

Altogether, the commands are
::
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt

Python has been setup.

********************
Running the website.
********************

After you have completed the setup, you are ready to run the website. First ensure that your python environment is activated.
::
    source env/bin/activate

Note: If you are using the fish shell, you will need to instead activate the following file
::
    source env/bin/activate.fish

NOTE: I know that the environment activation is different on Windows. You'll have to look online for information on how to do that.

After the environment has been activated, run the file named "run.py".
::
    python run.py

The website will start up and be accessible if you web browse to
::
    http://localhost:5001

*****************
Diagnosing Errors
*****************

If you get errors when trying to run the site, or while running the site, about database models missing, being incorrect, etc, make sure you're using the most recent version of the database.
::
    ./migrate.sh

If the migration succeeds without errors, verify that your database is indeed fully up to date.
::
    FLASK_APP=theatre flask db current --version

If your database is fully up to date, it may be worth removing and adding it back through the mysql commands.
