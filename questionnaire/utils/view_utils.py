from questionnaire.models import Country, Questionnaire

def get_country(request):
    country_id = request.GET.get('country', '')
    if country_id.isdigit():
        return Country.objects.get(id=country_id)
    if request.user.user_profile.country:
        return request.user.user_profile.country
    return None


def get_regions(request):
    country = get_country(request)
    region = request.user.user_profile.region
    if region:
        return [region]
    elif country:
        return country.regions.all()
    return []


def get_questionnaire_status(request):
    statuses = []
    for perm in request.user.get_all_permissions():
        map_get =  Questionnaire.PERMS_STATUS_MAP.get(perm, None)
        if map_get:
            statuses.extend(map_get)
    return set(filter(None, statuses))