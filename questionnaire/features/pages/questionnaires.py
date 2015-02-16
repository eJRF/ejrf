from questionnaire.features.pages.base import PageObject
from nose.tools import assert_true, assert_equals, assert_in


class QuestionnairePage(PageObject):
    def __init__(self, browser, section):
        super(QuestionnairePage, self).__init__(browser)
        self.questionnaire = section.questionnaire
        self.section = section
        self.url = "/questionnaire/entry/%s/section/%s/" % (self.questionnaire.id, self.section.id)

    def validate_fields(self):
        assert self.browser.find_by_name("Number-0-response")
        assert self.browser.find_by_name("Number-1-response")
        assert self.browser.find_by_name("MultiChoice-0-response")
        assert self.browser.is_element_present_by_id('cancel_button')
        assert self.browser.is_element_present_by_id('save_draft_button')
        assert self.browser.is_element_present_by_id('submit_questionnaire_btn')

    def validate_instructions(self, question):
        self.click_by_css("#question-%d-instructions" % question.id)
        self.is_text_present(question.instructions)

    def validate_alert_success(self):
        self.is_text_present("Draft saved.")
        self.is_element_present_by_css(".alert-success")

    def validate_alert_error(self):
        self.is_text_present("Draft NOT saved. See errors below")
        self.is_element_present_by_css(".alert-danger")

    def validate_responses(self, data):
        data_keys = data.keys()
        numerical = filter(lambda key_: 'Number' in key_, data_keys)
        text = filter(lambda key_: 'Text' in key_, data_keys)
        for key in numerical:
            assert_true(self.browser.find_by_name(key).first.value in data.values())
        for key in text:
            assert_true(self.browser.find_by_name(key).first.value in data.values())

    def validate_fields_disabled(self, data):
        for key in data:
            self.is_element_with_id_disabled('id_%s' % key)

    def validate_fields_enabled(self, data):
        for key in data:
            self.is_element_with_id_enabled('id_%s' % key)

    def validate_add_new_section_exists(self):
        self._is_text_present('New Section')
        assert self.is_element_present_by_id('new-section')

    def validate_updated_numbering(self, question, question_number):
        assert self.get_text_of_element_by_id('label-question-%s' % question.id) == '%s%s' % (question_number, question.text)

    def validate_check_box_ischecked_by_id(self, element_id):
        script = '$($("#%s")[0]).is(":checked")' % element_id
        assert_true(self.browser.evaluate_script(script))

    def validate_numbering_of_subsection(self, subsection_numbering, subsection):
        subsection_title_with_numbering = "%s %s" % (subsection_numbering, subsection.title)
        subsection_element_id = "subsection-%s-content" % subsection.id
        self.is_text_present_in_element_by_id(subsection_title_with_numbering, subsection_element_id)

    def assert_questions_ordered_in_entry(self, questions_in_order, group):
        grid_table = self.browser.find_by_id('grid-table-%s' % group.id)
        table_headers = grid_table.find_by_css('th')
        for index, header in enumerate(table_headers[2:]):
            assert_equals(header.text, questions_in_order[index].text)

    def assert_questions_ordered_in_hybrid_grid_entry(self, questions_in_order, group):
        grid_table = self.browser.find_by_css('.hybrid-group-%s' % group.id)
        question_text_divs = grid_table.find_by_css('.question-text')
        question_text = [element.text for element in question_text_divs]
        for index, elem in enumerate(question_text):
            assert_equals(elem, questions_in_order[index].text)

    def assert_questions_ordered_in_edit_modal(self, questions_in_order):
        for index, question in enumerate(questions_in_order):
            selected = self.browser.find_by_id('column-%d' % index)
            assert_equals(selected.value, str(question.id))