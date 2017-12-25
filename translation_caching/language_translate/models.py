from django.db import models

# Create your models here.
class Language(models.Model):
    name = models.CharField(max_length=200, unique=True)
    label = models.CharField(max_length=2, unique=True)
    related_name = models.ManyToManyField('self',
                                        symmetrical=False,
                                        related_name='related_to')

    def __str__(self):
        return self.name

    def add_relationship(self, related_language):
        if self.id is not related_language.id:
            relationship, created = Language.related_name.through.objects.get_or_create(
                from_language_id=self.id,
                to_language_id=related_language.id)
            return relationship

    def remove_relationship(self, related_language):
        Language.related_name.through.objects.filter(
            from_language_id=self.id,
            to_language_id=related_language.id).delete()
        return

    def get_related_languages(self):
        return Language.objects.filter(
            id__in=[
                i.to_language_id for i in Language.related_name.through.objects.filter(
                from_language=self
                )
            ]
        ).values_list(
            "label", flat=True
        )

