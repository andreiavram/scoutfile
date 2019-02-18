from django.core.management.base import BaseCommand
from django.db.models.query_utils import Q

from album.models import Eveniment
from utils.oncr_client import ONCRClient


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('an', nargs='+', type=int)

    def handle(self, *args, **options):
        year = options['an'][0]

        events = Eveniment.objects.filter(start_date__year=year).filter(Q(oncr_id__isnull=True) | Q(oncr_id=""))
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

            participanti = event.participareeveniment_set.exclude(membru__isnull=True)
            participanti_fete = participanti.filter(membru__sex="f")
            participanti_baieti = participanti.filter(membru__sex="m")

            participanti_adulti_fete = sum([1 for i in participanti_fete if i.membru.get_ramura_de_varsta(slug=True, moment=event.start_date) in ['lideri', None]])
            participanti_adulti_baieti = sum([1 for i in participanti_baieti if i.membru.get_ramura_de_varsta(slug=True, moment=event.start_date) in ['lideri', None]])
            participanti_tineri_fete = participanti_fete.count() - participanti_adulti_fete
            participanti_tineri_baieti = participanti_baieti.count() - participanti_adulti_baieti


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
                # "numar_participanti": str(event.total_participanti),
                "numar_participanti": {
                    "fete": participanti_tineri_fete,
                    "baieti": participanti_tineri_baieti,
                    "lideri_femei": participanti_adulti_fete,
                    "lideri_barbati": participanti_adulti_baieti,
                },
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

            self.stdout.write("{}\n".format(eveniment_args))

            photo = event.cover_photo()
            if photo:
                eveniment_args['photo'] = photo.image.url

            result = oncr_client.add_activitate(**eveniment_args)
            if result:
                successful_events += 1
            break

        self.stdout.write(u"Terminat sincronizare. %d cu succes, %d erori\n" % (successful_events, events.count() - successful_events))


