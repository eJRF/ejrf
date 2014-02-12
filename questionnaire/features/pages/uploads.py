from questionnaire.features.pages.base import PageObject


class UploadDocumentPage(PageObject):
    def __init__(self, browser):
        super(UploadDocumentPage, self).__init__(browser)
        self.url = '/questionnaire/documents/upload/'

    def validate_upload_form(self, data):
        for label, field in data.items():
            self.is_text_present(label)
            assert self.browser.find_by_name(field)


class DeleteDocumentPage(PageObject):
    def __init__(self, browser, document):
        super(DeleteDocumentPage, self).__init__(browser)
        self.url = '/questionnaire/document/%s/delete/' % document.id