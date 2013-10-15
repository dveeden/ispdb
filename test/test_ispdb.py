# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(1, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import ispdb

from lxml import objectify

from subprocess import Popen, PIPE
from time import sleep
import unittest

def get_data_path(filename=None):
    dirname = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    return os.path.join(dirname, filename or '')


class TestUsernameSubstitution(unittest.TestCase):
    def test_address(self):
        self.assertEqual(
            ispdb._substitute_username('%EMAILADDRESS%', 'john@example.com'),
            'john@example.com')
    
    def test_local_part(self):
        self.assertEqual(
            ispdb._substitute_username('%EMAILLOCALPART%', 'john@example.com'),
            'john')
    
    def test_domain(self):
        self.assertEqual(
            ispdb._substitute_username('pub-%EMAILDOMAIN%', 'john@example.com'),
            'pub-example.com')


class TestProtocolConfigExtraction(unittest.TestCase):
    def setUp(self):
        with open(get_data_path('gmail.com')) as f:
            self.xml = objectify.parse(f)
    
    def test_smtp(self):
        extracted_config = ispdb._extract_protocol_config(
            'outgoing', 'smtp', self.xml, 'johndoe@gmail.com')
        
        config = ispdb.OutgoingConfiguration(
            protocol='smtp',
            hostname='smtp.googlemail.com',
            port=465,
            socket_type='ssl',
            authentication='password-cleartext',
            username='johndoe@gmail.com',
            restriction=None)
        
        self.assertEqual(extracted_config, config)
    
    def test_pop3(self):
        extracted_config = ispdb._extract_protocol_config(
            'incoming', 'pop3', self.xml, 'johndoe@gmail.com')
        
        config = ispdb.IncomingConfiguration(
            protocol='pop3',
            hostname='pop.googlemail.com',
            port=995,
            socket_type='ssl',
            authentication='password-cleartext',
            username='johndoe@gmail.com')
        
        self.assertEqual(extracted_config, config)
    
    def test_imap(self):
        extracted_config = ispdb._extract_protocol_config(
            'incoming', 'imap', self.xml, 'johndoe@gmail.com')
        
        config = ispdb.IncomingConfiguration(
            protocol='imap',
            hostname='imap.googlemail.com',
            port=993,
            socket_type='ssl',
            authentication='password-cleartext',
            username='johndoe@gmail.com')
        
        self.assertEqual(extracted_config, config)


class TestConfigurationFunction(unittest.TestCase):
    def setUp(self):
        module = 'http.server' if sys.version_info >= (3,) else 'SimpleHTTPServer'
        args = [sys.executable, '-m', module, '8000']
        self.proc = Popen(args, stdout=PIPE, stderr=PIPE, cwd=get_data_path())
        sleep(1)
        ispdb.DATABASE_URL = 'http://localhost:8000/'
    
    def tearDown(self):
        self.proc.terminate()
        ispdb.DATABASE_URL = ('https://autoconfig-live.mozillamessaging.com/'
                              'autoconfig/v1.1/')
    
    def test_ok(self):
        config = ispdb.get_configuration('johndoe@gmail.com')
        self.assertIsInstance(config, ispdb.ISPConfiguration)
        self.assertIsInstance(config.smtp, ispdb.OutgoingConfiguration)
        self.assertIsInstance(config.pop3, ispdb.IncomingConfiguration)
        self.assertIsInstance(config.imap, ispdb.IncomingConfiguration)
    
    def test_not_found(self):
        with self.assertRaises(ispdb.ServerError):
            ispdb.get_configuration('johndoe@example.com')

if __name__ == '__main__':
    unittest.main()
