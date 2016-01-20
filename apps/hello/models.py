from django.db import models

from PIL import Image


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
    photo = models.ImageField(upload_to='photos', blank=True, null=True)

    def __unicode__(self):
        return u'%s %s' % (self.name, self.surname)

    def save(self):
        super(MyData, self).save()
        if self.photo:
            image = Image.open(self.photo)
            width, height = image.size
            ratio = float(float(width) / float(height))
            size = (200, int(round(200 / ratio, 0)))
            image = image.resize(size, Image.ANTIALIAS)
            image.save(self.photo.path)





class StorageRequests(models.Model):
    host = models.CharField('Host', max_length=255)
    path = models.CharField('Path', max_length=255)
    method = models.CharField('Method', max_length=30)
    req_date = models.DateTimeField('Data request', auto_now_add=True)
    viewed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id', ]

    def __unicode__(self):
        return self.host
