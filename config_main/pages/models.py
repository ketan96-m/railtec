from __future__ import unicode_literals

from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    # class Meta:
    #     managed = False
    #     db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    # class Meta:
    #     managed = False
    #     db_table = 'auth_group_permissions'
    #     unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    # class Meta:
    #     managed = False
    #     db_table = 'auth_permission'
    #     unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    title = models.CharField(max_length=128)
    class Meta:
         managed = False
         db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    # class Meta:
    #     managed = False
    #     db_table = 'auth_user_groups'
    #     unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    # class Meta:
    #     managed = False
    #     db_table = 'auth_user_user_permissions'
    #     unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    # class Meta:
    #     managed = False
    #     db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    # class Meta:
    #     managed = False
    #     db_table = 'django_content_type'
    #     unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    # class Meta:
    #     managed = False
    #     db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    # class Meta:
    #     managed = False
    #     db_table = 'django_session'


class Metratr116(models.Model):
    id = models.IntegerField(primary_key = True)
    tr_id = models.CharField(db_column='TrainDateTime', max_length=255)
    v1n = models.DecimalField(db_column='V1N_pks', max_digits=4, decimal_places=2)  # Field name made lowercase. ##added 'default' and 'editable' properties to avoid non-nullable field error during model migrations.
    v1s = models.DecimalField(db_column='V1S_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    l1n = models.DecimalField(db_column='L1N_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    l1s = models.DecimalField(db_column='L1S_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    v3n = models.DecimalField(db_column='V3N_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    v3s = models.DecimalField(db_column='V3S_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    v3n_prot = models.DecimalField(db_column='V3N Prot', max_digits=4, decimal_places=2)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    carloc = models.CharField(db_column='carOrLoc', max_length=255)  # Field name made lowercase.
    speed = models.DecimalField(db_column='Speed', max_digits=4, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'metratr116'
        




###@author: disha###
class Backup_Frontend(models.Model):
    id = models.IntegerField(primary_key = True)
    tr_id = models.CharField(db_column='TrainDateTime', max_length=255, default="")
    v1n = models.DecimalField(db_column='V1N_pks', max_digits=4, decimal_places=2)  # Field name made lowercase. ##added 'default' and 'editable' properties to avoid non-nullable field error during model migrations.
    v1s = models.DecimalField(db_column='V1S_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    l1n = models.DecimalField(db_column='L1N_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    l1s = models.DecimalField(db_column='L1S_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    v3n = models.DecimalField(db_column='V3N_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    v3s = models.DecimalField(db_column='V3S_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    v3n_prot = models.DecimalField(db_column='V3NProt', max_digits=4, decimal_places=2)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    carloc = models.CharField(db_column='carOrLoc', max_length=255)  # Field name made lowercase.
    speed = models.DecimalField(db_column='Speed', max_digits=4, decimal_places=2, default="", editable=False)  # Field name made lowercase.
    

    class Meta:
        managed = True
        db_table = 'metra_backup_frontend_0918'


class Backup_Speed(models.Model):
    id = models.IntegerField(primary_key = True)
    tr_id = models.CharField(db_column='TrainDateTime', max_length=255, default="")
    v1n = models.DecimalField(db_column='V1N_pks', max_digits=4, decimal_places=2)  # Field name made lowercase. ##added 'default' and 'editable' properties to avoid non-nullable field error during model migrations.
    v1s = models.DecimalField(db_column='V1S_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    l1n = models.DecimalField(db_column='L1N_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    l1s = models.DecimalField(db_column='L1S_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    v3n = models.DecimalField(db_column='V3N_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    v3s = models.DecimalField(db_column='V3S_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    v3n_prot = models.DecimalField(db_column='V3N Prot', max_digits=4, decimal_places=2)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    carloc = models.CharField(db_column='carOrLoc', max_length=255)  # Field name made lowercase.
    speed = models.DecimalField(db_column='Speed', max_digits=25, decimal_places=2)  # Field name made lowercase.
    

    class Meta:
        managed = True
        db_table = 'final_dataset_speed'
    

class Cta_backup(models.Model):
    id = models.IntegerField(db_column = 'Unique_ID', primary_key = True)
    car_num = models.FloatField(db_column='Car_num')
    run_num = models.FloatField(db_column='Run_num')
    axle = models.FloatField(db_column='Axle')
    train_id = models.CharField(db_column='TrainDateTime', max_length=255, default="")
    speed = models.DecimalField(db_column='Speed', max_digits=25, decimal_places=2)  # Field name made lowercase.
    l2w = models.DecimalField(db_column='L2W_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    l2e = models.DecimalField(db_column='L2E_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    l1w = models.DecimalField(db_column='L1W_pks', max_digits=4, decimal_places=2)  # Field name made lowercase. ##added 'default' and 'editable' properties to avoid non-nullable field error during model migrations.
    l1e = models.DecimalField(db_column='L1E_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    v2w = models.DecimalField(db_column='V2W_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    v2e = models.DecimalField(db_column='V2E_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    v1w = models.DecimalField(db_column='V1W_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    v1e = models.DecimalField(db_column='V1E_pks', max_digits=4, decimal_places=2)  # Field name made lowercase.
    

    class Meta:
        managed = False
        db_table = 'cta_backup_10222022'
    