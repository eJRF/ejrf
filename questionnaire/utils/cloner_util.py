from questionnaire.models import Section, SubSection, QuestionGroup, Question


def get_query_params(model, fields):
    return dict((field, getattr(model, field)) for field in fields)


def create_copies(objects, region, fields, **kwargs):
    copy_map = {}
    for model in objects:
        kwargs.update(**get_query_params(model, fields))
        copy_map[model] = eval(model.__class__.__name__).objects.create(region=region, **kwargs)
    return copy_map