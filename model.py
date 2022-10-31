from django.db import models

CARBON_EMISSION_INDEX_LOW = "LOW"
CARBON_EMISSION_INDEX_MODERATE = "MODERATE"
CARBON_EMISSION_INDEX_HIGH = "HIGH"

CARBON_EMISSION_INDEX = (
    (CARBON_EMISSION_INDEX_LOW, "Low"),
    (CARBON_EMISSION_INDEX_MODERATE, "Moderate"),
    (CARBON_EMISSION_INDEX_HIGH, "High"),
)


class CarbonIntensity(models.Model):
    forecast = models.IntegerField()
    actual = models.IntegerField()
    index = models.CharField(choices=CARBON_EMISSION_INDEX, default=CARBON_EMISSION_INDEX_LOW, max_length=10)

    class Meta:
        verbose_name_plural = "CarbonIntensity"

    def __str__(self):
        return self.index


class CarbonEmission(models.Model):
    from_datetime = models.DateTimeField()
    to_datetime = models.DateTimeField()
    intensity = models.ForeignKey(CarbonIntensity, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "CarbonEmissions"

    def __str__(self):
        return self.intensity


class TimeSchedule(models.Model):
    # Would be nice to have added localization to the help text
    ready_by = models.DateTimeField(help_text="Time by when the car should be 100% charged")
    charge_time = models.IntegerField(help_text="Time needed for a car battery to be fully charged")
    plug_in_time = models.DateTimeField(help_text="Timestamp at the moment when the car was plugged on a charger")
    emission = models.ForeignKey(CarbonEmission, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'TimeSchedules'

    def __str__(self):
        return self.ready_by
