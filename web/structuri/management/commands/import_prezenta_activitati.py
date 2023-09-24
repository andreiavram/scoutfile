import csv
import datetime
import logging

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.management import CommandError
from django.core.management.base import BaseCommand

from album.models import TipEveniment, StatusEveniment, Eveniment, AsociereEvenimentStructura, ParticipareEveniment, \
    StatusParticipare
from structuri.models import CentruLocal, Unitate, Membru

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('--dryrun', action="store_true")


    def create_event(self, date, dryrun=False):
        centru_local = CentruLocal.objects.get(id=1)
        parsed_date = datetime.datetime.strptime(date, "%d.%m.%Y")
        start_date = datetime.datetime(year=parsed_date.year, month=parsed_date.month, day=parsed_date.day, hour=18, minute=00)
        end_date = datetime.datetime(year=parsed_date.year, month=parsed_date.month, day=parsed_date.day, hour=20, minute=00)
        tip_eveniment = TipEveniment.objects.get(nume="Întâlnire")
        kwargs_create = {
            "centru_local": centru_local,
            "nume": "Întâlnire săptămânală eXplo",
            "start_date": start_date,
            "end_date": end_date,
            "slug": f"meeting-eXplo-{parsed_date.day}-{parsed_date.month}-{parsed_date.year}",
            "tip_eveniment_text": "intalnire",
            "tip_eveniment": tip_eveniment,
            "status": StatusEveniment.FINISHED,
            "locatie_text": "Centrul Cercetășesc Alba Iulia",
        }

        if not dryrun:
            eveniment = Eveniment.objects.create(**kwargs_create)
        else:
            eveniment = Eveniment(**kwargs_create)

        if not dryrun:
            unitate = Unitate.objects.get(nume="Thor")
            content_type = ContentType.objects.get_for_model(unitate)
            object_id = unitate.id
            AsociereEvenimentStructura.objects.create(content_type=content_type, object_id=object_id, eveniment=eveniment)

        return eveniment

    def create_prezenta(self, eveniment, membru, dryrun=False):
        kwargs = {
            "membru": membru,
            "eveniment": eveniment,
            "data_sosire": eveniment.start_date,
            "data_plecare": eveniment.end_date,
            "status_participare": StatusParticipare.COMPLETED_REAL,
            "detalii": "imported from gdrive",
            "user_modificare": User.objects.get(email="andrei.avram@albascout.ro").utilizator.membru
        }

        if not dryrun:
            return ParticipareEveniment.objects.create(**kwargs)
        else:
            return ParticipareEveniment(**kwargs)

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        dryrun = options.get('dryrun', False)
        evenimente = {}
        cnt_prezente = 0
        try:
            with open(csv_file_path) as f:
                csv_reader = csv.reader(f)
                first_line = next(csv_reader)
                id_c = 1
                for event_date in first_line[1:]:
                    eveniment = self.create_event(event_date, dryrun=dryrun)
                    evenimente[id_c] = eveniment
                    id_c += 1
                self.stdout.write(f"Created {len(evenimente.keys())} evenimente!\n")

                for row in csv_reader:
                    try:
                        membru = Membru.objects.get(id=row[0])
                    except Membru.DoesNotExist:
                        self.stdout.write(f"Could not find Membru with id {row[0]}\n")
                        membru = None

                    for id_c, prezenta in enumerate(row[1:], 1):
                        if prezenta.strip() == "1":
                            if membru:
                                self.create_prezenta(evenimente[id_c], membru, dryrun=dryrun)
                            cnt_prezente += 1

        except FileNotFoundError:
                raise CommandError(f'CSV file not found at path: {csv_file_path}')

        self.stdout.write(f"Created {cnt_prezente} prezente!\n")
