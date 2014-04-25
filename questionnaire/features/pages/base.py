from lettuce.django import django_url
from nose.tools import assert_equals, assert_true


class PageObject(object):
    url = None

    def __init__(self, browser):
        self.browser = browser

    def visit(self):
        self.browser.visit(django_url(self.url))

    def visit_url(self, url):
        self.browser.visit(django_url(url))

    def validate_url(self):
        assert self.browser.url == django_url(self.url)

    def fill(self, name, value):
        self.browser.fill(name, value)

    def submit(self):
        self.browser.find_by_css("form button").first.click()

    def click_link_by_text(self, text):
        self.browser.click_link_by_text(text)

    def click_by_css(self, css_selector):
        self.browser.find_by_css(css_selector).first.click()

    def click_link_by_partial_href(self, modal_id):
        self.browser.click_link_by_partial_href(modal_id)

    def click_link_by_href(self, modal_id):
        self.browser.click_link_by_href(modal_id)

    def click_by_name(self, name):
        self.browser.find_by_name(name).first.click()

    def _is_text_present(self, text, status=True):
        assert_equals(status, self.browser.is_text_present(text))

    def is_text_present(self, *texts, **kwargs):
        status = kwargs['status'] if 'status' in kwargs else True
        for text in texts:
            self._is_text_present(text, status)

    def is_name_present(self, *names, **kwargs):
        status = kwargs['status'] if 'status' in kwargs else True
        check = []
        for name in names:
            check.append(bool(self.browser.find_by_name(name)))
        assert_equals(status, len(check) == check.count(True))

    def validate_pagination(self):
        self.click_link_by_text('2')

    def fill_form(self, data):
        self.browser.fill_form(data)

    def fill_this_form(self, form_css, data):
        for name, value in data.items():
            the_form_element = self.browser.find_by_css('%s #id_%s' % (form_css, name))
            the_form_element.fill(value)

    def click_by_id(self, id):
        self.browser.find_by_id(id).first.click()

    def number_of_elements(self, element_name):
        return len(self.browser.find_by_name(element_name))

    def check(self, value):
        self.browser.find_by_value(value).first.check()

    def uncheck_by_name(self, value):
        self.browser.find_by_name(value).first.uncheck()

    def select(self, name, value):
        self.browser.select(name, value)

    def is_element_present_by_css(self, css_selector):
        self.browser.is_element_present_by_css(css_selector)

    def input_file(self, filename):
        self.browser.attach_file('path', filename)

    def is_element_present_by_value(self, value):
        assert_true(self.browser.is_element_present_by_value(value))

    def is_element_present_by_id(self, id):
        found = self.browser.find_by_id(id)
        return not len(found) == 0

    def is_element_not_present_by_id(self, id):
        return not self.is_element_present_by_id(id)

    def confirm_delete(self, model):
        self.is_text_present("Confirm Delete", "Are you sure you want to delete this %s?" % model)

    def is_element_with_id_disabled(self, id):
        assert self.browser.find_by_id(id).first['disabled']

    def is_element_with_id_enabled(self, id):
        assert (self.browser.find_by_id(id).first['disabled'], False)

    def find_by_id(self, id, status=True):
        assert_equals(status, self.is_element_present_by_id(id))

    def hover_over_id(self, id):
        element = "document.getElementById('%s')" % id
        ie_hover_script = "var event = document.createEventObject(); %s.fireEvent('onmouseover', event);" % element
        other_hover_script = "var eventObj = document.createEvent('MouseEvents'); " \
                             "eventObj.initMouseEvent('mouseover',true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);" \
                             "%s.dispatchEvent(eventObj);" % element

        if self.browser.driver.name == 'internet explorer':
            self.browser.execute_script(ie_hover_script)
        else:
            self.browser.execute_script(other_hover_script)

    def fill_this_element(self, id, data):
        element = self.browser.find_by_id(id).first
        element.fill(data)

    def move_draggable_id_by_this_number_of_steps(self, draggable_id, steps):
        script = "$.getScript('/static/js/lib/jquery.simulate.drag-sortable.js', function() {$('#%s').simulateDragSortable({move: %s});});" % (draggable_id, steps)
        self.browser.execute_script(script)

    def get_text_of_element_by_id(self, id):
        return self.browser.find_by_id(id).first.text

    def choose_this_value_in_this_select_order_by_this_name(self, value, select_order, name):
        script = "document.getElementsByName('%s')[%s].value = %s" % (name, select_order, value)
        self.browser.execute_script(script)