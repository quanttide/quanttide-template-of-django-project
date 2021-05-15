"""
Django settings for {{ project_name }} project.

Generated by 'django-admin startproject' using Django {{ django_version }}.

For more information on this file, see
https://docs.djangoproject.com/en/{{ doc_version }}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{ doc_version }}/ref/settings/
"""

import os
import ast

import environ


# ----- Django base directory -----

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ----- django-environ -----
# 当环境变量中不存在ENV变量时，判断为无CloudBase注入环境变量的本地开发环境或本地容器环境
# Warning: 量潮开发者请务必通过CI或者.env文件传入ENV参数，否则设置会被覆盖。

# 本地开发状态时通过django-environ代替CloudBase Framework注入环境变量；
# 根据CloudBase注入默认方式添加`.env`和`.env.local`文件到环境变量，详见：
# https://docs.cloudbase.net/cli-v1/config.html#huan-jing-bian-liang
if 'ENV' not in os.environ:
    for env_file in ['.env', '.env.local']:
        env_file = os.path.join(BASE_DIR, env_file)
        environ.Env.read_env(env_file)


# ----- QuantTide env settings -----

# 部署环境。对不同的环境，分别应用不同的配置。
# 部署环境标签，可选值为开发环境'dev', 预生产环境'pre-prod', 生产环境'prod'
ENV = os.environ.get('ENV', 'dev')
# 是否为生产环境
IS_PROD_ENV = (ENV == 'prod')
# 是否为预生产环境
IS_PRE_PROD_ENV = (ENV == 'pre-prod')
# 是否为生产环境或者预生产环境
IS_DEPLOY_ENV = IS_PROD_ENV or IS_PRE_PROD_ENV
# 是否为开发环境
IS_DEV_ENV = not IS_DEPLOY_ENV


# ----- Django debug settings -----

# Django默认DEBUG设置
# 环境变量不读取时默认为True，预生产和生产环境强制为False
# 一般情况下Django的DEBUG设置等同于我们自定义的IS_DEV_ENV设置，不过有可能在IS_DEV_ENV关闭DEBUG模式方便测试
if IS_DEPLOY_ENV:
    DEBUG = False
elif 'DEBUG' in os.environ:
    # 环境变量读取的值都是字符串格式的，解析字符串格式的布尔值为布尔类型的布尔值
    DEBUG = ast.literal_eval(os.environ['DEBUG'])
else:
    DEBUG = True


# ----- QuantTide settings -----
# 量潮代码风格：基于量潮工程规范的具体配置放在前面，方便后面使用。


# ----- WeChat and QCloud settings -----
# 量潮代码风格：微信和腾讯云密钥等配置放在前面，方便后面使用。


# ----- Django default settings -----
# https://docs.djangoproject.com/en/3.0/ref/settings/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 自建应用
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{{ project_name }}.urls'

WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

# Database
# https://docs.djangoproject.com/en/{{ doc_version }}/ref/settings/#databases
# DEBUG模式使用SQLite做测试数据库，非DEBUG模式使用生产配置数据库（本项目为MySQL）
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Caches
# DEBUG模式下用本地文件做临时缓存，非DEBUG模式下使用生产配置数据库（本项目为Redis）
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': os.path.join(BASE_DIR, 'caches/default'), },
    }

# Password validation
# https://docs.djangoproject.com/en/{{ doc_version }}/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/{{ doc_version }}/topics/i18n/

# Languages
# 默认语言为中文
LANGUAGE_CODE = 'zh-Hans'
USE_I18N = True

# Timezone
# 注意：修改settings中的时区以后，改变的是Django读取数据标记的时区，数据库数据需要调整计算。在生产环境中调整此设置需要特别小心。
USE_L10N = True
USE_TZ = False
TIME_ZONE = 'Asia/Shanghai'  # 北京时间

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/{{ doc_version }}/howto/static-files/

STATIC_URL = '/static/'


# ----- Django REST Framework settings ------

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.AdminRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}