import logging
import os

log = logging.getLogger(__name__)

from pylons import config
import ckan.plugins.toolkit as tk
from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurable, IMiddleware, IConfigurer, ITemplateHelpers

from ckanext.wordpresser.middleware import WordpresserMiddleware


class WordpresserException(Exception): pass


class Wordpresser(SingletonPlugin):
    implements(IConfigurable, inherit=True)
    implements(IConfigurer, inherit=True)
    implements(IMiddleware, inherit=True)
    implements(ITemplateHelpers)

    def configure(self, config):
        self.config = config
        log.info("Loading Wordpresser extension")
        if not 'wordpresser.proxy_host' in config:
            msg = "Must have 'wordpresser.proxy_host in config"
            raise WordpresserException(msg)

    def update_config(self, config):
        tk.add_template_directory(config, 'templates')


    def make_middleware(self, app, config):
        return WordpresserMiddleware(app)

    def get_helpers(self):
        return {
                'get_content': WordpresserMiddleware.get_wordpress_content,
                'get_relevant': WordpresserMiddleware.replace_relevant_bits,
        }
