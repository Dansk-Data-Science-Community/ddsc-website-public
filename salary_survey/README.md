# Salary survey preprocessor

The data for the salary survey is preprocessed in this little script to make it fit the model object in django.
The script assumes files named `Data - 2022.csv` and `Data - 2023.csv` where the 2022 file is `;` separeted and the 2023 is `,` separated.

The data is then loaded into django using this command.

```bash
python manage.py load_survey_data path/to/survey_data.json --settings=ddsc_web.settings.dev
```

Use `--settings=ddsc_web.settings.prod` for production environment
