####################################
### DICTCONFIG SETUP FOR LOGGING ###
####################################

#TO REMOVE ROTATINING FILE HANDLER ONCE DEV COMPLETE AS CAN CAUSE ISSUE WITH MULTIWORKERS.
#CHECK THAT FILE HANDLER IS APPROPRIATE PRIOR TO PRODUCTION RELEASE.
#CHANGE ROOT LEVEL TO WARNING PRIOR TO RELEASE

import os 
from pathlib import Path

#------------------------------------------------------------#
# Define Base Directory.                                     #
#------------------------------------------------------------#

BASE_DIR = Path(__file__).resolve().parent.parent

#-------------------------------------------------------------#
# Set Secret Key (dev).                                       #
#-------------------------------------------------------------#

SECRET_KEY = "dev"

#-------------------------------------------------------------#
# Define Default Log File (dev)                               #
#-------------------------------------------------------------#

DEBUG = True

ALLOWED_HOSTS = []

#-------------------------------------------------------------#
# Register Installed Apps                                     #
#-------------------------------------------------------------#

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "InfoGene.InfoGeneApp",
]

#-------------------------------------------------------------#
# Set-up Request Processing                                   #
#-------------------------------------------------------------#

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

#-------------------------------------------------------------#
# Set-up URL Entry point                                      #
#-------------------------------------------------------------#

ROOT_URLCONF = "InfoGene.urls"

#-------------------------------------------------------------#
# Set-up Template Loading/Rendering                           #
#-------------------------------------------------------------#

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    }
]

#-------------------------------------------------------------#
# Internal Configuration                                      #
#-------------------------------------------------------------#

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

#-------------------------------------------------------------#
# Static Files                                                #
#-------------------------------------------------------------#

STATIC_URL = "/static/"

#-------------------------------------------------------------#
# Application Logging                                         #
#-------------------------------------------------------------#

home_dir = os.path.expanduser("~")
DEFAULT_LOG = os.path.join(home_dir, ".InfoGene.log")

LOG_FILE = os.path.abspath(os.path.expanduser(DEFAULT_LOG))

log_dir = os.path.dirname(LOG_FILE)
if log_dir:
    os.makedirs(log_dir, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
        
    "formatters": {
        "standard": {
            "format": ("%(asctime)s | %(levelname)s | %(name)s | "
            "%(filename)s:%(lineno)d | %(message)s"
            )
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG" if DEBUG else "INFO",
            "formatter": "standard"
        },

        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": LOG_FILE,
        },
    },

    "loggers": {
        "InfoGene": {
            "level": "DEBUG" if DEBUG else "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },

    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    },
}

#-------------------------------------------------------------#
# Application Data Configuration                              #
#-------------------------------------------------------------#

DATA_DIR = BASE_DIR / "Data"
DATA_FILE = DATA_DIR / "hgnc_complete_set.txt"