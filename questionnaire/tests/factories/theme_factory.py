import factory

from questionnaire.models import Theme


class ThemeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Theme

    name = "A title"
    description = 'Description'