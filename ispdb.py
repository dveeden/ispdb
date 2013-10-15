# -*- coding: utf-8 -*-
"""Interface to Mozilla ISP database"""
from version import VERSION

from collections import namedtuple

from lxml import objectify
import requests

__author__ = 'sprt <hellosprt@gmail.com>'
__version__ = VERSION

DATABASE_URL = 'https://autoconfig-live.mozillamessaging.com/autoconfig/v1.1/'

SOCKET_TYPES = {'plain', 'ssl', 'starttls'}

AUTH_METHODS = {'password-cleartext', 'password-encrypted', 'ntlm', 'gssapi',
                'client-ip-address', 'tls-client-cert', 'none'}

SMTP_AUTH_METHODS = AUTH_METHODS | {'smtp-after-pop'}

BASE_FIELDS = ('protocol', 'hostname', 'port', 'socket_type', 'authentication',
               'username')

OUTGOING_FIELDS = BASE_FIELDS + ('restriction',)
INCOMING_FIELDS = BASE_FIELDS

OutgoingConfiguration = namedtuple('OutgoingConfiguration', OUTGOING_FIELDS)
IncomingConfiguration = namedtuple('IncomingConfiguration', INCOMING_FIELDS)
ISPConfiguration = namedtuple('ISPConfiguration', ['smtp', 'pop3', 'imap'])

class ServerError(Exception):
    """Indicates that the database server failed to respond correctly"""
    pass


def _substitute_username(username, email):
    """Use parts of the email address to format the username"""
    local_part, domain = email.split('@', 2)
    username = username.replace('%EMAILADDRESS%', email)
    username = username.replace('%EMAILLOCALPART%', local_part)
    username = username.replace('%EMAILDOMAIN%', domain)
    return username


def _extract_protocol_config(kind, protocol, xml, email):
    """Return the configuration for the specified protocol, or None"""
    tree = xml.find('.//%sServer[@type="%s"]' % (kind, protocol))
    
    if tree is None:
        return None
    
    username = _substitute_username(str(tree.username), email)
    authentication = str(tree.authentication).lower()
    socket_type = str(tree.socketType).lower()
    
    config = dict(protocol=protocol,
                  hostname=str(tree.hostname),
                  port=int(tree.port),
                  socket_type=socket_type,
                  authentication=authentication,
                  username=username)
    
    if kind == 'outgoing':
        try:
            restriction = str(tree.restriction).lower()
        except AttributeError:
            restriction = None
        
        config['restriction'] = restriction
        return OutgoingConfiguration(**config)
    else:
        return IncomingConfiguration(**config)


def get_configuration(email):
    """Return the configuration for the specified email address"""
    _, domain = email.split('@', 2)
    r = requests.get(DATABASE_URL + domain)
    
    try:
        r.raise_for_status()
    except requests.HTTPError:
        raise ServerError('error %d (%s) for domain %s' % (r.status_code,
                                                           r.reason, domain))
    
    xml = objectify.fromstring(r.text)
    
    smtp_config = _extract_protocol_config('outgoing', 'smtp', xml, email)
    pop3_config = _extract_protocol_config('incoming', 'pop3', xml, email)
    imap_config = _extract_protocol_config('incoming', 'imap', xml, email)
    
    return ISPConfiguration(smtp=smtp_config,
                            pop3=pop3_config,
                            imap=imap_config)
