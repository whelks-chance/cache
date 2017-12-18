from django.db import models

# Create your models here.


class CacheSurvey(models.Model):
    timestamp = models.TextField()
    entered_by = models.TextField()
    dataset_name = models.TextField()
    data_owner = models.TextField()
    category1 = models.TextField()
    category2 = models.TextField()
    category_notes = models.TextField()
    source_of_information = models.TextField()
    source_weblink = models.TextField()
    dataset_content = models.TextField()
    geographic_coverage = models.TextField()
    geographic_units = models.TextField()
    geography_notes = models.TextField()
    time_period_from = models.TextField()
    time_period_to = models.TextField()
    time_frequency = models.TextField()
    time_notes = models.TextField()
    data_type = models.TextField()
    data_type_notes = models.TextField()
    data_quality = models.TextField()
    data_access = models.TextField()
    data_owner_attitude_to_research_use = models.TextField()
    other_notes = models.TextField()

    class Meta:
        db_table = 'user_language'

    def __unicode__(self):
        return '{} : {}'.format(self.id, self.dataset_name)
