# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MyData.photo'
        db.add_column(u'hello_mydata', 'photo',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MyData.photo'
        db.delete_column(u'hello_mydata', 'photo')


    models = {
        u'hello.mydata': {
            'Meta': {'object_name': 'MyData'},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'contacts': ('django.db.models.fields.TextField', [], {}),
            'date_birth': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'hello.storagerequests': {
            'Meta': {'ordering': "['-id']", 'object_name': 'StorageRequests'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'req_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['hello']