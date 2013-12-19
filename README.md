Reliam2
================
An email market backend system


How to use
==========

1.
Install all required packages::

    $ pip install virtualenv
    $ virtualenv reliam
    $ reliam/bin/activate
    $ reliam/bin/pip install -r requirements.txt

2.Optionally edit configuration in ``resources/default/settings*.py`` file. default setting is in ``settings.py`` file, 
    you can cover it in ``resources/prod/settings.py`` or ``resources/test/settings-test.py``

3.Run ``venv/bin/python manage.py runserver -c setting-folder-abspath`` and point your browser to [Version Api][VERSION_API]

4.
Run ``venv/bin/python manage.py initdb`` to Initialize database, you can edit the initialize data file in fold **init-data**;

5.
Run ``venv/bin/python manage.py cleardb`` to *Clear database*.

[VERSION_API]: http://localhost:5000/api/version


Install supervisor
=====

* install supervisor `apt-get install supervisor`
* setup celeryd.conf in /etc/supervisor/conf.d/
```
	[program:celeryd]
	command=/home/www-data/reliam2/venv/bin/celery worker --workdir=/home/www-data/reliam2 --pidfile=/var/run/celery/reliam.pid --logfile=/var/log/celery/reliam.log --loglevel=INFO --app=reliam.celeryd
	environment=RELIAM_RESOURCE_FOLDER='/home/www-data/reliam2/resources/prod'
	user=www-data
	group=www-data
	numprocs=1
	stdout_logfile=/var/log/celery/celeryd.log
	stderr_logfile=/var/log/celery/celeryd.log
	autostart=true
	autorestart=true
	startsecs=10
	stopwaitsecs=600
```
* remember change the folder permission for owner www-data

	`chmod +x /var/run/celery /var/log/celery/`

* run supervisor `service supervisor restart`