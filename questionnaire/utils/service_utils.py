def filter_empty_values(dict_to_clean):
    return dict((key, values) for key, values in dict_to_clean.items() if values)


def export_id(primary_answer):
    if not primary_answer.exists():
        return ''
    primary_answer = primary_answer[0]
    if hasattr(primary_answer.response, 'UID'):
        return '_%s'% primary_answer.response.UID
    return ''


def export_text(primary_answer, grid=True):
    if not primary_answer.exists() or not grid:
        return ''
    return ' | %s' % str(primary_answer[0].format_response())
