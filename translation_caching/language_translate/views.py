from language_translate.models import Language as l
from rest_framework.views import APIView, status
from rest_framework.response import Response
import json
from .tasks import push_to_cache
from language_translate.serializers import LanguageSerializer
from rest_framework import viewsets
from language_translate.models import Language
from language_translate.core.CachingStratergy import CachingContext
from language_translate.core.CachingStratergy import RedisCacheStrategy
from language_translate.core.TranslateStrategy import GoogleTranslate
from language_translate.core.TranslateStrategy import TranslateContext


class TranslateView(APIView):

    def post(self, request,format=None):
        request_body = json.loads(request.body)
        text_to_translate = request_body.get('text')
        to_l = request_body.get('to_language')
        if to_l is None:
            response_data = {"msg" : "Language to convert nor provided"}
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                to_lang = l.objects.get(label=to_l)
            except Exception as e:
                response_data = {
                    "msg": "Language translation not supported. Please check the list of languages supported"
                }
                return Response(status=status.HTTP_400_BAD_REQUEST,data=response_data)
        if text_to_translate is None:
            response_data = {"msg": "Text to translate not provided"}
            return Response(status=status.HTTP_400_BAD_REQUEST,data=response_data)
        caching_redis = RedisCacheStrategy()
        context = CachingContext(caching_redis)
        translated = context.get_value(text_to_translate, to_l)
        if translated is None:
            google_translate = GoogleTranslate()
            translate_context = TranslateContext(google_translate)
            translated = translate_context.get_translation(to_l, text_to_translate)["translatedText"]
            push_to_cache.delay(text_to_translate, to_l, translated)
        response_data = {
            "original_text": text_to_translate,
            "translated_text": translated
        }
        return Response(
            status=status.HTTP_200_OK,
            data=response_data
        )


class LanguageViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Language.objects.all()
        serializer = LanguageSerializer(queryset, many=True)
        return Response(serializer.data)