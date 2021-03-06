# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding field 'Revision.branch_id'
        db.add_column('codespeed_revision', 'branch', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['codespeed.Branch']))
        # Removing unique constraint on 'Revision', fields ['commitid', 'project', branch']
        db.delete_unique('codespeed_revision', ['commitid', 'project_id', 'branch'])
        # Delete field 'Revision.branch'
        db.delete_column('codespeed_revision', 'branch')
        # Adding unique constraint on 'Revision', fields ['commitid', 'project_id', 'branch_id']
        db.create_unique('codespeed_revision', ['commitid', 'project_id', 'branch_id'])


        # Adding index on 'Revision', fields ['branch']
        # NOTE: commented out because it can cause an
        # "index codespeed_revision_d56253ba already exists"
        # db.create_index('codespeed_revision', ['branch_id'])


    def backwards(self, orm):

        # Removing index on 'Revision', fields ['branch']
        db.delete_index('codespeed_revision', ['branch_id'])

        # Renaming column for 'Revision.branch' to match new field type.
        db.rename_column('codespeed_revision', 'branch_id', 'branch')
        # Changing field 'Revision.branch'
        db.alter_column('codespeed_revision', 'branch', self.gf('django.db.models.fields.CharField')(max_length=15))


    models = {
        'codespeed.benchmark': {
            'Meta': {'object_name': 'Benchmark'},
            'benchmark_type': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '1'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lessisbetter': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'units': ('django.db.models.fields.CharField', [], {'default': "'seconds'", 'max_length': '20'}),
            'units_title': ('django.db.models.fields.CharField', [], {'default': "'Time'", 'max_length': '30'})
        },
        'codespeed.branch': {
            'Meta': {'unique_together': "(('name', 'project'),)", 'object_name': 'Branch'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'branches'", 'to': "orm['codespeed.Project']"})
        },
        'codespeed.environment': {
            'Meta': {'object_name': 'Environment'},
            'cpu': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kernel': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'memory': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        'codespeed.executable': {
            'Meta': {'object_name': 'Executable'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'executables'", 'to': "orm['codespeed.Project']"})
        },
        'codespeed.project': {
            'Meta': {'object_name': 'Project'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'repo_pass': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'repo_path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'repo_type': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'repo_user': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'track': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'codespeed.report': {
            'Meta': {'unique_together': "(('revision', 'executable', 'environment'),)", 'object_name': 'Report'},
            '_tablecache': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'colorcode': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '10'}),
            'environment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reports'", 'to': "orm['codespeed.Environment']"}),
            'executable': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reports'", 'to': "orm['codespeed.Executable']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'revision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reports'", 'to': "orm['codespeed.Revision']"}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        'codespeed.result': {
            'Meta': {'unique_together': "(('revision', 'executable', 'benchmark', 'environment'),)", 'object_name': 'Result'},
            'benchmark': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': "orm['codespeed.Benchmark']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'environment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': "orm['codespeed.Environment']"}),
            'executable': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': "orm['codespeed.Executable']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'revision': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to': "orm['codespeed.Revision']"}),
            'std_dev': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'val_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'val_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'codespeed.revision': {
            'Meta': {'unique_together': "(('commitid', 'project', 'branch'),)", 'object_name': 'Revision'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'branch'", 'to': "orm['codespeed.Branch']"}),
            'commitid': ('django.db.models.fields.CharField', [], {'max_length': '42'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'to': "orm['codespeed.Project']"}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        }
    }

    complete_apps = ['codespeed']
