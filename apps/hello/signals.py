from django.db.models.signals import post_save, post_delete
from models import LogWorks


def my_callback(sender, **kwargs):
    """
        This function add into model LogWorks
        log works (creation/editing/deletion) with all models
    """
    if sender._meta.object_name == 'LogWorks':
        return None
    sign = LogWorks()
    work = 'deletion'
    if 'created' in kwargs.keys():
        work = 'creation' if kwargs['created'] else 'editing'

    sign.mod_name = sender._meta.object_name
    sign.work = work
    sign.save()
    return None

post_save.connect(my_callback)
post_delete.connect(my_callback)
