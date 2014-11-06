from questionnaire.models import AnswerGroup, Answer
from questionnaire.utils.service_utils import filter_empty_values, export_id, export_text


class ExportToTextService:
    HEADERS = "ISO\tCountry\tYear\tField code\tQuestion text\tValue"

    def __init__(self, questionnaires, version=None, countries=None, themes=None):
        self.questionnaires = questionnaires
        self.version = version
        self.countries = countries
        self.themes = themes

    def get_formatted_responses(self):
        formatted_response = [self.HEADERS]
        for questionnaire in self.questionnaires:
            for subsection in questionnaire.sub_sections():
                subsection_answers = self._answers(subsection)
                formatted_response.extend(subsection_answers)
        return formatted_response

    def _answers(self, subsection):
        formatted_response = []
        section = subsection.section
        for group in subsection.parent_question_groups():
            answers_in_group = self._answers_in(group, section)
            formatted_response.extend(answers_in_group)
        return formatted_response

    def _answer_filter_dict(self, question):
        filter_dict = {'question': question, 'status': Answer.SUBMITTED_STATUS, 'version': self.version,
                       'country__in': self.countries, 'question__theme__in': self.themes}
        return filter_empty_values(filter_dict)

    def _answers_in(self, group, section):
        formatted_response = []
        primary_question = group.primary_question()
        questions = group.all_non_primary_questions() if group.grid else group.ordered_questions()
        answer_groups = AnswerGroup.objects.filter(grouped_question=group)
        for answer_group in answer_groups:
            answers = answer_group.answer.all().select_subclasses()
            primary_answer = self._get_answer_from(primary_question, answers)
            for question in questions:
                answer = self._get_answer_from(question, answers)
                if answer.exists():
                    for answer_ in answer:
                        response_row = self._format_response(answer_, question, primary_question, section,
                                                             primary_answer, group)
                        formatted_response.append(response_row)
        return formatted_response

    def _get_answer_from(self, question, answers):
        filter_dict = self._answer_filter_dict(question)
        return answers.filter(**filter_dict)

    @staticmethod
    def _format_response(answer, question, primary_question, section, primary_answer, group):
        question_prefix = 'C' if question.is_core else 'R'
        primary_answer_id = export_id(primary_answer)
        primary_answer_text = export_text(primary_answer, group.grid)
        answer_id = "%s_%s_%s%s" % (question_prefix, primary_question.UID, question.UID, primary_answer_id)
        question_text_format = "%s | %s%s" % (section.name, question.text, primary_answer_text)
        answer_format = (
        answer.country.code, answer.country.name, answer.questionnaire.year, answer_id.encode('base64').strip(),
        question_text_format, str(answer.format_response()))
        return "%s\t%s\t%s\t%s\t%s\t%s" % answer_format