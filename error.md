ProgrammingError at /news/subscribe/
column news_newssubscriber.email does not exist
LINE 1: ...ubscriber"."id", "news_newssubscriber"."user_id", "news_news...
                                                             ^
Request Method:	POST
Request URL:	http://127.0.0.1:8000/news/subscribe/
Django Version:	4.1.5
Exception Type:	ProgrammingError
Exception Value:	
column news_newssubscriber.email does not exist
LINE 1: ...ubscriber"."id", "news_newssubscriber"."user_id", "news_news...
                                                             ^
Exception Location:	/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/db/backends/utils.py, line 89, in _execute
Raised during:	news.views.subscribe_widget
Python Executable:	/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/bin/python
Python Version:	3.11.6
Python Path:	
['/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/ddsc_web',
 '/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/ddsc_web',
 '/Library/Frameworks/Python.framework/Versions/3.11/lib/python311.zip',
 '/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11',
 '/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/lib-dynload',
 '/Users/mansstormer/Desktop/hackathon '
 'project/ddsc-website-public/.venv/lib/python3.11/site-packages',
 '__editable__.ddsc_website-0.1.0.finder.__path_hook__']
Server time:	Thu, 13 Nov 2025 19:13:54 +0100
Traceback Switch to copy-and-paste view
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/db/backends/utils.py, line 89, in _execute
                return self.cursor.execute(sql, params) …
