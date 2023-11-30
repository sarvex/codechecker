# -------------------------------------------------------------------------
#
#  Part of the CodeChecker project, under the Apache License v2.0 with
#  LLVM Exceptions. See LICENSE for license information.
#  SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#
# -------------------------------------------------------------------------
""" JSON output helpers. """

from typing import Dict, List

from codechecker_report_converter.report import Report


def convert(reports: List[Report]) -> Dict:
    """ Convert the given reports to JSON format. """
    version = 1

    json_reports = [report.to_json() for report in reports]
    return {"version": version, "reports": json_reports}
