from google.cloud import translate

def get_supported_languages(
    project_id: str = "caramel-galaxy-423217-u2",
) -> list:
    """Getting a list of supported language codes.

    Args:
        project_id: The GCP project ID.

    Returns:
        A list of supported language codes.
    """
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}"

    # Supported language codes: https://cloud.google.com/translate/docs/languages
    response = client.get_supported_languages(parent=parent)

    supported_languages = []

    # Append language codes of supported languages to the list.
    for language in response.languages:
        supported_languages.append(language.language_code)

    print("Supported Languages:", supported_languages)

    return supported_languages

get_supported_languages()
