# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ubicacions'
        db.create_table(u'ifestes_ubicacions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('provincia', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('comarca', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('poble', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('adressa', self.gf('django.db.models.fields.TextField')(max_length=100)),
        ))
        db.send_create_signal(u'ifestes', ['Ubicacions'])

        # Adding model 'Festes'
        db.create_table(u'ifestes_festes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('data_inici', self.gf('django.db.models.fields.DateTimeField')()),
            ('data_fi', self.gf('django.db.models.fields.DateTimeField')()),
            ('categoria', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('descripcio', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('localitat', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'ifestes', ['Festes'])

        # Adding model 'Events'
        db.create_table(u'ifestes_events', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tipus', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('descripcio', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('festa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ifestes.Festes'])),
            ('ubicacio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ifestes.Ubicacions'])),
            ('data', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'ifestes', ['Events'])

        # Adding model 'Usuaris'
        db.create_table(u'ifestes_usuaris', (
            (u'user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'ifestes', ['Usuaris'])

        # Adding M2M table for field assistencia on 'Usuaris'
        m2m_table_name = db.shorten_name(u'ifestes_usuaris_assistencia')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('usuaris', models.ForeignKey(orm[u'ifestes.usuaris'], null=False)),
            ('festes', models.ForeignKey(orm[u'ifestes.festes'], null=False))
        ))
        db.create_unique(m2m_table_name, ['usuaris_id', 'festes_id'])

        # Adding model 'Organitzadors'
        db.create_table(u'ifestes_organitzadors', (
            (u'usuaris_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ifestes.Usuaris'], unique=True, primary_key=True)),
            ('empresa', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'ifestes', ['Organitzadors'])

        # Adding M2M table for field festa on 'Organitzadors'
        m2m_table_name = db.shorten_name(u'ifestes_organitzadors_festa')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('organitzadors', models.ForeignKey(orm[u'ifestes.organitzadors'], null=False)),
            ('festes', models.ForeignKey(orm[u'ifestes.festes'], null=False))
        ))
        db.create_unique(m2m_table_name, ['organitzadors_id', 'festes_id'])

        # Adding M2M table for field event on 'Organitzadors'
        m2m_table_name = db.shorten_name(u'ifestes_organitzadors_event')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('organitzadors', models.ForeignKey(orm[u'ifestes.organitzadors'], null=False)),
            ('events', models.ForeignKey(orm[u'ifestes.events'], null=False))
        ))
        db.create_unique(m2m_table_name, ['organitzadors_id', 'events_id'])


    def backwards(self, orm):
        # Deleting model 'Ubicacions'
        db.delete_table(u'ifestes_ubicacions')

        # Deleting model 'Festes'
        db.delete_table(u'ifestes_festes')

        # Deleting model 'Events'
        db.delete_table(u'ifestes_events')

        # Deleting model 'Usuaris'
        db.delete_table(u'ifestes_usuaris')

        # Removing M2M table for field assistencia on 'Usuaris'
        db.delete_table(db.shorten_name(u'ifestes_usuaris_assistencia'))

        # Deleting model 'Organitzadors'
        db.delete_table(u'ifestes_organitzadors')

        # Removing M2M table for field festa on 'Organitzadors'
        db.delete_table(db.shorten_name(u'ifestes_organitzadors_festa'))

        # Removing M2M table for field event on 'Organitzadors'
        db.delete_table(db.shorten_name(u'ifestes_organitzadors_event'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ifestes.events': {
            'Meta': {'object_name': 'Events'},
            'data': ('django.db.models.fields.DateTimeField', [], {}),
            'descripcio': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'festa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ifestes.Festes']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tipus': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ubicacio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ifestes.Ubicacions']"})
        },
        u'ifestes.festes': {
            'Meta': {'object_name': 'Festes'},
            'categoria': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'data_fi': ('django.db.models.fields.DateTimeField', [], {}),
            'data_inici': ('django.db.models.fields.DateTimeField', [], {}),
            'descripcio': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'localitat': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'ifestes.organitzadors': {
            'Meta': {'object_name': 'Organitzadors', '_ormbases': [u'ifestes.Usuaris']},
            'empresa': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'event': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ifestes.Events']", 'symmetrical': 'False', 'blank': 'True'}),
            'festa': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ifestes.Festes']", 'symmetrical': 'False', 'blank': 'True'}),
            u'usuaris_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['ifestes.Usuaris']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'ifestes.ubicacions': {
            'Meta': {'object_name': 'Ubicacions'},
            'adressa': ('django.db.models.fields.TextField', [], {'max_length': '100'}),
            'comarca': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'poble': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'provincia': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'ifestes.usuaris': {
            'Meta': {'object_name': 'Usuaris', '_ormbases': [u'auth.User']},
            'assistencia': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ifestes.Festes']", 'symmetrical': 'False'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['ifestes']