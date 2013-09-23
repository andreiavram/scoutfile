from django.core.exceptions import ImproperlyConfigured
from raven.handlers import logging

__author__ = 'andrei'

logger = logging.getLogger(__name__)


class Menu(object):
    name = ""

    def __init__(self, *args, **kwargs):
        pass

    def get_name(self):
        return self.name

class MenuRepository(object):
    def __init__(self, *args, **kwargs):
        self.menus = {}

    def register_menu(self, menu, name = None):
        if name is None:
            name = menu.get_name()

        if name in self.menus:
            raise Exception("Menu name {0} already registered".format(name))
        self.menus[name] = menu
        return self

    def get_menu(self, name):
        if name not in self.menus:
            raise Exception("Menu {0} not registered".format(name))
        return self.menus[name]

    def unregister_menu(self, name):
        try:
            del self.menus[name]
        except Exception, e:
            logger.error("MenuRepository: %e")


menu_repository = MenuRepository()