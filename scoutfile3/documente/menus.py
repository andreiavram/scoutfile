#coding: utf-8
__author__ = 'andrei'

from goodies.menus import ContextMenu


class DecizieContextMenu(ContextMenu):
    def get_menu(self, *args, **kwargs):
        object = kwargs.pop("object", None)

        menu = {"Locații" : [("")]}
        return