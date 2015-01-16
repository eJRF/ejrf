from datetime import date

from questionnaire.models import Questionnaire


def _set_year_choices(**kwargs):
    query_set = Questionnaire.objects.filter(status=Questionnaire.PUBLISHED,
                                             children__answers__isnull=False)
    choices = []
    choices.insert(0, ('', 'Choose a year', ))
    questionnaire_years = query_set.values_list('year', flat=True)
    start_year = 2014
    twenty_year_range = [start_year + count for count in range(0, 20)]
    all_years = filter(lambda year: year not in questionnaire_years, twenty_year_range)
    choices.extend((year, year) for year in list(all_years))
    return choices


def _set_is_core(initial, section):
    user = initial.get('user')
    if section.id:
        return section
    elif user and user.user_profile.region:
        section.is_core = False
    else:
        section.is_core = True
    return section