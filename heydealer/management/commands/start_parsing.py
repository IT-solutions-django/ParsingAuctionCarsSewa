from django.core.management.base import BaseCommand
from heydealer.utils.parsing import main


class Command(BaseCommand):
    help = 'Загрузка авто с heydealer'

    def handle(self, *args, **kwargs):
        print('Загрузка началась')
        main()
        print('Загрузка завершилась')
