#!/usr/bin/python3
#
# Title:       Basic Health Check - Zombie (Defunct) Processes
# Description: Also TID 7002724
# Modified:    2024 Jan 31
#
##############################################################################
# Copyright (C) 2024 SUSE LLC
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

import os
import sys
import suse_core2 as core
import suse_base2 as suse

################################################################
# main
################################################################

def main(argv):
    '''main entry point'''
    pat.set_supportconfig_path(argv[1])
    IDX_STATE = 7
    HEADER_LINES = 2
    LIMIT_CRIT = 9
    LIMIT_WARN = 4
    REQUIRED_STATE = 'Z'

    line_count = 0
    state_count = 0
    content = core.get_file_section(pat.get_supportconfig_path('basic-health-check.txt'), '/ps axwwo')

    if len(content) > 0:
        for line in content:
            line_count += 1
            if line_count < HEADER_LINES:
                continue
            else:
                process_data = line.strip().split()
                if REQUIRED_STATE in process_data[IDX_STATE]:
                    state_count += 1

        if state_count > LIMIT_CRIT:
            pat.update_status(core.CRIT, 'Zombie (Defunct) processes: {0}, exceeds {1}'.format(state_count, LIMIT_CRIT))
        elif state_count > LIMIT_WARN:
            pat.update_status(core.WARN, 'Zombie (Defunct) processes: {0}, exceeds {1}'.format(state_count, LIMIT_WARN))
        else:
            pat.update_status(core.SUCC, 'Zombie (Defunct) processes observed: {0}'.format(state_count))
    else:
        pat.update_status(core.ERROR, 'Error: Missing process data')

    pat.print_results()

# Entry point
if __name__ == '__main__':
    pat = suse.SCAPatternGen2('Basic Health', 'SLE', 'Processes')
    pat.set_id(os.path.basename(__file__))
    pat.set_tid('000016919')
    main(sys.argv)

