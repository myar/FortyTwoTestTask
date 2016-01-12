from django.db import models


class MyData(models.Model):
    name = models.CharField('Your name', max_length=50,
                            help_text='Max. 50 chars')
    surname = models.CharField('Your surname', max_length=50,
                               help_text='Max. 50 chars')
    date_birth = models.DateField('Your data birth')
    bio = models.TextField('Biography')
    email = models.EmailField('Email')
    jabber = models.CharField('Jabber', max_length=50,
                              help_text='Max. 50 chars')
    skype = models.CharField('Skype', max_length=50, help_text='Max. 50 char')
    contacts = models.TextField('Your contact')

    def __unicode__(self):
        return u'%s %s' % (self.name, self.surname)
