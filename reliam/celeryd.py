# -*- coding: utf-8 -*-
'''
This py file is used for running celery from cmd

Example:
       celery worker -A reliam2.app
       celerybeat -A reliam.celeryd -f e:\celerybeat.log
       celeryd -A reliam.celeryd -f e:\crontabs.log
'''

import datetime
import os

from celery.app.base import Celery

from reliam.common.tools.env import ResourceLoader
from reliam.common.tools.files import get_csv_dialect
from reliam.projects import get_zip_path


__test__ = False


def init_celery():
    
    from reliam.common.app import startup_app
    
    os.environ.setdefault(ResourceLoader.ENV_VAR_NAME,
                          '/home/www-data/reliam2/resources/prod')
    
    app = startup_app()
    celery = Celery(app.import_name)
    celery.conf.add_defaults(app.config)
    # celery.log.setup(loglevel=logging.INFO, logfile=app.config.get('CELERYD_LOG_FILE'),
    #                  redirect_stdouts=True, redirect_level='INFO')
    celery.app = app
    
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
            
    celery.Task = ContextTask
    return celery


# initial celery
celery = init_celery()

print celery.Task


#==============================================================================
#  Task definition starts
#==============================================================================
@celery.task()
def import_zip_task(zip_id):
    ''' import recipient list from zip file '''
    
    # TODO i don't know why ContextTask context is not work here
    # will check it later
    with celery.app.app_context():
        
        print 'Start import zip task for zip id : [' + zip_id + ']'
    
        import csv
        from reliam.models import User
        from reliam.models import ImportTask, Recipient
        from reliam.common.choices import ImportStatus, ZipFileStatus
        
        # update import task status
        it = ImportTask.objects.get_or_404(id=zip_id)
        it.start_time = datetime.datetime.now()
        it.status = ImportStatus.Importing[0]
        it.save()
        
        # parse recipient file
        zipfile = it.zip
        user = User.objects.get(id=zipfile.created_by)
        abs_zipfile_path = get_zip_path(zipfile.path, user)
        _, dialect = get_csv_dialect(abs_zipfile_path)
        
        success = 0
        failed = 0
        column_size = len(it.tokens)
        with open(abs_zipfile_path, 'rU') as f:
            reader = csv.reader(f, dialect)
            
            first = True
            produced = []
            for row in reader:
                
                if it.ignore_header and first:
                    first = False
                    continue
                
                if len(row) != column_size:
                    failed = failed + 1
                else:
                    # TODO need to validate here
                    email = row[it.email_col_index]  # get email value
                    as_list = it.tokens, row
                    mapped = dict((item[0], item[1]) for item in zip(*as_list)
                                  if item[0] != '' and item[0] != 'email')
                    produced.append(Recipient(email=email, props=mapped, created_by=user.id))
                    success = success + 1
                if len(produced) >= 300:
                    Recipient.objects.insert(produced)
                    produced = []
                    
            if len(produced) >= 0:
                Recipient.objects.insert(produced)
            
            # update zip file
            zipfile.success = success
            zipfile.failed = failed
            zipfile.status = ZipFileStatus.Imported[0]
            zipfile.save()
            
            # update import task
            it.end_time = datetime.datetime.now()
            it.status = ImportStatus.Finished[0]
            it.save()
        
        print 'Import zip task for zip id : [' + zip_id + '] finished'

@celery.task(name='recipient.printlog')
def printlog():
    ''' import recipient list from zip file '''
    print '========== Celery Task Run =========='
