import logging
import os

log = logging.getLogger(__name__)

from pylons import config
import ckan.plugins.toolkit as tk
from ckan.plugins import implements, SingletonPlugin
from ckan.controllers.package import PackageController
from ckan.plugins import IConfigurable, IMiddleware, IConfigurer, ITemplateHelpers, IRoutes

from ckanext.wordpresser.middleware import WordpresserMiddleware


class WordpresserException(Exception): pass


class Wordpresser(SingletonPlugin):
    implements(IConfigurable, inherit=True)
    implements(IConfigurer, inherit=True)
    implements(IMiddleware, inherit=True)
    implements(IRoutes, inherit=True)
    implements(ITemplateHelpers)


    def configure(self, config):
        self.config = config
        log.info("Loading Wordpresser extension")
        if not 'wordpresser.proxy_host' in config:
            msg = "Must have 'wordpresser.proxy_host in config"
            raise WordpresserException(msg)


    def update_config(self, config):
        tk.add_template_directory(config, 'templates')
        tk.add_resource('theme', 'wordpress')
        #tk.add_resource('fanstatic', 'wordpress')  # resource need to be referenced in the template block too


    def make_middleware(self, app, config):
        return WordpresserMiddleware(app)


    def get_helpers(self):
        return {
                'get_content': WordpresserMiddleware.get_wordpress_content,
                'get_relevant': WordpresserMiddleware.replace_relevant_bits,
               }


    def before_map(self, map):
        map.connect('blog', '/blog',
                    controller='ckanext.wordpresser.plugin:BlogController',
                    action='blog')

        return map



class BlogController(PackageController):
    def blog(self):
        tk.redirect_to('/2018')
