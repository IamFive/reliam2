# -*- coding: utf-8 -*-


#===================================================
# This py file is used for running celery from cmd
#
# Example:
#        celery worker -A reliam2.app
#        celerybeat -A reliam.celeryd -f e:\celerybeat.log
#        celeryd -A reliam.celeryd -f e:\crontabs.log
#===================================================


# set default resource path
# if not os.environ.has_key(ResourceLoader.ENV_VAR_NAME):
#    resource_folder = '/var/www/reliam2/resources'
#    os.environ.setdefault(ResourceLoader.ENV_VAR_NAME, resource_folder)

# need to initial Flask-APP

__test__ = False


from celery.app.base import Celery



def init_celery():
    
    from reliam.common.app import startup_app
    
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


#==============================================================================
#  Task definition starts
#==============================================================================
@celery.task(name='recipient.ImportZip')
def import_zip_task(zip_id):
    ''' import recipient list from zip file '''
    
    print '====================' + zip_id
    return True

@celery.task(name='recipient.printlog')
def printlog():
    ''' import recipient list from zip file '''
    print '========== Celery Task Run =========='
