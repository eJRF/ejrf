from questionnaire.models import Country


def get_country(request):
    country_id = request.GET.get('country', None)
    country_ = Country.objects.filter(id=country_id)
    country_ = country_[0] if country_.exists() else None
    return country_ or request.user.user_profile.country
