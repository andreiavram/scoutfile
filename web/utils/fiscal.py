#   coding: utf8
from __future__ import print_function
from __future__ import division
from builtins import range
from past.utils import old_div
__author__ = 'andrei'

import math

singular_translation = {0 : "", 1 : "unu", 2 : "doi", 3 : "trei", 4 : "patru", 5 : "cinci", 6 : u"șase", 7 : u"șapte", 8 : "opt", 9 : u"nouă"}
plural_translation = {0 : "", 1 : "o", 2 : u"două", 3 : "trei", 4 : "patru", 5 : "cinci", 6 : u"șase", 7 : u"șapte", 8 : "opt", 9 : u"nouă"}
decada_doi_translation = {10 : "zece", 11 : "unsprezece", 12 : "doisprezece", 13 : "treisprezece", 14 : "paisprezece", 15 : "cincisprezece", 16 : u"șaisprezece", 17 : u"șaptesprezece", 18 : "optsprezece", 19 : u"nouăsprezece"}
order_translation_singular = ["", "o mie", "un milion", "un miliard"]
order_translation_plural = ["", "mii", "milioane", "miliarde"]

def suta2text(numar, separator = " ", level = 1):
    if numar < 0 or numar > 999 or numar != math.floor(numar):
        raise ValueError(u"Trebuie un numar natural mai mic de 1000")

    text_final = []
    sute = old_div(numar, 100)
    zeci = old_div((numar - 100 * sute), 10)
    unitati = (numar - 100 * sute - 10 * zeci)
    if sute:
        text_final.append(plural_translation.get(sute))
        if sute == 1:
            text_final.append(u"sută")
        else:
            text_final.append(u"sute")
    if zeci:
        #text_final += zeciplus.get(zeci)
        if zeci == 1:
            text_final.append(decada_doi_translation.get(numar - 100 * sute))
        else:
            text_final.append(plural_translation.get(zeci) + "zeci")

    if unitati and zeci != 1:
        if zeci:
            text_final.append(u"și")
        text_final.append(singular_translation.get(unitati))

    return separator.join(text_final)

def numar2text(numar, separator = " "):
    level = 1
    parts = []
    numar = int(numar)
    while numar > 0:
        parts.append(suta2text(numar % 1000, level = level, separator=separator))
        numar /= 1000
        level += 1

    if len(parts) > 4:
        raise ValueError(u"Numerele mai mari de sute de miliarde nu pot fi procesate")

    text_final = []
    for i in range(len(parts)):
        text_local = []
        if i > 0 and parts[i] == "unu":
            text_local.append(order_translation_singular[i])
        else:
            text_local.append(parts[i])
            text_local.append(order_translation_plural[i])

        text_final.append(separator.join(text_local))

    print(text_final)
    return separator.join(reversed(text_final))

def suma2text(suma):
    bani = (suma - math.floor(suma)) * 100
    suma = math.floor(suma)

    text = numar2text(suma) + "lei "
    if bani > 0:
        text += u"și " + numar2text(bani) + "bani"

    return text


if __name__ == "__main__":
    print(suma2text(124123.53))