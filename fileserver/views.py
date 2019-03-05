from django.db.models import F
from django.http import Http404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
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
from .tasks import *


class FileUploadList(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, format=None):
        data = UploadedFile.objects.all()
        sz = FileSerializer(data, many=True)
        return Response(sz.data)

    def post(self, request, format=None):
        lang = Language.objects.get(pk=request.data['language'])
        doctype = Doctype.objects.get(pk=request.data['doctype'])
        conf_level = ConfLevel.objects.get(pk=request.data['conf_level'])
        file = request.data['file']
        file_serializer = FileSerializer(data={
            'name': file.name,
            'language': lang.id,
            'doctype': doctype.id,
            'conf_level': conf_level.id,
            'uploaded_file': file
        })
        if file_serializer.is_valid():
            lang_count = LanguageCounter.objects.filter(pk=lang.id)
            lang_count.update(total_docs=F('total_docs') + 1)
            doctype_count = DoctypeCounter.objects.filter(pk=doctype.id)
            doctype_count.update(total_docs=F('total_docs') + 1)
            conf_level_count = ConfLevelCounter.objects.filter(pk=conf_level.id)
            conf_level_count.update(total_docs=F('total_docs') + 1)
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileUploadDetail(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self, pk):
        try:
            return UploadedFile.objects.get(pk=pk)
        except UploadedFile.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        f = self.get_object(pk)
        data = request.data
        name, lang, doctype, conf_level, file = f.name, f.language, f.doctype, f.conf_level, f.uploaded_file
        if 'language' in data: lang = Language.objects.get(pk=data['language'])
        if 'doctype' in data: doctype = Doctype.objects.get(pk=data['doctype'])
        if 'conf_level' in data: conf_level = ConfLevel.objects.get(pk=data['conf_level'])
        if 'file' in data:
            name = data['file'].name
            file = data['file']
        file_serializer = FileSerializer(f, data={
            'name': name,
            'language': lang.id,
            'doctype': doctype.id,
            'conf_level': conf_level.id,
            'uploaded_file': file
        })
        if file_serializer.is_valid():
            if f.language.id != lang.id:
                LanguageCounter.objects.filter(pk=f.language.id).update(total_docs=F('total_docs') - 1)
                LanguageCounter.objects.filter(pk=lang.id).update(total_docs=F('total_docs') + 1)
            if f.doctype.id != doctype.id:
                DoctypeCounter.objects.filter(pk=f.doctype.id).update(total_docs=F('total_docs') - 1)
                DoctypeCounter.objects.filter(pk=doctype.id).update(total_docs=F('total_docs') + 1)
            if f.conf_level.id != conf_level.id:
                ConfLevelCounter.objects.filter(pk=f.conf_level.id).update(total_docs=F('total_docs') - 1)
                ConfLevelCounter.objects.filter(pk=conf_level.id).update(total_docs=F('total_docs') + 1)
            file_serializer.save()
            return Response(file_serializer.data)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        f = self.get_object(pk)
        sz = FileSerializer(f)
        return Response(sz.data)

    def delete(self, request, pk, format=None):
        delete_file.delay(pk)
        return Response('deleting...')


class LanguageList(APIView):

    def get(self, request, format=None):
        data = Language.objects.all()
        sz = LangSZ(data, many=True)
        return Response(sz.data)

    def post(self, request, format=None):
        create_language.delay(request.data)
        return Response('Creating language and counter...')


class LanguageDetail(APIView):

    def get_object(self, pk):
        try:
            return Language.objects.get(pk=pk)
        except Language.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        sz = LangSZ(data)
        return Response(sz.data)

    def put(self, request, pk, format=None):
        update_language.delay(pk, request.data)
        return Response('Updating language...')

    def delete(self, request, pk, format=None):
        delete_language.delay(pk)
        return Response('Deleting language with counter...')


class LanguageCounterList(APIView):

    def get(self, request, format=None):
        data = LanguageCounter.objects.all()
        sz = LangCountSZ(data, many=True)
        return Response(sz.data)


class LanguageCounterDetail(APIView):

    def put(self, request, pk, format=None):
        update_language_counter.delay(pk, request.data)
        return Response('Updating language counter...')


class DoctypeList(APIView):

    def get(self, request, format=None):
        data = Doctype.objects.all()
        sz = DoctypeSZ(data, many=True)
        return Response(sz.data)

    def post(self, request, format=None):
        create_doctype.delay(request.data)
        return Response('Creating doctype and counter...')


class DoctypeDetail(APIView):

    def get_object(self, pk):
        try:
            return Doctype.objects.get(pk=pk)
        except Doctype.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        sz = DoctypeSZ(data)
        return Response(sz.data)

    def put(self, request, pk, format=None):
        update_doctype.delay(pk, request.data)
        return Response('Updating doctype...')

    def delete(self, request, pk, format=None):
        delete_doctype.delay(pk)
        return Response('Deleting doctype with counter...')


class DoctypeCounterList(APIView):

    def get(self, request, format=None):
        data = DoctypeCounter.objects.all()
        sz = DoctypeCountSZ(data, many=True)
        return Response(sz.data)


class DoctypeCounterDetail(APIView):

    def put(self, request, pk, format=None):
        update_doctype_counter.delay(pk, request.data)
        return Response('Updating doctype counter...')


class ConfLevelList(APIView):

    def get(self, request, format=None):
        data = ConfLevel.objects.all()
        sz = ConfLevelSZ(data, many=True)
        return Response(sz.data)

    def post(self, request, format=None):
        create_conf_level.delay(request.data)
        return Response('Creating conf level and counter...')


class ConfLevelDetail(APIView):

    def get_object(self, pk):
        try:
            return ConfLevel.objects.get(pk=pk)
        except ConfLevel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        sz = ConfLevelSZ(data)
        return Response(sz.data)

    def put(self, request, pk, format=None):
        update_conf_level.delay(pk, request.data)
        return Response('Updating conf level...')

    def delete(self, request, pk, format=None):
        delete_conf_level.delay(pk)
        return Response('Deleting conf level with counter...')


class ConfLevelCounterList(APIView):

    def get(self, request, format=None):
        data = ConfLevelCounter.objects.all()
        sz = ConfLevelCountSZ(data, many=True)
        return Response(sz.data)


class ConfLevelCounterDetail(APIView):

    def put(self, request, pk, format=None):
        update_conf_level_counter.delay(pk, request.data)
        return Response('Updating conf level counter...')
