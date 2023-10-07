#!/usr/bin/python3
#
# Title:       Basic Health Check - CPU Context switches per second
# Description: Also TID 7002720
# Modified:    2023 Oct 04
#
##############################################################################
# Copyright (C) 2023 SUSE LLC
##############################################################################
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
#  Authors/Contributors:
#   Jason Record <jason.record@suse.com>
#
##############################################################################

##############################################################################
# Module Definition
##############################################################################

import re
import os
import sys
import suse_core2 as core
import suse_base2 as suse

################################################################
# main
################################################################

def main(argv):
    '''main entry point'''
    IDX_CONTEXT_SWITCHES = 11
    CS_COUNT = 3
    HEADER_LINES = 4
    LIMIT_CS_CRIT = 100000
    LIMIT_CS_WARN = 80000

    try:
        pat.set_supportconfig_path(argv[1])
    except IndexError:
        print('Error: Supportconfig directory not found')
        sys.exit(1)

    line_count = 0
    cs_total = 0
    cs_avg = 0
    proc_missing = re.compile("mount.*proc", re.IGNORECASE)
    file_open = pat.get_supportconfig_path('basic-health-check.txt')
    section = 'vmstat 1 4'
    content = core.get_section_re(file_open, section)

    if len(content) > 0:
        for line in content:
            line_count += 1
            if proc_missing.search(line):
                pat.set_status(core.ERROR, 'Error: procfs not mounted')
                break
            elif line_count < HEADER_LINES:
                continue
            else:
                vmstat_data = line.strip().split()
                cs_total += int(vmstat_data[IDX_CONTEXT_SWITCHES])
        cs_avg = int(cs_total / CS_COUNT)
        if cs_avg > LIMIT_CS_CRIT:
            pat.update_status(core.CRIT, 'Average context switches per second: {0} exceeds {1}'.format(cs_avg, LIMIT_CS_CRIT))
        elif cs_avg > LIMIT_CS_WARN:
            pat.update_status(core.WARN, 'Average context switches per second: {0} exceeds {1}'.format(cs_avg, LIMIT_CS_WARN))
        else:
            pat.update_status(core.SUCC, 'Average context switches per second observed: {0}'.format(cs_avg))
    else:
        pat.update_status(core.ERROR, 'Error: Missing vmstat data')

    pat.print_results()

# Entry point
if __name__ == '__main__':
    pat = suse.SCAPattern('Basic Health', 'ALP', 'Kernel')
    pat.set_tid('000016927')
    pat.set_id(os.path.basename(__file__))
    main(sys.argv)

