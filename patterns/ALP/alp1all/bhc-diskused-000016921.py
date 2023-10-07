#!/usr/bin/python3
#
# Title:       Basic Health Check - File System Used Space
# Description: Also TID 7002723
# Modified:    2023 Oct 06
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

def get_cpu_count():
    file_open = pat.get_supportconfig_path('basic-health-check.txt')
    section = 'name'
    content = core.get_section_re(file_open, section)

    cpus = 0
    if len(content) > 0:
        for line in content:
            if line.startswith('processor'):
                cpus += 1
    return cpus

################################################################
# main
################################################################

def main(argv):
    '''main entry point'''
    LIMIT_CRIT = 50
    LIMIT_WARN = 30
    try:
        pat.set_supportconfig_path(argv[1])
    except Exception:
        print('Error: Supportconfig directory not found')
        sys.exit(1)

    highest_percent_used = -1
    highest_mount_point = ''
    fs_list = suse.get_filesystem_data(pat)
    for fs in fs_list:
        if fs['is_mounted'] and fs['space_percent_used'] > highest_percent_used:
            highest_percent_used = fs['space_percent_used']
            highest_mount_point = fs['mount_point']

    if highest_percent_used > LIMIT_CRIT:
        pat.update_status(core.CRIT, '{0}% used exceeds {1}% mounted on {2}'.format(highest_percent_used, LIMIT_CRIT, highest_mount_point))
    elif highest_percent_used > LIMIT_WARN:
        pat.update_status(core.WARN, '{0}% used exceeds {1}% mounted on {2}'.format(highest_percent_used, LIMIT_WARN, highest_mount_point))
    else:
        pat.update_status(core.SUCC, 'Mount {0} has the highest percent disk spaced used: {1}%'.format(highest_mount_point, highest_percent_used))

    pat.print_results()

# Entry point
if __name__ == '__main__':
    pat = suse.SCAPattern('Basic Health', 'ALP', 'Disk')
    pat.set_id(os.path.basename(__file__))
    pat.set_tid('000016921')
    pat.add_solution_link('Video', 'https://youtu.be/Vgr8n-J1T3M')
    main(sys.argv)