Local vars
The above exception (column news_newssubscriber.email does not exist LINE 1: ...ubscriber"."id", "news_newssubscriber"."user_id", "news_news... ^ ) was the direct cause of the following exception:
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/core/handlers/exception.py, line 55, in inner
                response = get_response(request) …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/core/handlers/base.py, line 197, in _get_response
                response = wrapped_callback(request, *callback_args, **callback_kwargs) …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/views/decorators/http.py, line 43, in inner
            return func(request, *args, **kwargs) …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/ddsc_web/news/views.py, line 55, in subscribe_widget
        if form.is_valid(): …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/forms/forms.py, line 205, in is_valid
        return self.is_bound and not self.errors …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/forms/forms.py, line 200, in errors
            self.full_clean() …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/forms/forms.py, line 437, in full_clean
        self._clean_fields() …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/forms/forms.py, line 452, in _clean_fields
                    value = getattr(self, "clean_%s" % name)() …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/ddsc_web/news/forms.py, line 79, in clean_email
            existing = NewsSubscriber.objects.filter(email=email).first() …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/db/models/query.py, line 1047, in first
        for obj in (self if self.ordered else self.order_by("pk"))[:1]: …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/db/models/query.py, line 394, in __iter__
        self._fetch_all() …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/db/models/query.py, line 1867, in _fetch_all
            self._result_cache = list(self._iterable_class(self)) …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/db/models/query.py, line 87, in __iter__
        results = compiler.execute_sql( …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/db/models/sql/compiler.py, line 1398, in execute_sql
            cursor.execute(sql, params) …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/db/backends/utils.py, line 103, in execute
            return super().execute(sql, params) …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/db/backends/utils.py, line 67, in execute
        return self._execute_with_wrappers( …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/db/backends/utils.py, line 80, in _execute_with_wrappers
        return executor(sql, params, many, context) …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/db/backends/utils.py, line 84, in _execute
        with self.db.wrap_database_errors: …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/db/utils.py, line 91, in __exit__
                raise dj_exc_value.with_traceback(traceback) from exc_value …
Local vars
/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv/lib/python3.11/site-packages/django/db/backends/utils.py, line 89, in _execute
                return self.cursor.execute(sql, params) …
Local vars
Request information
USER
AnonymousUser

GET
No GET data

POST
Variable	Value
csrfmiddlewaretoken	
'jOORFSL1iGu0QxyS1TfEeJXdjgTgufXtkz0WGzriOMOTHM3hfBSuYlRSlDEvG06g'
name	
'Måns'
email	
'mans.stromer@hotmail.se'
FILES
No FILES data

COOKIES
Variable	Value
csrftoken	
'bVmfbRQrGgu31pFzoSN0UM4PcxVpmVjX'
sessionid	
'2yms77pamtqujw7wtjxop62dw2mnfugf'
META
Variable	Value
BUNDLED_DEBUGPY_PATH	
'/Users/mansstormer/.vscode/extensions/ms-python.debugpy-2025.16.0-darwin-arm64/bundled/libs/debugpy'
CLAUDE_CODE_SSE_PORT	
'14792'
COLORTERM	
'truecolor'
COMMAND_MODE	
'unix2003'
CONDA_DEFAULT_ENV	
'base'
CONDA_EXE	
'/opt/miniconda3/bin/conda'
CONDA_PREFIX	
'/opt/miniconda3'
CONDA_PROMPT_MODIFIER	
'(base) '
CONDA_PYTHON_EXE	
'/opt/miniconda3/bin/python'
CONDA_SHLVL	
'1'
CONTENT_LENGTH	
'131'
CONTENT_TYPE	
'application/x-www-form-urlencoded'
CSRF_COOKIE	
'bVmfbRQrGgu31pFzoSN0UM4PcxVpmVjX'
DJANGO_SETTINGS_MODULE	
'ddsc_web.settings.dev'
ENABLE_IDE_INTEGRATION	
'true'
GATEWAY_INTERFACE	
'CGI/1.1'
GIT_ASKPASS	
'********************'
HOME	
'/Users/mansstormer'
HOMEBREW_CELLAR	
'/opt/homebrew/Cellar'
HOMEBREW_PREFIX	
'/opt/homebrew'
HOMEBREW_REPOSITORY	
'/opt/homebrew'
HTTP_ACCEPT	
'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
HTTP_ACCEPT_ENCODING	
'gzip, deflate, br, zstd'
HTTP_ACCEPT_LANGUAGE	
'en-GB,en;q=0.8'
HTTP_CACHE_CONTROL	
'max-age=0'
HTTP_CONNECTION	
'keep-alive'
HTTP_COOKIE	
('csrftoken=bVmfbRQrGgu31pFzoSN0UM4PcxVpmVjX; '
 'sessionid=2yms77pamtqujw7wtjxop62dw2mnfugf')
HTTP_HOST	
'127.0.0.1:8000'
HTTP_ORIGIN	
'http://127.0.0.1:8000'
HTTP_REFERER	
'http://127.0.0.1:8000/members/board/'
HTTP_SEC_CH_UA	
'"Chromium";v="142", "Brave";v="142", "Not_A Brand";v="99"'
HTTP_SEC_CH_UA_MOBILE	
'?0'
HTTP_SEC_CH_UA_PLATFORM	
'"macOS"'
HTTP_SEC_FETCH_DEST	
'document'
HTTP_SEC_FETCH_MODE	
'navigate'
HTTP_SEC_FETCH_SITE	
'same-origin'
HTTP_SEC_FETCH_USER	
'?1'
HTTP_SEC_GPC	
'1'
HTTP_UPGRADE_INSECURE_REQUESTS	
'1'
HTTP_USER_AGENT	
('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/142.0.0.0 Safari/537.36')
INFOPATH	
'/opt/homebrew/share/info:'
LANG	
'en_US.UTF-8'
LOGNAME	
'mansstormer'
MallocNanoZone	
'0'
OLDPWD	
'/Users/mansstormer/Desktop/hackathon project/ddsc-website-public'
ORIGINAL_XDG_CURRENT_DESKTOP	
'undefined'
PATH	
('/Users/mansstormer/Desktop/hackathon '
 'project/ddsc-website-public/.venv/bin:/Applications/Postgres.app/Contents/Versions/latest/bin:/Applications/Postgres.app/Contents/Versions/latest/bin:/Applications/Postgres.app/Contents/Versions/latest/bin:/opt/miniconda3/bin:/opt/miniconda3/condabin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin:/Users/mansstormer/.vscode/extensions/ms-python.debugpy-2025.16.0-darwin-arm64/bundled/scripts/noConfigScripts:/Users/mansstormer/Library/Application '
 'Support/Code/User/globalStorage/github.copilot-chat/debugCommand')
PATH_INFO	
'/news/subscribe/'
PS1	
'(ddsc-website) (base) %n@%m %1~ %# '
PWD	
'/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/ddsc_web'
PYDEVD_DISABLE_FILE_VALIDATION	
'1'
PYTHONSTARTUP	
('/Users/mansstormer/Library/Application '
 'Support/Code/User/workspaceStorage/b832047d9c6318472d29d99ff4853302/ms-python.python/pythonrc.py')
PYTHON_BASIC_REPL	
'1'
QUERY_STRING	
''
REMOTE_ADDR	
'127.0.0.1'
REMOTE_HOST	
''
REQUEST_METHOD	
'POST'
RUN_MAIN	
'true'
SCRIPT_NAME	
''
SERVER_NAME	
'1.0.0.127.in-addr.arpa'
SERVER_PORT	
'8000'
SERVER_PROTOCOL	
'HTTP/1.1'
SERVER_SOFTWARE	
'WSGIServer/0.2'
SHELL	
'/bin/zsh'
SHLVL	
'1'
SSH_AUTH_SOCK	
'/private/tmp/com.apple.launchd.cHL0XursLj/Listeners'
TERM	
'xterm-256color'
TERM_PROGRAM	
'vscode'
TERM_PROGRAM_VERSION	
'1.102.2'
TMPDIR	
'/var/folders/7g/zfthx6_s33n7jdqw_31_vg980000gn/T/'
TZ	
'Europe/Copenhagen'
USER	
'mansstormer'
USER_ZDOTDIR	
'/Users/mansstormer'
VIRTUAL_ENV	
'/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/.venv'
VIRTUAL_ENV_PROMPT	
'ddsc-website'
VSCODE_DEBUGPY_ADAPTER_ENDPOINTS	
'/Users/mansstormer/.vscode/extensions/ms-python.debugpy-2025.16.0-darwin-arm64/.noConfigDebugAdapterEndpoints/endpoint-4d7214dc22741cd3.txt'
VSCODE_GIT_ASKPASS_EXTRA_ARGS	
'********************'
VSCODE_GIT_ASKPASS_MAIN	
'********************'
VSCODE_GIT_ASKPASS_NODE	
'********************'
VSCODE_GIT_IPC_HANDLE	
'/var/folders/7g/zfthx6_s33n7jdqw_31_vg980000gn/T/vscode-git-016ee9a3de.sock'
VSCODE_INJECTION	
'1'
VSCODE_PROFILE_INITIALIZED	
'1'
XPC_FLAGS	
'0x0'
XPC_SERVICE_NAME	
'0'
ZDOTDIR	
'/Users/mansstormer'
_	
('/Users/mansstormer/Desktop/hackathon '
 'project/ddsc-website-public/.venv/bin/python')
__CFBundleIdentifier	
'com.microsoft.VSCode'
__CF_USER_TEXT_ENCODING	
'0x1F5:0x0:0x0'
wsgi.errors	
<_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>
wsgi.file_wrapper	
<class 'wsgiref.util.FileWrapper'>
wsgi.input	
<django.core.handlers.wsgi.LimitedStream object at 0x111e4e6d0>
wsgi.multiprocess	
False
wsgi.multithread	
True
wsgi.run_once	
False
wsgi.url_scheme	
'http'
wsgi.version	
(1, 0)
Settings
Using settings module ddsc_web.settings.dev
Setting	Value
ABSOLUTE_URL_OVERRIDES	
{}
ADMINS	
[('DDSC Maintainer', 'maintainer.ddsc.io@gmail.com')]
ALLOWED_HOSTS	
['*']
APPEND_SLASH	
True
AUTHENTICATION_BACKENDS	
['django.contrib.auth.backends.ModelBackend']
AUTH_PASSWORD_VALIDATORS	
'********************'
AUTH_USER_MODEL	
'users.User'
AWS_ACCESS_KEY_ID	
'********************'
AWS_DEFAULT_ACL	
'private'
AWS_LOCATION	
'dev'
AWS_S3_ENDPOINT_URL	
'http://localhost:9000'
AWS_S3_OBJECT_PARAMETERS	
{'CacheControl': 'max-age=86400'}
AWS_SECRET_ACCESS_KEY	
'********************'
AWS_STORAGE_BUCKET_NAME	
'dev'
BASE_DIR	
PosixPath('/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/ddsc_web/ddsc_web')
CACHES	
{'default': {'BACKEND': 'django.core.cache.backends.redis.RedisCache',
             'LOCATION': 'redis://127.0.0.1:6379'}}
CACHE_MIDDLEWARE_ALIAS	
'default'
CACHE_MIDDLEWARE_KEY_PREFIX	
'********************'
CACHE_MIDDLEWARE_SECONDS	
600
CELERY_ACCEPT_CONTENT	
['application/json']
CELERY_BROKER_URL	
'redis://localhost:6379'
CELERY_RESULT_BACKEND	
'redis://localhost:6379'
CELERY_RESULT_SERIALIZER	
'json'
CELERY_TASK_SERIALIZER	
'json'
CELERY_TIMEZONE	
'Europe/Copenhagen'
CONSUME_TICKET_ENDPOINT	
'http://localhost:8000/events/consume/'
CRISPY_TEMPLATE_PACK	
'bootstrap4'
CSRF_COOKIE_AGE	
31449600
CSRF_COOKIE_DOMAIN	
None
CSRF_COOKIE_HTTPONLY	
False
CSRF_COOKIE_MASKED	
False
CSRF_COOKIE_NAME	
'csrftoken'
CSRF_COOKIE_PATH	
'/'
CSRF_COOKIE_SAMESITE	
'Lax'
CSRF_COOKIE_SECURE	
False
CSRF_FAILURE_VIEW	
'django.views.csrf.csrf_failure'
CSRF_HEADER_NAME	
'HTTP_X_CSRFTOKEN'
CSRF_TRUSTED_ORIGINS	
[]
CSRF_USE_SESSIONS	
False
DATABASES	
{'default': {'ATOMIC_REQUESTS': False,
             'AUTOCOMMIT': True,
             'CONN_HEALTH_CHECKS': False,
             'CONN_MAX_AGE': 0,
             'ENGINE': 'django.db.backends.postgresql_psycopg2',
             'HOST': 'localhost',
             'NAME': 'development',
             'OPTIONS': {},
             'PASSWORD': '********************',
             'PORT': '',
             'TEST': {'CHARSET': None,
                      'COLLATION': None,
                      'MIGRATE': True,
                      'MIRROR': None,
                      'NAME': None},
             'TIME_ZONE': None,
             'USER': 'django'}}
DATABASE_ROUTERS	
[]
DATA_UPLOAD_MAX_MEMORY_SIZE	
2621440
DATA_UPLOAD_MAX_NUMBER_FIELDS	
1000
DATETIME_FORMAT	
'N j, Y, P'
DATETIME_INPUT_FORMATS	
['%Y-%m-%d %H:%M:%S',
 '%Y-%m-%d %H:%M:%S.%f',
 '%Y-%m-%d %H:%M',
 '%m/%d/%Y %H:%M:%S',
 '%m/%d/%Y %H:%M:%S.%f',
 '%m/%d/%Y %H:%M',
 '%m/%d/%y %H:%M:%S',
 '%m/%d/%y %H:%M:%S.%f',
 '%m/%d/%y %H:%M']
DATE_FORMAT	
'N j, Y'
DATE_INPUT_FORMATS	
['%Y-%m-%d',
 '%m/%d/%Y',
 '%m/%d/%y',
 '%b %d %Y',
 '%b %d, %Y',
 '%d %b %Y',
 '%d %b, %Y',
 '%B %d %Y',
 '%B %d, %Y',
 '%d %B %Y',
 '%d %B, %Y']
DEBUG	
True
DEBUG_PROPAGATE_EXCEPTIONS	
False
DECIMAL_SEPARATOR	
'.'
DEFAULT_AUTO_FIELD	
'django.db.models.BigAutoField'
DEFAULT_CHARSET	
'utf-8'
DEFAULT_EXCEPTION_REPORTER	
'django.views.debug.ExceptionReporter'
DEFAULT_EXCEPTION_REPORTER_FILTER	
'django.views.debug.SafeExceptionReporterFilter'
DEFAULT_FILE_STORAGE	
'ddsc_web.settings.custom_storages.PublicMediaStorage'
DEFAULT_FROM_EMAIL	
'webmaster@localhost'
DEFAULT_INDEX_TABLESPACE	
''
DEFAULT_TABLESPACE	
''
DISALLOWED_USER_AGENTS	
[]
EMAIL_BACKEND	
'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST	
'smtp.gmail.com'
EMAIL_HOST_PASSWORD	
'********************'
EMAIL_HOST_USER	
None
EMAIL_PORT	
587
EMAIL_SSL_CERTFILE	
None
EMAIL_SSL_KEYFILE	
'********************'
EMAIL_SUBJECT_PREFIX	
'[Django] '
EMAIL_TIMEOUT	
None
EMAIL_USE_LOCALTIME	
False
EMAIL_USE_SSL	
False
EMAIL_USE_TLS	
True
FILE_UPLOAD_DIRECTORY_PERMISSIONS	
None
FILE_UPLOAD_HANDLERS	
['django.core.files.uploadhandler.MemoryFileUploadHandler',
 'django.core.files.uploadhandler.TemporaryFileUploadHandler']
FILE_UPLOAD_MAX_MEMORY_SIZE	
2621440
FILE_UPLOAD_PERMISSIONS	
420
FILE_UPLOAD_TEMP_DIR	
None
FIRST_DAY_OF_WEEK	
0
FIXTURE_DIRS	
[]
FORCE_SCRIPT_NAME	
None
FORMAT_MODULE_PATH	
None
FORM_RENDERER	
'django.forms.renderers.DjangoTemplates'
IGNORABLE_404_URLS	
[]
IMAGE_CROPPING_BACKEND	
'image_cropping.backends.easy_thumbs.EasyThumbnailsBackend'
IMAGE_CROPPING_BACKEND_PARAMS	
{}
IMAGE_CROPPING_JQUERY_URL	
'http://localhost:9000/dev/admin/js/vendor/jquery/jquery.min.js'
IMAGE_CROPPING_SIZE_WARNING	
False
IMAGE_CROPPING_THUMB_SIZE	
(300, 300)
INSTALLED_APPS	
['django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.messages',
 'django.contrib.staticfiles',
 'users.apps.UsersConfig',
 'events.apps.EventsConfig',
 'news.apps.NewsConfig',
 'members.apps.MembersConfig',
 'polls.apps.PollsConfig',
 'stats.apps.StatsConfig',
 'easy_thumbnails',
 'image_cropping',
 'crispy_forms',
 'tinymce',
 'import_export']
INTERNAL_IPS	
[]
LANGUAGES	
(('da', 'Danish'), ('en', 'English'))
LANGUAGES_BIDI	
['he', 'ar', 'ar-dz', 'fa', 'ur']
LANGUAGE_CODE	
'en-us'
LANGUAGE_COOKIE_AGE	
None
LANGUAGE_COOKIE_DOMAIN	
None
LANGUAGE_COOKIE_HTTPONLY	
False
LANGUAGE_COOKIE_NAME	
'django_language'
LANGUAGE_COOKIE_PATH	
'/'
LANGUAGE_COOKIE_SAMESITE	
None
LANGUAGE_COOKIE_SECURE	
False
LOCALE_PATHS	
[PosixPath('/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/ddsc_web/locale')]
LOGGING	
{}
LOGGING_CONFIG	
'logging.config.dictConfig'
LOGIN_REDIRECT_URL	
'/users/dashboard'
LOGIN_URL	
'/users/login'
LOGOUT_REDIRECT_URL	
None
LOGOUT_URL	
'/users/logout'
MAILERLITE_API_KEY	
'********************'
MAILERLITE_API_URL	
'********************'
MANAGERS	
[]
MEDIA_ROOT	
('/Users/mansstormer/Desktop/hackathon '
 'project/ddsc-website-public/ddsc_web/media')
MEDIA_URL	
'/media/'
MESSAGE_STORAGE	
'django.contrib.messages.storage.fallback.FallbackStorage'
MESSAGE_TAGS	
{10: 'alert-info',
 20: 'alert-info',
 25: 'alert-success',
 30: 'alert-warning',
 40: 'alert-danger'}
MIDDLEWARE	
['django.middleware.security.SecurityMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware',
 'django.middleware.clickjacking.XFrameOptionsMiddleware',
 'django.middleware.locale.LocaleMiddleware']
MIGRATION_MODULES	
{}
MONTH_DAY_FORMAT	
'F j'
NUMBER_GROUPING	
0
PASSWORD_HASHERS	
'********************'
PASSWORD_RESET_TIMEOUT	
'********************'
PREPEND_WWW	
False
PRIVATE_FILE_STORAGE	
'ddsc_web.settings.custom_storages.PrivateMediaStorage'
PRIVATE_MEDIA_LOCATION	
'media/private'
PUBLIC_MEDIA_LOCATION	
'media/public'
ROOT_URLCONF	
'ddsc_web.urls'
SALARY_URL	
None
SECRET_KEY	
'********************'
SECRET_KEY_FALLBACKS	
'********************'
SECURE_CONTENT_TYPE_NOSNIFF	
True
SECURE_CROSS_ORIGIN_OPENER_POLICY	
'same-origin'
SECURE_HSTS_INCLUDE_SUBDOMAINS	
False
SECURE_HSTS_PRELOAD	
False
SECURE_HSTS_SECONDS	
0
SECURE_PROXY_SSL_HEADER	
None
SECURE_REDIRECT_EXEMPT	
[]
SECURE_REFERRER_POLICY	
'same-origin'
SECURE_SSL_HOST	
None
SECURE_SSL_REDIRECT	
False
SERVER_EMAIL	
'root@localhost'
SESSION_CACHE_ALIAS	
'default'
SESSION_COOKIE_AGE	
1209600
SESSION_COOKIE_DOMAIN	
None
SESSION_COOKIE_HTTPONLY	
True
SESSION_COOKIE_NAME	
'sessionid'
SESSION_COOKIE_PATH	
'/'
SESSION_COOKIE_SAMESITE	
'Lax'
SESSION_COOKIE_SECURE	
False
SESSION_ENGINE	
'django.contrib.sessions.backends.db'
SESSION_EXPIRE_AT_BROWSER_CLOSE	
False
SESSION_FILE_PATH	
None
SESSION_SAVE_EVERY_REQUEST	
False
SESSION_SERIALIZER	
'django.contrib.sessions.serializers.JSONSerializer'
SETTINGS_MODULE	
'ddsc_web.settings.dev'
SHORT_DATETIME_FORMAT	
'm/d/Y P'
SHORT_DATE_FORMAT	
'm/d/Y'
SIGNING_BACKEND	
'django.core.signing.TimestampSigner'
SILENCED_SYSTEM_CHECKS	
[]
SITE_URL	
'localhost'
SLACK_INVITATION_LINK	
None
STATICFILES_DIRS	
['/Users/mansstormer/Desktop/hackathon '
 'project/ddsc-website-public/ddsc_web/static']
STATICFILES_FINDERS	
['django.contrib.staticfiles.finders.FileSystemFinder',
 'django.contrib.staticfiles.finders.AppDirectoriesFinder']
STATICFILES_LOCATION	
'static'
STATICFILES_STORAGE	
'ddsc_web.settings.custom_storages.StaticStorage'
STATIC_ROOT	
'/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/static_root'
STATIC_URL	
'http://localhost:9000/dev/'
TEMPLATES	
[{'APP_DIRS': True,
  'BACKEND': 'django.template.backends.django.DjangoTemplates',
  'DIRS': [PosixPath('/Users/mansstormer/Desktop/hackathon project/ddsc-website-public/ddsc_web/home')],
  'OPTIONS': {'context_processors': ['django.template.context_processors.debug',
                                     'django.template.context_processors.request',
                                     'django.contrib.auth.context_processors.auth',
                                     'django.contrib.messages.context_processors.messages']}}]
TEST_NON_SERIALIZED_APPS	
[]
TEST_RUNNER	
'django.test.runner.DiscoverRunner'
THOUSAND_SEPARATOR	
','
THUMBNAIL_ALIASES	
{'': {'avatar': {'crop': True, 'size': (35, 35)},
      'edit_profile': {'crop': True, 'size': (100, 100)}}}
THUMBNAIL_DEFAULT_STORAGE	
'ddsc_web.settings.custom_storages.PublicMediaStorage'
THUMBNAIL_PROCESSORS	
('image_cropping.thumbnail_processors.crop_corners',
 'easy_thumbnails.processors.colorspace',
 'easy_thumbnails.processors.autocrop',
 'easy_thumbnails.processors.scale_and_crop',
 'easy_thumbnails.processors.filters',
 'easy_thumbnails.processors.background')
TIME_FORMAT	
'P'
TIME_INPUT_FORMATS	
['%H:%M:%S', '%H:%M:%S.%f', '%H:%M']
TIME_ZONE	
'Europe/Copenhagen'
TINYMCE_DEFAULT_CONFIG	
{'height': 500,
 'menubar': True,
 'plugins': 'advlist,autolink,lists,link,image,charmap,print,preview,anchor,searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,code,help,wordcount',
 'theme': 'silver',
 'toolbar': 'undo redo | formatselect | bold italic backcolor | alignleft '
            'aligncenter alignright alignjustify | bullist numlist outdent '
            'indent | removeformat | help'}
TINYMCE_JS_URL	
'http://localhost:9000/dev/static/tinymce/tinymce.min.js'
USE_DEPRECATED_PYTZ	
False
USE_I18N	
True
USE_L10N	
True
USE_THOUSAND_SEPARATOR	
False
USE_TZ	
True
USE_X_FORWARDED_HOST	
False
USE_X_FORWARDED_PORT	
False
WSGI_APPLICATION	
'ddsc_web.wsgi.application'
X_FRAME_OPTIONS	
'DENY'
YEAR_MONTH_FORMAT	
'F Y'
You’re seeing this error because you have DEBUG = True in your Django settings file. Change that to False, and Django will display a standard page generated by the handler for this status code.