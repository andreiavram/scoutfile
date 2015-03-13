# coding: utf-8
from StringIO import StringIO
from django.http import HttpResponse
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import reportlab
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import PageBreak
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus.paragraph import Paragraph
import traceback
from adrese_postale.adrese import AdresaPostala


import logging
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

        error_count = 0
        record = {}

        for participare in qs:
            if participare.membru:
                destinatar = u"%s" % participare.membru
            elif participare.nonmembru:
                destinatar = participare.nonmembru.get_full_name()

            adresa_postala = participare.membru.adresa_postala if participare.membru else participare.nonmembru.adresa_postala
            try:
                adresa = AdresaPostala.parse_address(adresa_postala, fail_silently=False)
            except Exception, e:
                logger.error("%s: %s (%s)" % (cls.__name__, e, traceback.format_exc()))
                record[destinatar] = u"Adresă rea (%s)" % e
                error_count += 1
                continue

            try:
                if not adresa.are_cod():
                    adresa.determine_cod()
            except Exception, e:
                logger.error("%s: %s (%s)" % (cls.__name__, e, traceback.format_exc()))
                error_count += 1
                record[destinatar] = u"Eroare la Cod Poștal (%s)" % e
                continue

            if not adresa.are_cod():
                error_count += 1
                record[destinatar] = u"Codul Poștal nu a putut fi determinat"
                continue

            record[destinatar] = u"OK"

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