from questionnaire.features.pages.base import PageObject
import time

class SkipRuleModalPage(PageObject):


    def view_existing_rules(self):
        time.sleep(2)
        self.click_by_id("selectExistingRuleTab")

    def create_new_qn_rule(self):
        self.view_create_new_qn_rules()
        self.browser.find_by_name('root_question')[0].select(1)
        self.browser.find_by_name('response')[0].click()
        self.browser.find_by_name('skip_question')[0].select('2')
        self.browser.find_by_id("save-skip-rule-button")[0].click()
        time.sleep(2)

    def create_new_sub_rule(self):
        self.view_create_new_sub_rules()
        self.browser.find_by_name('skip_subsection')[0].select('2')
        self.browser.find_by_name('subsection_root_question')[0].select('0')
        self.browser.find_by_name('subsection_response')[0].click()
        self.browser.find_by_id("save-subsection-skip-rule-button")[0].click()
        time.sleep(2)

    def view_create_new_qn_rules(self):
        time.sleep(2)
        self.click_by_id("selectNewRuleTab")

    def view_create_new_sub_rules(self):
        time.sleep(2)
        self.click_by_id('selectNewSubsectiongRuleTab')

    def number_of_skip_rules(self):
        element = self.browser.find_by_id("existingRulesTab")[0]
        return len(element.find_by_css(".existingRule"))

    def skip_tab_is_present_for(self, element):
        self.is_text_present("New %s Rule" % element)