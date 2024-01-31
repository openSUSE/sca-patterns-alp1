#!/usr/bin/python3
#
# Title:       Basic Health Check - Tainted Kernel
# Description: Checks if the kernel is tainted or not, also TID 3582750
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
import re
import sys
import suse_core2 as core
import suse_base2 as suse

################################################################
# main
################################################################

def main(argv):
    '''main entry point'''
    pat.set_supportconfig_path(argv[1])
    LAST = -1

    tainted = re.compile('Kernel Status.*Tainted')
    content = core.get_file_section(pat.get_supportconfig_path('basic-health-check.txt'), 'Kernel Status.*Tainted')
    taint_str = ''
    this_list = []
    only_external = True
    external = False
    evaluated = False
    if len(content) > 0:
        for line in content:
            if tainted.search(line):
                evaluated = True
                taint_str = ' '.join(line.split())
                if 'Not Tainted' in taint_str:
                    pat.update_status(core.SUCC, 'The Kernel is not Tainted')
                    break
                else:
                    flag_str = taint_str.split(':')[LAST]
                    flags = [*flag_str]
                    for flag in flags:
                        if flag == ' ':
                            continue
                        elif flag != 'X':
                            only_external = False
                        elif flag == 'X':
                            external = True
                    if external:
                        if only_external:
                            pat.update_status(core.SUCC, '{}, but modules are externally supported'.format(taint_str))
                        else:
                            pat.update_status(core.CRIT, taint_str)
        if not evaluated:
            pat.update_status(core.ERROR, 'Error: Taint status not found')
    else:
        pat.update_status(core.ERROR, 'Error: Taint status section not found')

    pat.print_results()

# Entry point
if __name__ == '__main__':
    pat = suse.SCAPatternGen2('Basic Health', 'ALP', 'Kernel')
    pat.set_id(os.path.basename(__file__))
    pat.set_tid('000016321')
    main(sys.argv)

