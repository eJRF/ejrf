from questionnaire.models import Country, Questionnaire, UserProfile

PERMS_STATUS_MAP = {'auth.can_edit_questionnaire': [Questionnaire.PUBLISHED, Questionnaire.DRAFT, Questionnaire.FINALIZED],
                    'auth.can_view_users': [Questionnaire.PUBLISHED, Questionnaire.DRAFT, Questionnaire.FINALIZED],
                    'auth.can_submit_responses': [Questionnaire.PUBLISHED]}


def get_country(request):
    country_id = request.GET.get('country', None)
    country_ = Country.objects.filter(id=country_id)
    country_ = country_[0] if country_.exists() else None
    return country_ or request.user.user_profile.country


def get_regions(request):
    country = get_country(request)
    if country:
        return country.regions.all()


def get_questionnaire_status(request):
    statuses = []
    for perm in request.user.get_all_permissions():
        map_get = PERMS_STATUS_MAP.get(perm, None)
        if map_get:
            statuses.extend(map_get)
    return set(filter(None, statuses))