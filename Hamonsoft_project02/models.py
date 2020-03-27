from django.db import models


class DB_impo(models.Model):
    idx = models.IntegerField(primary_key=True, auto_created=True)
    name = models.TextField()
    period = models.TextField()
    content = models.TextField()
    new_date = models.DateTimeField(auto_now_add=True)
    sched_id = models.TextField()

    class Meta:
        managed = False
        db_table = 'db_impo'
