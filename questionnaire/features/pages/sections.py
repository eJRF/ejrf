from questionnaire.features.pages.base import PageObject


class CreateSectionPage(PageObject):
    def __init__(self, browser, questionnaire):
        super(CreateSectionPage, self).__init__(browser)
        self.url = '/questionnaire/entry/%s/section/new/' % questionnaire.id

    def verify_current_position_of_section(self, position):
        self.assert_page_html_contains("selected=\"selected\">%s<" % position)

class CreateSubSectionPage(PageObject):
    def __init__(self, browser, questionnaire, section):
        super(CreateSubSectionPage, self).__init__(browser)
        self.url = '/questionnaire/entry/%s/section/%s/subsection/new/' % (questionnaire.id, section.id)