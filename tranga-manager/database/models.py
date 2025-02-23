import socket
import ipaddress
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator

# Create your models here.
class API(models.Model):
    name = models.CharField(max_length=64, blank=True, default="")
    ip_or_hostname = models.CharField(max_length=255)
    port = models.PositiveIntegerField(validators=[MaxValueValidator(65535)])
    timeout = models.PositiveIntegerField(validators=[MaxValueValidator(60)], default=1)

    class Meta:
        verbose_name = "API"
        verbose_name_plural = "APIs"
        constraints = [
            models.UniqueConstraint(fields=['ip_or_hostname', 'port'], name='unique_ip_port')
        ]

    @property
    def ip(self):
        if self.ip_or_hostname:
            try:
                # Try to parse it as an IP address
                return ipaddress.ip_address(self.ip_or_hostname)
            except ValueError:
                # If it's a hostname, resolve it to an IP address
                try:
                    ip_address = socket.gethostbyname(self.ip_or_hostname)
                    return ipaddress.ip_address(ip_address)
                except socket.gaierror:
                    # raise ValueError(f"{self.ip_or_hostname} could not be resolved.")
                    return None
        return None
    
    def __str__(self):
        if len(self.name) == 0:
            return f'{self.ip_or_hostname}:{self.port}'
        return self.name
    
    def try_save(self):
        try:
            if not self.timeout:
                self.timeout = 1
            self.save()
            return True
        except Exception as e:
            return False