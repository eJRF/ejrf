from questionnaire.features.pages.base import PageObject


class CreateSectionPage(PageObject):
    def __init__(self, browser, questionnaire):
        super(CreateSectionPage, self).__init__(browser)
        self.url = '/questionnaire/entry/%s/section/new/' % questionnaire.id

    def verify_current_position_of_section(self, position):
        if self.browser.driver.name == 'internet explorer':
            self.assert_page_html_contains(
                "<option selected=\"selected\" value=\"%s\">%s</option>" % (position, position))
        else:
            self.assert_page_html_contains(
                "<option value=\"%s\" selected=\"selected\">%s</option>" % (position, position))


class CreateSubSectionPage(PageObject):
    def __init__(self, browser, questionnaire, section):
        super(CreateSubSectionPage, self).__init__(browser)
        self.url = '/questionnaire/entry/%s/section/%s/subsection/new/' % (questionnaire.id, section.id)