from google.cloud import translate
import six
import abc


class TranslateStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def translate_text(self, target, text):
        pass

    @abc.abstractmethod
    def list_languages(self):
        pass


class GoogleTranslate(TranslateStrategy):

    def list_languages(self):
        """Lists all available languages."""
        translate_client = translate.Client()

        results = translate_client.get_languages()

        for language in results:
            print(language['language'])
            print(u'{name} ({language})'.format(**language))
        return results

    def translate_text(self, target, text):
        translate_client = translate.Client()

        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        result = translate_client.translate(
            text, target_language=target)

        return result


class TranslateContext:

    def __init__(self, strategy):
        self.strategy = strategy

    def get_translation(self, target, text):
        print(target)
        print(text)
        return self.strategy.translate_text(target, text)

    def get_languages_supported(self):
        return self.strategy.list_languages()


if __name__ == '__main__':
    google_translate = GoogleTranslate()
    context = TranslateContext(google_translate)
    context.get_languages_supported()
    context.get_translation("fe", "Good Morning")