# -*- coding: utf-8 -*-
import logging

from django.core.management.base import BaseCommand

from wagtail.wagtailcore.models import Site
from wagtailmenus import app_settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Create a 'main menu' for any 'Site' that doesn't already have one. "
        "If main menus for any site do not have menu items, identify the "
        "'home' and 'section root' pages for the site, and menu items linking "
        "to those to the menu. Assumes 'site.root_page' is the 'home page' "
        "and its children are the 'section root' pages")

    def add_arguments(self, parser):
        parser.add_argument(
            '--add-home-links',
            action='store_true',
            dest='add-home-links',
            default=True,
            help="Add menu items for 'home' pages",
        )

    def handle(self, *args, **options):
        for site in Site.objects.all():
            menu = app_settings.MAIN_MENU_MODEL_CLASS.get_for_site(site)
            if not menu.get_menu_items_manager().exists():
                menu.add_menu_items_for_pages(
                    site.root_page.get_descendants(
                        inclusive=options['add-home-links']
                    ).filter(depth__lte=3)
                )
