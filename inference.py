class Preprocessing:
    def __init__(self, project_id, glossary_id, source_language_code, target_language_code):
        self.project_id = project_id
        self.glossary_id = glossary_id
        self.source_language_code = source_language_code
        self.target_language_code = target_language_code

    def common_preprocess(self, text):
        client = translate.TranslationServiceClient()
        location = "us-central1"
        parent = f"projects/{}/locations/{location}"
        model = 'projects/218254067973/locations/us-central1/models/NM44251c86bb449264'

        glossary = client.glossary_path(self.project_id, "us-central1", self.glossary_id)

        glossary_config = translate.TranslateTextGlossaryConfig(glossary=glossary)

        if isinstance(text, list):
            out = []
            print('Inside list method')
            for line in text:
                response = client.translate_text(
                    request={
                        "contents": [line if len(line) > 1 else " "],
                        "target_language_code": self.target_language_code,
                        "source_language_code": self.source_language_code,
                        "parent": parent,
                        # "model": model,
                        # "glossary_config": glossary_config,
                    }
                )
                out.append(response.translations[0].translated_text)

            resp = "\n".join(out)

        else:
            print('Inside str method')
            response = client.translate_text(
                request={
                    "contents": [text],
                    "target_language_code": self.target_language_code,
                    "source_language_code": self.source_language_code,
                    "parent": parent,
                    # "model": model,
                    # "glossary_config": glossary_config,
                }
            )
            resp = response.translations[0].translated_text

        return resp


class Translate:
    def __init__(self, project_id, glossary_id, source_language_code, target_language_code):
        self.preprocessor = Preprocessing(project_id, glossary_id, source_language_code, target_language_code)

    def default_translate_text(self, text):
        """
        Translate text using the default translation function.

        Args:
            text: The text to translate.

        Returns:
            str: The translated text.
        """
        return self.preprocessor.common_preprocess(text)

    def glossary_translate_text(self, text):
        """
        Translate text using the glossary translation function.

        Args:
            text: The text to translate.

        Returns:
            str: The translated text.
        """
        return self.preprocessor.common_preprocess(text)

project_id = "218254067973"
glossary_id = "glossary-id"
source_language_code = "en"
target_language_code = "hi"

preprocessor = Preprocessing(project_id, glossary_id, source_language_code, target_language_code)

translator = Translate(preprocessor)

default_translation_result = translator.default_translate_text("Many years back, Parvathi P from Bengaluru, then a young woman in her 20s, struggled even to breathe. She was diagnosed with asthma. Fast forward 32 years.  \
                         At 54, Parvathi goes on treks easily with her daughter and friends who are about half her age.")
glossary_translation_result = translator.glossary_translate_text("Many years back, Parvathi P from Bengaluru, then a young woman in her 20s, struggled even to breathe. She was diagnosed with asthma. Fast forward 32 years.  \
                         At 54, Parvathi goes on treks easily with her daughter and friends who are about half her age.")

print(default_translation_result)
print(glossary_translation_result)







