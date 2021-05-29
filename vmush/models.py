from django.db import models


class TypeName(models.Model):
    name = models.CharField(max_length=30, unique=True)


class GameObject(models.Model):
    type_name = models.ForeignKey(TypeName, related_name='objects', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(default=False, db_index=True)
    dbid = models.PositiveIntegerField(null=False)
    created = models.PositiveIntegerField(null=False)
    name = models.CharField(max_length=255)
    latest = models.ForeignKey("GameObjectSave", null=True,  on_delete=models.SET_NULL)

    class Meta:
        unique_together = (('dbid', 'created'),)


class GameObjectSave(models.Model):
    obj = models.ForeignKey(GameObject, related_name='saves', on_delete=models.CASCADE)
    version = models.DateTimeField(null=False)
    data = models.JSONField(null=False)

    class Meta:
        unique_together = (('obj', 'version'),)


class HostAddress(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reverse_dns = models.CharField(max_length=255, null=True)


class LoginAttempt(models.Model):
    target = models.ForeignKey(GameObject, related_name='logins', on_delete=models.CASCADE)
    created = models.DateTimeField(null=False)
    fail_reason = models.PositiveSmallIntegerField(default=0)

