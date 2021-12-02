# -*- coding: utf-8 -*-
# -*- Mode: Python; py-ident-offset: 4 -*-
# vim:ts=4:sw=4:et
'''
High level pyrpm tests

'''

import unittest

from pyrpm import RPM, rpmdefs

class RPMTest(unittest.TestCase):

    def setUp(self):
        with open('tests/fakeroot-1.26-4.el7.x86_64.rpm', 'rb') as f:
             self.rpm = RPM(f)
        self.maxDiff = None

    def test_entries(self):

        description = '''fakeroot runs a command in an environment wherein it appears to have
root privileges for file manipulation. fakeroot works by replacing the
file manipulation library functions (chmod(2), stat(2) etc.) by ones
that simulate the effect the real library functions would have had,
had the user really been root.'''
        self.assertEqual(self.rpm[rpmdefs.RPMTAG_NAME], 'fakeroot')
        self.assertEqual(self.rpm[rpmdefs.RPMTAG_VERSION], '1.26')
        self.assertEqual(self.rpm[rpmdefs.RPMTAG_RELEASE], '4.el7')
        self.assertEqual(self.rpm[rpmdefs.RPMTAG_ARCH], 'x86_64')
        self.assertEqual(self.rpm[rpmdefs.RPMTAG_LICENSE], 'GPLv3+ and LGPLv2+ and (GPL+ or Artistic)')
        self.assertEqual(self.rpm[rpmdefs.RPMTAG_DESCRIPTION], description)
        self.assertGreaterEqual(len(self.rpm.items()), 21)

    def test_package_type(self):
        self.assertEqual(self.rpm.binary, True)
        self.assertEqual(self.rpm.source, False)

    def test_name(self):
        self.assertEqual(self.rpm.name(), 'fakeroot')

    def test_package(self):
        self.assertEqual(self.rpm.package(), 'fakeroot-1.26')

    def test_filename(self):
        self.assertEqual(self.rpm.filename(), 'fakeroot-1.26-4.el7.x86_64.rpm')
