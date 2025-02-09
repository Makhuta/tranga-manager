from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class API(models.Model):
    name = models.CharField(max_length=64, blank=True, default="")
    ip = models.GenericIPAddressField()
    port = models.PositiveIntegerField(validators=[MaxValueValidator(65535)])
    timeout = models.PositiveIntegerField(validators=[MaxValueValidator(60)], default=1)

    class Meta:
        verbose_name = "API"
        verbose_name_plural = "APIs"
        constraints = [
            models.UniqueConstraint(fields=['ip', 'port'], name='unique_ip_port')
        ]

    def __str__(self):
        if len(self.name) == 0:
            return f'{self.ip}:{self.port}'
        return self.name
    
    def try_save(self):
        try:
            if not self.timeout:
                self.timeout = 1
            self.save()
            return True
        except Exception as e:
            return False