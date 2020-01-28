#!/usr/bin/env python
# -------------------------------------------------------------------------
#                     The CodeChecker Infrastructure
#   This file is distributed under the University of Illinois Open Source
#   License. See LICENSE.TXT for details.
# -------------------------------------------------------------------------

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from ..plist_converter import PlistConverter


class ClangTidyPlistConverter(PlistConverter):
    """ Warning messages to plist converter. """

    def _get_checker_category(self, checker):
        """ Returns the check's category."""
        parts = checker.split('-')
        return parts[0] if parts else 'unknown'
