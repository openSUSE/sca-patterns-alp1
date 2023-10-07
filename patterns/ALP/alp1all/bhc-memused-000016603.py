#!/usr/bin/python3
#
# Title:       Basic Health Check - Free Memory and Disk Swapping
# Description: Check the available memory and disk swapping activity, also TID 7000120
# Modified:    2023 Oct 03
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

import os
import sys
import suse_core2 as core
import suse_base2 as suse

##############################################################################
# Local Function Definitions
##############################################################################

def get_swapping_status():
    '''Returns if the sever is swapping to disk'''
    IDX_SWAP_OUT = 7
    HEADER_LINES = 4

    swap_current = '0'
    swap_previous = '0'
    swap_changes = 0
    current_line = 0
    swapping = 'Unknown'

    file_open = pat.get_supportconfig_path('basic-health-check.txt')
    section = 'vmstat 1 4'
    content = core.get_section_re(file_open, section)

    if len(content) > 0:
        for line in content:
            current_line += 1
            if current_line < HEADER_LINES:
                continue
            else:
                vmstat_data = line.strip().split()
                swap_current = vmstat_data[IDX_SWAP_OUT]
                if swap_current != swap_previous:
                    swap_previous = swap_current
                    swap_changes += 1

        if swap_changes > 0:
            swapping = 'Yes'
        else:
            swapping = 'No'

    return swapping

def get_memory_status():
    IDX_MEM_AVAIL = -1
    IDX_MEM_TOTAL = 1

    mem_values = []
    mem_element = []
    this_mem_total = -1
    this_mem_avail = -1
    this_mem_percent = -1

    file_open = pat.get_supportconfig_path('basic-health-check.txt')
    section = 'free -k'
    content = core.get_section_re(file_open, section)

    if len(content) > 0:
        for line in content:
            if line.startswith("Mem:"):
                    mem_element = line.split()
                    this_mem_total = int(mem_element[IDX_MEM_TOTAL])
                    this_mem_avail = int(mem_element[IDX_MEM_AVAIL])
                    break
        if this_mem_total > 0:
            this_mem_percent = int((this_mem_total - this_mem_avail)*100/this_mem_total)

    mem_values = [this_mem_total, this_mem_avail, this_mem_percent]

    return mem_values

################################################################
# main
################################################################

def main(argv):
    '''main entry point'''
    LIMIT_MEM_CRIT = 90
    LIMIT_MEM_WARN = 85

    try:
        pat.set_supportconfig_path(argv[1])
    except IndexError:
        print('Error: Supportconfig directory not found')
        sys.exit(1)

    swapping_to_disk = get_swapping_status()
    mem_total, mem_avail, mem_percent = get_memory_status()
    if mem_percent < 0:
        pat.update_status(core.ERROR, 'Error: Invalid memory data')
    elif mem_percent >= LIMIT_MEM_CRIT:
        pat.update_status(core.CRIT, 'Memory used {0}%, exceeds {1}% - Swapping: {2}'.format(mem_percent, LIMIT_MEM_CRIT, swapping_to_disk))
    elif mem_percent >= LIMIT_MEM_WARN:
        if swapping_to_disk == "Yes":
            pat.update_status(core.CRIT, 'Memory used {0}%, exceeds {1}% and Swapping: {2}'.format(mem_percent, LIMIT_MEM_WARN, swapping_to_disk))
        else:
            pat.update_status(core.WARN, 'Memory used {0}% - Swapping: {1}'.format(mem_percent, swapping_to_disk))
    else:
        if swapping_to_disk == "Yes":
            pat.update_status(core.WARN, 'Memory used {0}% - Swapping: {1}'.format(mem_percent, swapping_to_disk))
        else:
            pat.update_status(core.SUCC, 'Memory used {0}% - Swapping: {1}'.format(mem_percent, swapping_to_disk))

    pat.print_results()

# Entry point
if __name__ == '__main__':
    pat = suse.SCAPattern('Basic Health', 'ALP', 'Memory')
    pat.set_id(os.path.basename(__file__))
    pat.set_tid('000016603')
    pat.add_solution_link('Video', 'https://youtu.be/yLtX5F7ORJI')
    main(sys.argv)

