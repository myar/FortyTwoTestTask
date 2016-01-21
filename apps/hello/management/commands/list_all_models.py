from django.core.management.base import BaseCommand
from django.db import models


class Command(BaseCommand):
    help = 'Show list all models and count objects'

    def handle(self, *args, **options):
        for model in models.get_models():
            out_str = u'Model %s has - %d objects.\n' % (model.__name__,
                                                         model.objects.count())
            self.stdout.write(out_str)
            self.stderr.write('error: %s' % out_str)
