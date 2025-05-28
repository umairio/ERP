from django.db.models import TextChoices


class Role(TextChoices):
    OWNER = 'owner', 'Owner'
    SALESMAN = 'salesman', 'Salesman'
    CUSTOMER = 'customer', 'Customer'
    STAFF = 'staff', 'Staff'
