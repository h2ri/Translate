from django.test import TestCase


from language_translate.models import Language as l
from language_translate.core.TranslateStrategy import GoogleTranslate
from language_translate.core.TranslateStrategy import TranslateContext

class TranslationTestCase(TestCase):

    def setUp(self):
        a = l.objects.create(name="Dutch", label="nl")
        b = l.objects.create(name="English", label="en")
        c = l.objects.create(name="French", label="fr")
        d = l.objects.create(name="German", label="de")
        e = l.objects.create(name="Hebrew", label="iw")
        f = l.objects.create(name="Kannada", label="kn")
        a.related_name.add(c)
        c.related_name.add(d)
        c.related_name.add(e)


    def test_translate_available_lang(self):
        to_l = "fr"
        text_to_translate = "Good Morning"
        google_translate = GoogleTranslate()
        translate_context = TranslateContext(google_translate)
        translated = translate_context.get_translation(to_l, text_to_translate)["translatedText"]
        self.assertTrue(translated)
