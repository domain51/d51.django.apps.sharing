
from south.db import db
from django.db import models
from d51.django.apps.sharing.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Alternate'
        db.create_table('sharing_alternate', (
            ('id', models.AutoField(primary_key=True)),
            ('original_url', models.ForeignKey(orm.URL, related_name='alternates')),
            ('url', models.URLField(null=True, blank=True)),
            ('provider', models.CharField(max_length=255)),
        ))
        db.send_create_signal('sharing', ['Alternate'])
        
        # Adding model 'Share'
        db.create_table('sharing_share', (
            ('id', models.AutoField(primary_key=True)),
            ('alternate', models.ForeignKey(orm.Alternate, related_name='shares')),
            ('is_fulfilled', models.BooleanField(default=False)),
            ('user', models.ForeignKey(orm['auth.User'])),
            ('service', models.CharField(max_length=255)),
        ))
        db.send_create_signal('sharing', ['Share'])
        
        # Adding model 'URL'
        db.create_table('sharing_url', (
            ('id', models.AutoField(primary_key=True)),
            ('url', models.URLField()),
        ))
        db.send_create_signal('sharing', ['URL'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Alternate'
        db.delete_table('sharing_alternate')
        
        # Deleting model 'Share'
        db.delete_table('sharing_share')
        
        # Deleting model 'URL'
        db.delete_table('sharing_url')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'sharing.alternate': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'original_url': ('models.ForeignKey', ["orm['sharing.URL']"], {'related_name': "'alternates'"}),
            'provider': ('models.CharField', [], {'max_length': '255'}),
            'url': ('models.URLField', [], {'null': 'True', 'blank': 'True'})
        },
        'sharing.share': {
            'alternate': ('models.ForeignKey', ["orm['sharing.Alternate']"], {'related_name': "'shares'"}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_fulfilled': ('models.BooleanField', [], {'default': 'False'}),
            'service': ('models.CharField', [], {'max_length': '255'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {})
        },
        'sharing.url': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'url': ('models.URLField', [], {})
        }
    }
    
    complete_apps = ['sharing']
