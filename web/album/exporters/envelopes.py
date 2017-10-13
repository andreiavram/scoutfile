# coding: utf-8
import logging
import traceback
from StringIO import StringIO

import reportlab
from django.http import HttpResponse
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus.flowables import PageBreak
from reportlab.platypus.paragraph import Paragraph

from adrese_postale.adrese import AdresaPostala
from album.models import CampArbitrarParticipareEveniment

logger = logging.getLogger(__name__)

__author__ = 'yeti'


class C5Envelopes(object):
    @classmethod
    def generate_envelopes(cls, qs):
        # Define envelope size
        C5_envelope = (22.9 * cm, 16.2 * cm)
        error_count = 0

        #    Font registration and settings
        reportlab.rl_config.warnOnMissingFontGlyphs = 0
        pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuBold', '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif-Bold.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuItalic', '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif-Italic.ttf'))
        pdfmetrics.registerFont(
            TTFont('DejaVuBoldItalic', '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif-BoldItalic.ttf'))

        registerFontFamily('DejaVu', normal='DejaVu', bold='DejaVuBold', italic='DejaVuItalic',
                           boldItalic='DejaVuBoldItalic')

        #    The Story is commonly used in flowing reportlab documents to contain all flowables
        Story = []
        buff = StringIO()

        document_settings = {"rightMargin": 1 * cm,
                             "leftMargin": 12 * cm,
                             "topMargin": 9 * cm,
                             "bottomMargin": 1.5 * cm,
                             "pagesize": C5_envelope}

        doc = SimpleDocTemplate(buff, **document_settings)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', fontName="DejaVu", alignment=TA_JUSTIFY, leading=0.65 * cm))
        styles["Normal"].fontName = "DejaVu"
        styles["Normal"].leading = 0.5 * cm

        qs = list(qs)
        camp_params = dict(
            eveniment=qs[0].eveniment,
            nume="Plic C5 export stats",
            slug="plic_c5_export_stats",
            tip_camp="text",
        )

        camp, _ = CampArbitrarParticipareEveniment.objects.get_or_create(**camp_params)

        error_count = 0
        record = {}

        for participare in qs:
            if participare.membru:
                destinatar = u"%s" % participare.membru
            elif participare.nonmembru:
                destinatar = participare.nonmembru.get_full_name()

            adresa_postala = participare.membru.adresa_postala if participare.membru else participare.nonmembru.adresa_postala

            adresa_internationala = False
            #   verifica adresa internationala
            if participare.membru:
                adresa = participare.membru.get_contact(u"Adresa corespondență", just_value=False)
                adresa = adresa.first()
                if adresa.informatii_suplimentare and any(i in adresa.informatii_suplimentare for i in ["adresa internationala", u"adresă internațională"]):
                    adresa_internationala = True

            try:
                adresa = AdresaPostala.parse_address(adresa_postala, fail_silently=False)
            except Exception, e:
                if not adresa_internationala:
                    logger.error(u"%s: %s (%s)" % (cls.__name__, e, traceback.format_exc()))
                    record[destinatar] = u"Adresă rea (%s)" % e
                    error_count += 1
                else:
                    record[destinatar] = u"OK, international"
                participare.add_to_custom_field(camp.slug, record[destinatar])
                continue

            try:
                if not adresa.are_cod():
                    adresa.determine_cod()
            except Exception, e:
                logger.error("%s: %s (%s)" % (cls.__name__, e, traceback.format_exc()))
                error_count += 1
                record[destinatar] = u"Eroare la Cod Poștal (%s)" % e
                participare.add_to_custom_field(camp.slug, record[destinatar])
                continue

            if not adresa.are_cod():
                error_count += 1
                record[destinatar] = u"Codul Poștal nu a putut fi determinat"
                participare.add_to_custom_field(camp.slug, record[destinatar])
                continue

            record[destinatar] = u"OK"
            participare.add_to_custom_field(camp.slug, record[destinatar])

            cod_postal = adresa.cod
            judet = adresa.judet
            localitate = adresa.localitate if not adresa.is_adresa_sat() else adresa.localitate + ", " + adresa.comuna
            adresa_strada = adresa.__unicode__(short=True)

            Story.append(Paragraph(u"<b>Destinatar:</b>", styles['Justify']))
            Story.append(Paragraph(u"<b>%s</b>" % destinatar, styles['Justify']))
            Story.append(Paragraph(u"%s" % adresa_strada, styles['Justify']))

            if localitate:
                linie_localitate = u"{0}".format(localitate)
                if cod_postal:
                    linie_localitate = u"{0}, ".format(cod_postal) + linie_localitate
                Story.append(Paragraph(linie_localitate, styles['Justify']))
                Story.append(Paragraph(u"Județ %s" % judet, styles['Justify']))
            Story.append(PageBreak())

        raport = u"<b>Total participanti: </b> %d<br /><b>Total erori:</b> %d<br /><b>Total OK:</b> %d<br />" % (len(qs), error_count, len(qs) - error_count)
        Story.append(Paragraph(raport, styles['Justify']))
        Story.append(PageBreak())

        doc.build(Story)

        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename="export_C5.pdf"'

        pdf = buff.getvalue()
        buff.close()
        response.write(pdf)
        return response