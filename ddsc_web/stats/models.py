from django.db import models


class SurveyData(models.Model):
    class Meta:
        ordering = ["year", "question"]
        indexes = [
            models.Index(fields=["question", "year"]),
        ]

    user_id = models.IntegerField(null=False, blank=False)
    question = models.CharField(max_length=750, db_index=True)
    answer = models.TextField(null=True, blank=True)
    year = models.IntegerField(db_index=True)
    monthly_salary = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField()
