import json
from fileserver.models import (
    Language, LanguageCounter,
    Doctype, DoctypeCounter,
    ConfLevel, ConfLevelCounter,
)

with open('data/language_labels.json') as f:
    language_labels = json.load(f)

with open('data/language_data.json') as f:
    language_data = json.load(f)

with open('data/doctype_labels.json') as f:
    doctype_labels = json.load(f)

with open('data/doctype_data.json') as f:
    doctype_data = json.load(f)

with open('data/confidentiality_labels.json') as f:
    confidentiality_labels = json.load(f)

with open('data/confidentiality_data.json') as f:
    confidentiality_data = json.load(f)

for label in language_labels:
    lang = Language(name=label['name'], short_name=label['shortName'])
    lang.save()
    LanguageCounter(language=lang).save()

for data in language_data:
    for lang in LanguageCounter.objects.all():
        if lang.language.name == data['name']:
            lang.total_docs = data['total_docs']
            lang.save()

for label in doctype_labels:
    Doctype(name=label['name']).save()

for data in doctype_data:
    doc = Doctype.objects.get(name__iexact=data['name'])
    DoctypeCounter(doctype=doc, total_docs=data['total_docs']).save()

for label in confidentiality_labels:
    ConfLevel(name=label['name']).save()

for data in confidentiality_data:
    conf = ConfLevel.objects.get(name__iexact=data['name'])
    ConfLevelCounter(conf_level=conf, total_docs=data['total_docs']).save()
