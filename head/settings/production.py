from head.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['www.coposto.com', '128.199.198.61', 'coposto.com']

# email settings

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@coposto.com'
EMAIL_HOST_PASSWORD = 'tentechunist'