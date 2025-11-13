# Tagging translations
## HTML
In the *.html files tag for translation with `{% translate "Translate this string" %}`, where `Translate this string` will be marked for translation (and go in the messages template file).  
NB, all templates using translations must have `{% load i18n %}`, even if they are extended from a template already having it.  

Translator comments can also be added with `{% comment %} Translators: 'No event' header text {% endcomment %}`, but then it must be spread over separate lines, for example:
```
<h1 class="fs-3 fw-bolder">
{% comment %} Translators: 'No event' header text {% endcomment %}
{% translate "Ingen events fundet" %}
</h1>
```

## Python files
In the *.py files, import the lazy translator function (by convention it's imported as `_`): `from django.utils.translation import gettext_lazy as _`.  
Then proceed to tagging the relevant fields/elements, e.g. `_("Region Hovedstaden")`.

# Create localisation file for a new language
Run the following in the /ddsc_web folder (where the `manage.py` file is located):
```python manage.py makemessages -l en```
It'll locate any calls to the translation function (`_()`) and write them to the PO file (in this case for English).  
New locales should be added in `settings.py` under `LANGUAGES` and the PO file is created in the `locale` folder.

The created PO file(s) are updated with translations.  
It does **not** overwrite existing translations in case the language already exists.  

## Update the localisation file
When the templates or Python sources are updated, update PO-files for all current languages with the new/changed entries by running the following in the /ddsc_web folder (where the `manage.py` file is located):
```python manage.py makemessages -a```

This will not overwrite any existing translations.

## Adding translations
This an example of an entry in the PO file:
```
#: .\ddsc_web\settings\settings.py:135
msgid "Danish"
msgstr ""
```

- `#:` tells where the tagged string was found
- `msgid` is the tagged string itself
- `msgstr` is the translated string

Simply add the correct translation for the language in `msgstr`.  

## Auto-detecting translations
There's an attempt to auto-detect fitting translations via 'nearby' spellings, these are tagged as 'fuzzy' and should always be reviewed.
An example (where it has gone wrong :)):
```
#: .\events\templates\events\detail.html:39
#, fuzzy
#| msgid "Bestyrelsen"
msgid "Beskrivelse"
msgstr "Bestyrelsen"
```

`msgstr` should be manually updated to `Beskrivelsen` and the `fuzzy` mark should be removed:

```
#: .\events\templates\events\detail.html:39
msgid "Beskrivelse"
msgstr "Beskrivelse"
```

Translations tagged `fuzzy` are not used when compiling, unless explicitly expressed (`compilemessages --use-fuzzy`).

## Quickly finding what to add translations for
When the translation files become longer it gets harder to find precisely what should be edited, but you should:
- RegEx search for `msgstr ""\n\n` to find locations without translation
- Search for `#, fuzzy` to find locations with fuzzy tags
- Search for the filename(s) that have been created/edited

# Compiling new translation updates
When translation files have been updated, run the following in the /ddsc_web folder (where the `manage.py` file is located):
```python manage.py compilemessages```

It will compile all the PO files to MO files, which Django will use for translations.  


# Documentation
- [Django translation](https://docs.djangoproject.com/en/4.0/topics/i18n/translation)
- [Creation of language files](https://docs.djangoproject.com/en/dev/topics/i18n/translation/#localization-how-to-create-language-files)
- [Makemessages](https://docs.djangoproject.com/en/dev/ref/django-admin/#django-admin-makemessages)