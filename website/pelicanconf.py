#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'DETImotic'
SITENAME = u'DETImotic'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Lisbon'

DEFAULT_LANG = u'En'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widget
SOCIAL = (('code ua', 'http://code.ua.pt/projects/pei-2018-2019-g12'),
		  ('Deti', 'https://www.ua.pt/deti/'),
		  ('UA','http://www.ua.pt/'),
		  ('IT', 'https://www.it.pt/ITSites/Index/3'),
		 )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

PLUGINS = ['assets', 'sitemap', 'i18n_subsites']
JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n'],
}
PLUGIN_PATHS = ['../../pelican-plugins/']

# change theme
#THEME = '../../pelican-themes/pelican-bootstrap3/'
THEME = '../../pelican-themes/pelican-blue/'
BOOTSTRAP_THEME = 'cerulean'

DISPLAY_PAGES_ON_MENU = False

FAVICON = 'images/favicon.ico'

CUSTOM_CSS = 'static/css/custom.css'

# Tell Pelican to add files from 'extra' to the output dir
STATIC_PATHS = ['images','extra']

# Tell Pelican to change the path to 'static/custom.css' in the output dir
EXTRA_PATH_METADATA = {
    'extra/custom.css': {'path': 'static/css/custom.css'}
}

ABOUT_ME = "The DETImotic project is related with IoT, M2M and domotics"
BANNER = './images/banner00.png' 
BANNER_ALL_PAGES = True
SHOW_DATE_MODIFIED = False
BOOTSTRAP_FLUID = True


#SITEURL = 'http://xcoa.av.it.pt/~pei2018-2019_g012/docs/'

DISPLAY_PAGES_ON_MENU = True
MENUITEMS = [('Home', 'index.html'),
			 ('Specification','specification.html'),
			 ('Architecture', 'architecture.html'),
			 ('Platform-Documentation', 'platform-documentation.html'),
			 ('Platform-Developers', 'platform-developers.html'),
			 ('Requirements', 'requirements.html'),
	         ('Client', 'client.html'),
	         ('Vision and scenarios', 'vision-and-scenarios.html'),
	         ('Demo', 'demo.html'),
	         ('Logbook', 'logbook.html')
	        ]