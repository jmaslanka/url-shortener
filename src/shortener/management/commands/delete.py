from django.core.management.base import BaseCommand
from django.utils.six.moves import input

from shortener.models import GrivURL


class Command(BaseCommand):
    """
    Command used to delete active/inactive records of URLs.
    """
    help = 'Deletes inactive shortcodes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--full',
            action='store_true',
            dest='full',
            default=False,
            help='Delete all shortcodes, even active ones',
        )

    def handle(self, *args, **options):
        if options['full']:
            qs = GrivURL.objects.all()
            quantity = len(qs)
            result = input(
                'You are about to delete all {} shortcodes. '
                'Type yes to confirm: '.format(len(qs))
            )
            if result.lower() == 'yes':
                qs.delete()
                if not GrivURL.objects.all().exists():
                    self.stdout.write(self.style.SUCCESS(
                        'Successfully deleted {} records.'.format(quantity)
                    ))
                else:
                    self.stdout.write(self.style.ERROR(
                        'Command unsuccessful. Not all records were deleted.'
                    ))
        else:
            qs = GrivURL.objects.filter(active=False)
            quantity = len(qs)
            result = input(
                'You are about to delete {} inactive shortcodes. '
                'Type yes to confirm: '.format(quantity)
            )
            if result.lower() == 'yes':
                qs.delete()
                if not GrivURL.objects.filter(active=False).exists():
                    self.stdout.write(self.style.SUCCESS(
                        'Successfully deleted {} records.'.format(quantity)
                    ))
                else:
                    self.stdout.write(self.style.ERROR(
                        'Command unsuccessful. Not all records were deleted.'
                    ))
