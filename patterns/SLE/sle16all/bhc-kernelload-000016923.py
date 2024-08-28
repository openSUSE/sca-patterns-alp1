#!/usr/bin/python3

# Title:       Basic Health Check - CPU Load
# Description: Processes Waiting for Run Queue (Kernel Load), also TID 7002722
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

##############################################################################
# Local Function Definitions
##############################################################################

def get_cpu_count():
    content = core.get_file_section(pat.get_supportconfig_path('hardware.txt'), '/proc/cpuinfo')
    cpus = 0
    if len(content) > 0:
        for line in content:
            if line.startswith('processor'):
                cpus += 1
    return cpus

def get_avg_loads():
    IDX_LAST1 = -3
    IDX_LAST5 = -2
    IDX_LAST15 = -1
    IDX_LAST = -1
    content = core.get_file_section(pat.get_supportconfig_path('basic-health-check.txt'), '/uptime')
    cpu_avg = []
    if len(content) > 0:
        for line in content:
            if 'load average' in line.lower():
                num = line.split()
                for value in [num[IDX_LAST1], num[IDX_LAST5], num[IDX_LAST15]]:
                    if( value[IDX_LAST] == ',' ):
                        value = value[:IDX_LAST]
                    value = value.replace(',','.')
                    cpu_avg.append(float(value))
    return cpu_avg

################################################################
# main
################################################################

def main(argv):
    '''main entry point'''
    pat.set_supportconfig_path(argv[1])
    OPTIMAL = 75
    WARNING = 90
    CRITICAL = 110

    cpu_count = get_cpu_count()
    cpu_loads = get_avg_loads()

    if( len(cpu_loads) == 0 ):
        pat.update_status(core.ERROR, 'ERROR: Invalid CPU load calculation, no CPU loads found')
    else:
        cpu_load = round(sum(cpu_loads)/len(cpu_loads), 2)
        cpu_load_percent = int(cpu_load * 100 / cpu_count)

        if( cpu_load_percent <= OPTIMAL ):
            pat.update_status(core.SUCC, '{0}% CPU load within limits, CPUs: {1}, Load Average: {2}'.format(cpu_load_percent, cpu_count, cpu_load))
        elif( cpu_load_percent < WARNING ):
            pat.update_status(core.WARN, '{0}% CPU load is full, CPUs: {1}, Load Average: {2}'.format(cpu_load_percent, cpu_count, cpu_load))
        elif( cpu_load_percent < CRITICAL ):
            pat.update_status(core.WARN, '{0}% CPU load is heavy, CPUs: {1}, Load Average: {2}'.format(cpu_load_percent, cpu_count, cpu_load))
        else:
            pat.update_status(core.CRIT, '{0}% CPU load is excessive, CPUs: {1}, Load Average: {2}'.format(cpu_load_percent, cpu_count, cpu_load))

    pat.print_results()

# Entry point
if __name__ == '__main__':
    pat = suse.SCAPatternGen2('Basic Health', 'ALP', 'Kernel')
    pat.set_id(os.path.basename(__file__))
    pat.set_tid('000016923')
    pat.add_solution_link('Web', 'http://blog.scoutapp.com/articles/2009/07/31/understanding-load-averages')
    pat.add_solution_link('Wikipedia', 'http://en.wikipedia.org/wiki/Load_%28computing%29')
    main(sys.argv)

