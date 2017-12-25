from __future__ import absolute_import

from celery import task
import time
from language_translate.core.CachingStratergy import RedisCacheStrategy, CachingContext
from language_translate.core.TranslateStrategy import GoogleTranslate
from language_translate.core.TranslateStrategy import TranslateContext
from language_translate.models import Language as l


@task(name="push to cache")
def push_to_cache(original_text, to_lang, translated_text):
    caching_redis = RedisCacheStrategy()
    context = CachingContext(caching_redis)
    context.set_value(original_text, translated_text, to_lang)
    z = l.get_related_languages(l.objects.get(label=to_lang))
    for i in z:
        google_translate = GoogleTranslate()
        translate_context = TranslateContext(google_translate)
        print(original_text)
        translated = translate_context.get_translation(i, original_text)
        print(translated)
        context.set_value(original_text, translated['translatedText'], i)

