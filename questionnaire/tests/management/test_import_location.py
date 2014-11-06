import os

from questionnaire.models import Region, Country
from questionnaire.management.commands.import_location import Command
from questionnaire.tests.base_test import BaseTest


class FakeStdout(object):
    def write(self, msg):
        return "haha %s" % msg


class FakeCommand(Command):
    def __init__(self):
        super(FakeCommand, self).__init__()
        self.stdout = FakeStdout()


class ImportLocationTest(BaseTest):
    def setUp(self):
        self.data = [['Region', 'Country' 'ISO'],
                     ['AFRO', 'Uganda', 'UGA'],
                     ['AFRO', 'Kenya', 'KES'],
                     ['PAHO', 'Brazil', 'JGJ'],
                     ['PAHO', 'Mexico', 'THD']]

        self.write_to_csv('wb', self.data)
        self.filename = 'test.csv'
        file = open(self.filename, 'rb')
        self.importer = FakeCommand()

    def tearDown(self):
        os.system("rm -rf %s" % self.filename)

    def test_should_create_regions_and_countries(self):
        self.importer.handle(self.filename, 'UNICEF')
        for locations in self.data[1:]:
            region = Region.objects.filter(name=locations[0], organization__name='UNICEF')
            self.failUnless(region)
            self.failUnless(Country.objects.filter(name=locations[1], regions=region[0], code=locations[-1]))