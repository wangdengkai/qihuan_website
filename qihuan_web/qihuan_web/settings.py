"""
Django settings for qihuan_web project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3ho(ji)7b+ud=oq&ac$6q&um&9#z4*l$&v-!2n#z^k*n$-$wu3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'common.apps.CommonConfig',
    'haystack',
    'client.apps.ClientConfig',
    'qihuan.apps.QihuanConfig',

    

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
    
   

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.weixin',
    'allauth.socialaccount.providers.github',

   
]
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'qihuan_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates"),],
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

WSGI_APPLICATION = 'qihuan_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE':'django.db.backends.mysql',
        'NAME':'qihuan_db',
        'USER':'root',
        'PASSWORD':'mysql',
        'HOST':'',
        'PORT':'',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

#设置登录和登出后默认跳转
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFIFLES_DIRS=[os.path.join(BASE_DIR,'static'),]
STATIC_ROOT =os.path.join(BASE_DIR,'collected_static')

HAYSTACK_CONNECTIONS ={
    'default':{
        'ENGINE':'blog.whoosh_cn_backend.WhooshEngine',
        'PATH':os.path.join(BASE_DIR,'whoosh_index'),
    },
}
# 指定如何对搜素结果分页,这里设置为每5项一页
HAYSTACK_SEARCH_RESULTS_PER_PAGE =5
# 设置为么当有文章更新时,就更新索引.
HARSTACK_SIGNAL_PROCESSOR ='haystack.signals.RealtimeSignalProcessor'

#生产环境,设置密码邮箱验证------------------------------------------------

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#  ---------------------------------------------------------
#  Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
 
EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '1017762632@qq.com'
EMAIL_HOST_PASSWORD = 'onnommchvdpzbbae'
DEFAULT_FROM_EMAIL = 'qihaun<1017762632@qq.com>'
#  ---------------------------------------------------------
#  
# django-allauth相关设置
AUTHENTICATION_BACKENDS = (
      # django admin所使用的用户登录与django-allauth无关 
      'django.contrib.auth.backends.ModelBackend',
      # `allauth` specific authentication methods, such as login by e-mail 
      'allauth.account.auth_backends.AuthenticationBackend',
)
# 前面我们app里添加了django.contrib.sites,需要设置
SITE_IDSITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True

