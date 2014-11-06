import csv

from django.core.management.base import BaseCommand

from questionnaire.models import Country, Region, Organization


class Command(BaseCommand):
    args = 'name_of_the_csv.file organization'
    help = 'Populates locations from a csv file with arguments the name of the csv file followed by the organization (WHO or UNICEF)'

    def handle(self, *args, **kwargs):
        csv_file = csv.reader(open(args[0], "rb"))
        skip_headers = csv_file.next()
        org = Organization.objects.get_or_create(name=args[1])[0] if len(args) > 1 else None
        for locations in csv_file:
            region = Region.objects.get_or_create(name=locations[0], organization=org)[0]
            country = Country.objects.get_or_create(name=locations[1], code=locations[-1])[0]
            country.regions.add(region)
        for_org = ' for %s' % args[1] if len(args) > 1 else ''
        self.stdout.write('Regions and countries successfully imported%s!' % for_org)