import logging
import os
import warnings
import dataset
from sqlalchemy.exc import SAWarning
from flask import Flask
from dotenv import load_dotenv

from regenesis import default_settings

warnings.filterwarnings('ignore', 'Unicode type received non-unicode bind param value.')
warnings.filterwarnings('ignore', category=SAWarning)

dotenv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
load_dotenv(dotenv_file, verbose=True)

app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar('REGENESIS_SETTINGS', silent=True)

engine = dataset.connect(os.getenv('DATABASE_URL'))

logging.basicConfig(level=logging.INFO)

def get_catalog(catalog_name):
    catalog = app.config.get('CATALOG').get(catalog_name)
    if catalog is None:
        raise ValueError('No such catalog: %s' % catalog_name)
    catalog['name'] = catalog_name
    return catalog
