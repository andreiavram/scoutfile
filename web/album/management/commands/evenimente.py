from django.core.management.base import BaseCommand

from album.models import Eveniment
from utils.oncr_client import ONCRClient


class Command(BaseCommand):
    available_commands = ["sync_oncr_activitati"]

    def handle(self, *args, **options):
        if args[0] not in self.available_commands:
            self.stderr.write(u"Command must be one of %s" % ",".join(self.available_commands))
            return

        getattr(self, args[0])(*args[1:], **options)

    def sync_oncr_activitati(self, *args, **options):
        if len(args) < 1:
            self.stderr.write(u"usage sync_oncr_activitati <year>\n")
            return

        year = int(args[0])

        events = Eveniment.objects.filter(start_date__year=year, oncr_id__isnull=True)
        self.stdout.write(u"Sincronizare ONCR: %d evenimente\n" % events.count())

        oncr_client = ONCRClient()
        oncr_client.do_login()

        if not oncr_client.logged_in:
            self.stderr.write(u"Nu am reusit autentificarea cu ONCR.ro\n")
            return

        category_translation = {
            1: u"Intalnire",
            2: u"Proiect organizat de Centrul Local",
            3: u"Regional & National",
            4: u"International"
        }

        successful_events = 0
        for event in events:
            if event.scor_raportare() < 0:
                continue

            categorie = 2
            if event.tip_eveniment == "intalnire":
                categorie = 1
            if event.international:
                categorie = 4
            elif event.organizator and event.organizator_cercetas:
                categorie = 3

            raport = event.raporteveniment_set.first()
            if raport is None:
                continue

            eveniment_args = {
                "raport_anual_oncr": raport.accept_publicare_raport_national,
                "raport_anual_cl": True,
                "nume": event.nume,
                "categorie": categorie,
                "aventura": raport.aventura,
                "social": raport.social,
                "cultural": raport.cultural,
                "ecologie": raport.ecologie,
                "spiritual": raport.spiritual,
                "fundraising": raport.fundraising,
                "altele": raport.altele,
                "numar_participanti": str(event.total_participanti),
                "descriere": event.descriere,
                "obiective": raport.obiective,
                "grup_tinta": raport.grup_tinta,
                "activitati": raport.activitati,
                "promovare": raport.promovare,
                "parteneri": raport.parteneri,
                "buget": str(raport.buget),
                "beneficiari": raport.alti_beneficiari,
                "data_inceput": event.start_date.date(),
                "data_sfarsit": event.end_date.date(),
                "locatie": event.locatie_text
            }

            photo = event.cover_photo()
            if photo:
                eveniment_args['photo'] = photo.image.url

            oncr_client.add_activitate(**eveniment_args)
            successful_events += 1

        self.stdout.write(u"Terminat sincronizare. %d cu succes, %d erori\n" % (successful_events, events.count() - successful_events))


