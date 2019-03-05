from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class LanguageCounter(models.Model):
    language = models.OneToOneField(
        Language,
        on_delete=models.CASCADE,
        primary_key=True
    )
    total_docs = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '%s - %s' % (self.language.name, str(self.total_docs))


class Doctype(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class DoctypeCounter(models.Model):
    doctype = models.OneToOneField(
        Doctype,
        on_delete=models.CASCADE,
        primary_key=True
    )
    total_docs = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '%s - %s' % (self.doctype.name, str(self.total_docs))


class ConfLevel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ConfLevelCounter(models.Model):
    conf_level = models.OneToOneField(
        ConfLevel,
        on_delete=models.CASCADE,
        primary_key=True
    )
    total_docs = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '%s - %s' % (self.conf_level.name, str(self.total_docs))


class UploadedFile(models.Model):
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    doctype = models.ForeignKey(Doctype, on_delete=models.SET_NULL, null=True)
    conf_level = models.ForeignKey(ConfLevel, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    uploaded_file = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.name
