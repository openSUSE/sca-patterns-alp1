#!/usr/bin/python3
#
# Title:       Basic Health Check - CPU Utilization
# Description: Also TID 7002713
# Modified:    2023 Oct 10
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
    IDX_CPU_IDLE = 14
    HEADER_LINES = 4
    COUNT = 3
    LIMIT_CRIT = 90
    LIMIT_WARN = 80

    try:
        pat.set_supportconfig_path(argv[1])
    except IndexError:
        print('Error: Supportconfig directory not found')
        sys.exit(1)

    line_count = 0
    cpu_idle_total = -1
    cpu_idle_avg = -1
    cpu_avg = -1
    proc_missing = re.compile("mount.*proc", re.IGNORECASE)
    content = core.get_file_section(pat.get_supportconfig_path('basic-health-check.txt'), 'vmstat 1 4')

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
                cpu_idle_total += int(vmstat_data[IDX_CPU_IDLE])
        cpu_idle_avg = int(cpu_idle_total / COUNT)
        cpu_avg = int(100 - cpu_idle_avg)
        if cpu_avg > LIMIT_CRIT:
            pat.update_status(core.CRIT, 'Average CPU utilization: {0}% exceeds {1}%'.format(cpu_avg, LIMIT_CRIT))
        elif cpu_avg > LIMIT_WARN:
            pat.update_status(core.WARN, 'Average CPU utilization: {0}% exceeds {1}%'.format(cpu_avg, LIMIT_WARN))
        else:
            pat.update_status(core.SUCC, 'Average CPU utilization observed: {0}%'.format(cpu_avg))
    else:
        pat.update_status(core.ERROR, 'Error: Missing vmstat data')

    pat.print_results()

# Entry point
if __name__ == '__main__':
    pat = suse.SCAPatternGen2('Basic Health', 'ALP', 'CPU')
    pat.set_id(os.path.basename(__file__))
    pat.set_tid('000016916')
    main(sys.argv)

