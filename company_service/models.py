from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from django.db.models import Sum
from users.models import User
from common.models import IndexedTimeStampedModel
from django.contrib.postgres.fields import ArrayField

class Company(IndexedTimeStampedModel):
    trade_name = models.CharField(max_length=256)
    corporate_name = models.CharField(max_length=256, blank=True)
    cnpj = models.CharField(max_length=14, blank=True)
    email = models.CharField(max_length=256, blank=True)
    phone = models.CharField(max_length=256, blank=True)
    address = models.CharField(max_length=256, blank=True)
    zip_code = models.CharField(max_length=256, blank=True)
    neighborhood = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    state = models.CharField(max_length=256, blank=True)
    country = models.CharField(max_length=256, blank=True)
    industrial_sector = models.CharField(max_length=256, blank=True)
    size = models.CharField(max_length=256, blank=True)
    slug = models.SlugField(db_index=True)
    is_active = models.BooleanField(default=False)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.trade_name

class Product(IndexedTimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class UnitOfMeasurement(IndexedTimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    is_default = models.BooleanField(default=False)
    conversion_factor = models.FloatField(default=1.0)

    def __str__(self):
        return self.name

class CodeGroup(IndexedTimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    STOP_CODE = 'StopCode'
    WASTE_CODE = 'WasteCode'
    REWORK_CODE = 'ReworkCode'
    GROUP_TYPES = (
        (STOP_CODE, 'Stop Code'),
        (WASTE_CODE, 'Waste Code'),
        (REWORK_CODE, 'Rework Code'),
    )

    group_type = models.CharField(
        max_length=256,
        choices=GROUP_TYPES,
    )

    def __str__(self):
        return self.name

class StopCode(IndexedTimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    code_group = models.ForeignKey(CodeGroup, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=256)
    is_planned = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class WasteCode(IndexedTimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    code_group = models.ForeignKey(CodeGroup, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class ReworkCode(IndexedTimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    code_group = models.ForeignKey(CodeGroup, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class TurnScheme(IndexedTimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Turn(IndexedTimeStampedModel):
    turn_scheme = models.ForeignKey(TurnScheme, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=256)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days_of_week = ArrayField(
        models.IntegerField(),
        default=list,
    )

    def __str__(self):
        return self.name


class ProductionLine(IndexedTimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    discount_rework = models.BooleanField(default=False)
    discount_waste = models.BooleanField(default=False)
    stop_on_production_absence = models.BooleanField(default=False)
    time_to_consider_absence = models.IntegerField(blank=True, null=True)
    reset_production_changing_order = models.BooleanField(default=False)
    micro_stop_seconds = models.IntegerField(blank=True, null=True)
    turn_scheme = models.ForeignKey(TurnScheme, blank=True, null=True, on_delete=models.SET_NULL)

    def in_progress_order(self):
        return self.production_orders.filter(state=ProductionOrder.IN_PROGRESS).first()

    def __str__(self):
        return self.name


class ProductionLineProductionRate(IndexedTimeStampedModel):
    production_line = models.ForeignKey(ProductionLine, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.FloatField()


class ProductionOrder(IndexedTimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    production_line = models.ForeignKey(ProductionLine, on_delete=models.SET_NULL, blank=True, null=True, related_name="production_orders")
    code = models.CharField(max_length=256)
    quantity = models.IntegerField(default=0)

    RELEASED = 'Released'
    IN_PROGRESS = 'InProgress'
    INTERRUPTED = 'Interrupted'
    DONE = 'Done'
    STATES = (
        (RELEASED, 'Released'),
        (IN_PROGRESS, 'In Progress'),
        (INTERRUPTED, 'Interrupted'),
        (DONE, 'Done'),
    )

    state = models.CharField(
        max_length=256,
        choices=STATES,
        default=RELEASED,
        db_index=True
    )

    def production_quantity(self):
        return self.event_quantity(event_type=ProductionEvent.PRODUCTION)

    def waste_quantity(self):
        return self.event_quantity(event_type=ProductionEvent.WASTE)

    def rework_quantity(self):
        return self.event_quantity(event_type=ProductionEvent.REWORK)

    def event_quantity(self, event_type):
        return self.production_events.filter(event_type=event_type).aggregate(Sum('quantity'))['quantity__sum']

    def __str__(self):
        return self.code

class Collector(IndexedTimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    mac = models.CharField(max_length=256)
    
    WISE = 'Wise'
    HW = 'HW'
    LORA = 'Lora'
    TYPES = (
        (WISE, 'Wise'),
        (HW, 'HW'),
        (LORA, 'Lora'),
    )
    collector_type = models.CharField(
        max_length=256,
        choices=TYPES,
    )

    def __str__(self):
        return self.mac

class Channel(IndexedTimeStampedModel):
    collector = models.ForeignKey(Collector, on_delete=models.CASCADE)
    production_line = models.ForeignKey(ProductionLine, blank=True, null=True, on_delete=models.SET_NULL)
    number = models.IntegerField()

    GOOD = 'Good'
    REWORK = 'Rework'
    WASTE = 'Waste'
    TYPES = (
        (GOOD, 'Good'),
        (REWORK, 'Rework'),
        (WASTE, 'Waste'),
    )

    channel_type = models.CharField(
        max_length=256,
        choices=TYPES,
        default=GOOD
    )
    inverse_state = models.BooleanField(default=False)
    is_cumulative = models.BooleanField(default=False)

    def __str__(self):
        return str(self.number)

class StateEvent(IndexedTimeStampedModel):
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.SET_NULL, null=True, blank=True)
    production_line = models.ForeignKey(ProductionLine, on_delete=models.CASCADE)
    stop_code = models.ForeignKey(StopCode, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    channel = models.ForeignKey(Channel, on_delete=models.SET_NULL, null=True, blank=True)
    event_datetime = models.DateTimeField(default=None, db_index=True)

    ON = 'On'
    OFF = 'Off'
    STATES = (
        (ON, 'On'),
        (OFF, 'Off'),
    )

    state = models.CharField(
        max_length=3,
        choices=STATES,
        default=ON,
        db_index=True
    )


class ProductionEvent(IndexedTimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    production_line = models.ForeignKey(ProductionLine, on_delete=models.CASCADE)
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name="production_events")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    channel = models.ForeignKey(Channel, on_delete=models.SET_NULL, null=True, blank=True)
    unit_of_measurement = models.ForeignKey(UnitOfMeasurement, on_delete=models.SET_NULL, null=True, blank=True)
    event_datetime = models.DateTimeField(default=None, db_index=True)
    quantity = models.IntegerField(default=0)

    PRODUCTION = 'Production'
    WASTE = 'Waste'
    REWORK = 'Rework'
    EVENT_TYPES = (
        (PRODUCTION, 'Production'),
        (WASTE, 'Waste'),
        (REWORK, 'Rework'),
    )

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        default=PRODUCTION,
        db_index=True
    )

    waste_code = models.ForeignKey(WasteCode, on_delete=models.SET_NULL, null=True, blank=True)
    rework_code = models.ForeignKey(ReworkCode, on_delete=models.SET_NULL, null=True, blank=True)
