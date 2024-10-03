#!/usr/bin/python3
#
# Title:       Cron Basic Service Pattern
# Description: Also TID 7014607
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

    package = "chrony"
    service = "chronyd.service"

    if( suse.package_is_installed(package, pat) ):
	    suse.evaluate_systemd_service(service, pat)
    else:
	    pat.set_status(core.ERROR, "Basic Service Health; Package Not Installed: {0}".format(package))

    pat.print_results()

# Entry point
if __name__ == '__main__':
    pat = suse.SCAPatternGen2('Basic Health', 'SLE', 'Chrony')
    pat.set_id(os.path.basename(__file__))
    pat.set_tid('000018283')
    main(sys.argv)

