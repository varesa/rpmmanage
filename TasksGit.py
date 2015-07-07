import AsyncProcess

from app import celery

@celery.task(name="git.clone")
def git_clone():
    pass #    db.get_session()
