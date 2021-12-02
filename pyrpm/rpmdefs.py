# -*- coding: utf-8 -*-
# -*- Mode: Python; py-ident-offset: 4 -*-
# vim:ts=4:sw=4:et
'''
rpm definitions

'''

from typing import Any, Dict


RPM_LEAD_MAGIC_NUMBER = b'\xed\xab\xee\xdb'
RPM_HEADER_MAGIC_NUMBER = b'\x8e\xad\xe8'

RPMTAG_MIN_NUMBER = 1000
RPMTAG_MAX_NUMBER = 1146

# signature tags
RPMSIGTAG_SIZE     = 1000
RPMSIGTAG_LEMD5_1  = 1001
RPMSIGTAG_PGP      = 1002
RPMSIGTAG_LEMD5_2  = 1003
RPMSIGTAG_MD5      = 1004
RPMSIGTAG_GPG      = 1005
RPMSIGTAG_PGP5     = 1006


MD5_SIZE = 16  # 16 bytes long
PGP_SIZE = 152  # 152 bytes long


# data types definition
RPM_DATA_TYPE_NULL = 0
RPM_DATA_TYPE_CHAR = 1
RPM_DATA_TYPE_INT8 = 2
RPM_DATA_TYPE_INT16 = 3
RPM_DATA_TYPE_INT32 = 4
RPM_DATA_TYPE_INT64 = 5
RPM_DATA_TYPE_STRING = 6
RPM_DATA_TYPE_BIN = 7
RPM_DATA_TYPE_STRING_ARRAY = 8
RPM_DATA_TYPE_I18NSTRING_TYPE = 9

RPM_DATA_TYPES = (RPM_DATA_TYPE_NULL,
                  RPM_DATA_TYPE_CHAR,
                  RPM_DATA_TYPE_INT8,
                  RPM_DATA_TYPE_INT16,
                  RPM_DATA_TYPE_INT32,
                  RPM_DATA_TYPE_INT64,
                  RPM_DATA_TYPE_STRING,
                  RPM_DATA_TYPE_BIN,
                  RPM_DATA_TYPE_STRING_ARRAY,)

# https://refspecs.linuxbase.org/LSB_3.1.1/LSB-Core-generic/LSB-Core-generic/pkgformat.html
RPMTAG_NAME = 1000
RPMTAG_VERSION = 1001
RPMTAG_RELEASE = 1002
RPMTAG_SUMMARY = 1004
RPMTAG_DESCRIPTION = 1005
RPMTAG_SIZE = 1009
RPMTAG_DISTRIBUTION = 1010
RPMTAG_VENDOR = 1011
RPMTAG_LICENSE = 1014
RPMTAG_PACKAGER = 1015
RPMTAG_GROUP = 1016
RPMTAG_URL = 1020
RPMTAG_OS = 1021
RPMTAG_ARCH = 1022
RPMTAG_SOURCERPM = 1044
RPMTAG_ARCHIVESIZE = 1046
RPMTAG_RPMVERSION = 1064
RPMTAG_COOKIE = 1094
RPMTAG_DISTURL = 1123
RPMTAG_PAYLOADFORMAT = 1124
RPMTAG_PAYLOADCOMPRESSOR = 1125
RPMTAG_PAYLOADFLAGS = 1126


def __get_tags(values: Dict[str, Any]) -> Dict[str, int]:
    out = dict()
    for k, v in values.items():
        if not k.startswith('RPMTAG'):
            continue
        if type(v) == int:
            out[k] = v
    return out

ALL_RPM_TAGS = __get_tags(locals())
RPMTAGS = ALL_RPM_TAGS.values()
VALUES_TO_RPMTAGS = dict([(v, k) for k, v in ALL_RPM_TAGS.items()])
