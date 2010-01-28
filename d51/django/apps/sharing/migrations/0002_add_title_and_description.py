
from south.db import db
from django.db import models
from d51.django.apps.sharing.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Share.title'
        db.add_column('sharing_share', 'title', models.CharField(max_length=255, null=True, blank=True))
        
        # Adding field 'Share.description'
        db.add_column('sharing_share', 'description', models.TextField(null=True, blank=True))
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Share.title'
        db.delete_column('sharing_share', 'title')
        
        # Deleting field 'Share.description'
        db.delete_column('sharing_share', 'description')
        
    
    
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
            'description': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_fulfilled': ('models.BooleanField', [], {'default': 'False'}),
            'service': ('models.CharField', [], {'max_length': '255'}),
            'title': ('models.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {})
        },
        'sharing.url': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'url': ('models.URLField', [], {})
        }
    }
    
    complete_apps = ['sharing']
