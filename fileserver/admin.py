from django.contrib import admin
from .models import (
    UploadedFile,
    Language, LanguageCounter,
    Doctype, DoctypeCounter,
    ConfLevel, ConfLevelCounter,
)

admin.site.register(UploadedFile)
admin.site.register(Language)
admin.site.register(LanguageCounter)
admin.site.register(Doctype)
admin.site.register(DoctypeCounter)
admin.site.register(ConfLevel)
admin.site.register(ConfLevelCounter)
