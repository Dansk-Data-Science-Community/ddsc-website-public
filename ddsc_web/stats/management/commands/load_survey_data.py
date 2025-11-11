from django.core.management.base import BaseCommand
from django.db import transaction
from stats.models import SurveyData
from datetime import datetime
from django.utils.timezone import make_aware
import json


class Command(BaseCommand):
    help = "Load data from a JSON file into SurveyData model"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to the JSON file")
        parser.add_argument(
            "--batch_size",
            type=int,
            default=1000,
            help="Number of records to insert in a batch",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        file_path = options["file_path"]
        batch_size = options["batch_size"]

        with open(file_path, "r") as file:
            data = json.load(file)

        total_records = len(data)

        for start in range(0, total_records, batch_size):
            end = start + batch_size

            records_to_insert = [
                self.__create_surveydata_record(record) for record in data[start:end]
            ]

            SurveyData.objects.bulk_create(records_to_insert)

        self.stdout.write(
            self.style.SUCCESS('Data successfully loaded from "{}"'.format(file_path))
        )

    def __create_surveydata_record(self, record):
        return SurveyData(
            user_id=record["user_id"],
            question=record["question"],
            answer=record["answer"],
            year=record["year"],
            monthly_salary=record["monthly_salary"],
            created_at=make_aware(datetime.fromisoformat(record["created_at"])),
        )
