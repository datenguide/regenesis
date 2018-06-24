import requests
import re
from lxml import etree
from html import unescape


QUADER = re.compile(r"<quaderDaten>\* (.*)<\/quaderDaten>", re.S | re.M)


def fetch_index(catalog):
    for i in range(10, 100):
        params = [
            ('method', 'DatenKatalog'),
            ('kennung', catalog.get('username')),
            ('passwort', catalog.get('password')),
            ('filter', '%s*' % i),
            ('bereich', 'Alle'),
            ('listenLaenge', '500'),
            ('sprache', 'de')
            ]
        doc = requests.get(catalog.get('index_url'), params=params)
        doc = etree.fromstring(doc.content)
        for entry in doc.findall('.//datenKatalogEintraege/datenKatalogEintraege'):
            yield entry.findtext('./code')


def fetch_cube(catalog, name):
    params = [
        ('method', 'DatenExport'),
        ('kennung', catalog.get('username')),
        ('passwort', catalog.get('password')),
        ('namen', name),
        ('bereich', 'Alle'),
        ('format', 'csv'),
        ('werte', True),
        ('metadaten', True),
        ('zusatz', True),
        ('startjahr', 1900),
        ('endjahr', ''),
        ('zeitscheiben', ''),
        ('inhalte', ''),
        ('regionalmerkmal', ''),
        ('regionalschluessel', ''),
        ('sachmerkmal', ''),
        ('sachschluessel', ''),
        ('sachmerkmal2', ''),
        ('sachschluessel2', ''),
        ('sachmerkmal3', ''),
        ('sachschluessel3', ''),
        ('stand', ''),
        ('sprache', 'de')
        ]
    res = requests.get(catalog.get('export_url'), params=params)
    m = QUADER.search(res.text)
    if m is None:
        print("NO CUBE CONTENT", catalog, name)
        return
    return unescape(m.group(1))
