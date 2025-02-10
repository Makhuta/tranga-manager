import socket
import ipaddress
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator

class IPOrHostnameField(models.GenericIPAddressField):
    def to_python(self, value):
        """
        Convert the value to an IP address. If the value is a valid IP address, 
        return it. If it's a hostname, resolve it to an IP address.
        """
        if value is None:
            return None
        try:
            # First try to parse the value as an IP address
            return ipaddress.ip_address(value)
        except ValueError:
            # If it's not an IP address, treat it as a hostname
            try:
                ip_address = socket.gethostbyname(value)
                return ipaddress.ip_address(ip_address)
            except socket.gaierror:
                raise ValidationError(f"{value} is not a valid IP address or hostname.")

    def get_prep_value(self, value):
        """
        Ensure that the value is in the correct format (IP address) before saving it.
        """
        if isinstance(value, ipaddress.IPv4Address) or isinstance(value, ipaddress.IPv6Address):
            return str(value)
        elif isinstance(value, str):
            # If it's a hostname, resolve it to IP
            try:
                resolved_ip = socket.gethostbyname(value)
                return resolved_ip
            except socket.gaierror:
                raise ValidationError(f"{value} could not be resolved to an IP address.")
        return super().get_prep_value(value)


# Create your models here.
class API(models.Model):
    name = models.CharField(max_length=64, blank=True, default="")
    ip = IPOrHostnameField()
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