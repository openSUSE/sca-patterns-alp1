#!/usr/bin/python3
#
# Title:       Expired SCC Registrations
# Description: Identify if SCC registrations have expired
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
import datetime
import suse_core2 as core
import suse_base2 as suse

################################################################
# main
################################################################

def main(argv):
    '''main entry point'''
    pat.set_supportconfig_path(argv[1])
    LIMIT_WARN_DAYS = 60

    scc_info = suse.get_scc_info(pat)

    reg_expired = []
    reg_expiring = []
    expire_date_found = False
    today = datetime.datetime.today()
    if( scc_info ):
        for product in scc_info:
            #print "product:    " + str(product)
            expire_date = ''
            expire_str = ''
            if 'expires_at' in product:
                expire_date_found = True
                TMP = product['expires_at'].split()
                del TMP[-1]
                expire_date = TMP[0]
                expire_str = ' '.join(TMP)
                expiration = datetime.datetime.strptime(expire_str, "%Y-%m-%d %H:%M:%S")
                expiration_warning = expiration - datetime.timedelta(days=int(LIMIT_WARN_DAYS))
            if( expire_str ):
                product_str = '{0} {1}: {2}'.format(product['identifier'], product['version'], str(expire_date))
                if( today > expiration ):
                    reg_expired.append(product_str)
                elif( today > expiration_warning ):
                    reg_expiring.append(product_str)

        if( expire_date_found ):
            if( reg_expired ):
                if( reg_expiring ):
                    pat.update_status(core.CRIT, 'Detected expired product registrations: {0}; expiring within {1] days: {2}'.format(
                        ' '.join(reg_expired), LIMIT_WARN_DAYS, ' '.join(reg_expiring))
                    )
                else:
                    pat.update_status(core.CRIT, 'Detected expired product registrations: {0}'.format(' '.join(reg_expired)))
            elif( reg_expiring ):
                    pat.update_status(core.WARN, 'Detected product registrations expiring within {0} days: {1}'.format(
                        LIMIT_WARN_DAYS, ' '.join(reg_expiring)
                    ))
            else:
                pat.update_status(core.SUCC, "No product registrations have or will expire within {0} days.".format(LIMIT_WARN_DAYS))
        else:
            pat.update_status(core.ERROR, "SCC Status: No expiration dates found")
    else:
        pat.update_status(core.ERROR, "SCC Status: Not Found")

    pat.print_results()

# Entry point
if __name__ == '__main__':
    pat = suse.SCAPatternGen2('Basic Health', 'ALP', 'Registration')
    pat.set_id(os.path.basename(__file__))
    pat.add_solution_link('SCC', 'https://scc.suse.com/dashboard', set_primary=True)
    pat.add_solution_link('Renew', 'https://www.suse.com/renewals/')
    pat.add_solution_link('Video', 'https://youtu.be/um4XQFG_nCo')
    main(sys.argv)

