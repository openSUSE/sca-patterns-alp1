#!/usr/bin/python3
#
# Description: Also TID 
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
    try:
        pat.set_supportconfig_path(argv[1])
    except Exception:
        print('Error: Supportconfig directory not found')
        sys.exit(1)


    pat.print_results()

# Entry point
if __name__ == '__main__':
    pat = suse.SCAPatternGen2('Basic Health', 'ALP', 'Kernel')
    pat.set_id(os.path.basename(__file__))
    pat.set_tid('7002722')
    pat.add_solution_link('tag', 'url')
    main(sys.argv)

