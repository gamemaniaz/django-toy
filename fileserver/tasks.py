from middleware.celery import app
from .models import (
    UploadedFile,
    Language, LanguageCounter,
    Doctype, DoctypeCounter,
    ConfLevel, ConfLevelCounter,
)
from .serializers import (
    FileSerializer,
    LangSZ, LangCountSZ,
    DoctypeSZ, DoctypeCountSZ,
    ConfLevelSZ, ConfLevelCountSZ,
)
from django.db.models import F
from django.http import Http404
from random import randint
import random
from django.db.models.aggregates import Count

# Helper methods

def get_uploaded_file(pk):
    try:
        return UploadedFile.objects.get(pk=pk)
    except UploadedFile.DoesNotExist:
        raise Http404

def get_language(pk):
    try:
        return Language.objects.get(pk=pk)
    except Language.DoesNotExist:
        raise Http404

def get_language_counter(pk):
    try:
        return LanguageCounter.objects.get(pk=pk)
    except LanguageCounter.DoesNotExist:
        raise Http404

def get_doctype(pk):
    try:
        return Doctype.objects.get(pk=pk)
    except Doctype.DoesNotExist:
        raise Http404

def get_doctype_counter(pk):
    try:
        return DoctypeCounter.objects.get(pk=pk)
    except DoctypeCounter.DoesNotExist:
        raise Http404

def get_conf_level(pk):
    try:
        return ConfLevel.objects.get(pk=pk)
    except ConfLevel.DoesNotExist:
        raise Http404

def get_conf_level_counter(pk):
    try:
        return ConfLevelCounter.objects.get(pk=pk)
    except ConfLevelCounter.DoesNotExist:
        raise Http404

# File upload tasks

@app.task
def delete_file(pk):
    f = get_uploaded_file(pk)
    lang_id = f.language.id
    doctype_id = f.doctype.id
    conf_level_id = f.conf_level.id
    LanguageCounter.objects.filter(pk=lang_id).update(total_docs=F('total_docs') - 1)
    DoctypeCounter.objects.filter(pk=doctype_id).update(total_docs=F('total_docs') - 1)
    ConfLevelCounter.objects.filter(pk=conf_level_id).update(total_docs=F('total_docs') - 1)
    f.delete()

# Language tasks

@app.task
def create_language(data):
    sz = LangSZ(data=data)
    if sz.is_valid():
        lang = sz.save()
        LanguageCounter(language=lang).save()

@app.task
def update_language(pk, data):
    lang = get_language(pk)
    sz = LangSZ(lang, data=data)
    if sz.is_valid():
        sz.save()

@app.task
def delete_language(pk):
    lang = get_language(pk)
    lang.delete()

@app.task
def update_language_counter(pk, data):
    lang_counter = get_language_counter(pk)
    data['language'] = pk
    sz = LangCountSZ(lang_counter, data=data)
    if sz.is_valid():
        sz.save()

# Doctype tasks

@app.task
def create_doctype(data):
    sz = DoctypeSZ(data=data)
    if sz.is_valid():
        doctype = sz.save()
        DoctypeCounter(doctype=doctype).save()

@app.task
def update_doctype(pk, data):
    lang = get_doctype(pk)
    sz = DoctypeSZ(lang, data=data)
    if sz.is_valid():
        sz.save()

@app.task
def delete_doctype(pk):
    doctype = get_doctype(pk)
    doctype.delete()

@app.task
def update_doctype_counter(pk, data):
    doctype_counter = get_doctype_counter(pk)
    data['doctype'] = pk
    sz = DoctypeCountSZ(doctype_counter, data=data)
    if sz.is_valid():
        sz.save()

# Conf level tasks

@app.task
def create_conf_level(data):
    sz = ConflevelSZ(data=data)
    if sz.is_valid():
        conf_level = sz.save()
        ConfLevelCounter(conf_level=conf_level).save()

@app.task
def update_conf_level(pk, data):
    conf_level = get_conf_level(pk)
    sz = ConfLevelSZ(conf_level, data=data)
    if sz.is_valid():
        sz.save()

@app.task
def delete_conf_level(pk):
    conf_level = get_conf_level(pk)
    conf_level.delete()

@app.task
def update_conf_level_counter(pk, data):
    conf_level_counter = get_conf_level_counter(pk)
    data['conf_level'] = pk
    sz = ConfLevelCountSZ(conf_level_counter, data=data)
    if sz.is_valid():
        sz.save()

# Periodic tasks

@app.task(name='increment_total_docs')
def increment_docs():
    choice = randint(1,3)
    if choice == 1:
        model = LanguageCounter
    elif choice == 2:
        model = DoctypeCounter
    else:
        model = ConfLevelCounter
    random_items = random.sample(list(model.objects.all()), k=2)
    for item in random_items:
        print('Incrementing:', item)
        model.objects.filter(pk=item).update(total_docs=F('total_docs') + 1)

@app.task(name='count_num_files')
def count_files():
    print('Number of files:', UploadedFile.objects.count())
