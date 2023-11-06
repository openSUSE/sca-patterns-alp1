#!/usr/bin/python3
#
# Title:       Pattern for TID000018546
# Description: Check system registration status
# Modified:    2023 Oct 06
# Version:     2.0.0
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

##############################################################################
# Local Function Definitions
##############################################################################

def get_registration_service():
    updates_file = core.get_entire_file(pat.get_supportconfig_path('updates.txt'))
    repos_d_section = core.get_content_section(updates_file, 'zypper --non-interactive --no-gpg-checks repos -d')
    repos_u_section = core.get_content_section(updates_file, 'zypper --non-interactive --no-gpg-checks repos -u')
    del updates_file    

    IDX_NUM = 0
    IDX_ALIAS = 1
    service_tag = ''
    SMT = re.compile("SMT-.*suse", re.IGNORECASE)
    SUSE = re.compile("/updates.suse.com/|/scc.suse.com/", re.IGNORECASE)
    if len(repos_d_section) > 0:
       idx_uri = 8
       for line in repos_d_section:
        parts = line.split('|')
        parts = [x.strip(' ') for x in parts]
        if( parts[IDX_NUM].isdigit() ):
            repo_alias = parts[IDX_ALIAS].strip()
            repo_uri = parts[idx_uri].strip()
            if SUSE.search(parts[idx_uri]):
                service_tag = 'SCC'
            elif( parts[IDX_ALIAS].startswith('susemanager:') ):
                service_tag = 'SUMA'
            elif( parts[IDX_ALIAS].startswith('spacewalk:') ):
                service_tag = 'SUMA'
            elif SMT.search(parts[IDX_ALIAS]):
                service_tag = 'SMT'
    elif len(repos_u_section) > 0:
        idx_uri = 6
        for line in content:
            parts = line.split('|')
            parts = [x.strip(' ') for x in parts]
            if( parts[IDX_NUM].isdigit() ):
                repo_alias = parts[IDX_ALIAS].strip()
                repo_uri = parts[idx_uri].strip()
                if SUSE.search(parts[idx_uri]):
                    service_tag = 'SCC'
                elif( parts[IDX_ALIAS].startswith('susemanager:') ):
                    service_tag = 'SUMA'
                elif( parts[IDX_ALIAS].startswith('spacewalk:') ):
                    service_tag = 'SUMA'
                elif SMT.search(parts[IDX_ALIAS]):
                    service_tag = 'SMT'

    return service_tag

def found_credentials():
    in_state = False
    updates_file = core.get_entire_file(pat.get_supportconfig_path('updates.txt'))
    for line in updates_file:
        if( in_state ):
            if line.startswith('#==['):
                in_state = False
            elif line.startswith('username='):
                return True
        elif line.startswith('# /etc/zypp/credentials.d/'):
            in_state = True

    return False

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

    reg_list = []
    reg_active = []
    reg_noreg = []
    scc_info = suse.get_scc_info(pat)
    reg_service = get_registration_service()
    reg_auth = found_credentials()
    #print(reg_auth)
    if( scc_info ):
        for I in range(len(scc_info)):
            if( scc_info[I]['status'] ):
                if( scc_info[I]['status'].lower() == "registered" ):
                    reg_list.append(scc_info[I]['identifier'])
                elif( scc_info[I]['status'].lower() == "not registered" ):
                    reg_noreg.append(scc_info[I]['identifier'])
                if 'subscription_status' in scc_info[I]:
                    if( scc_info[I]['subscription_status'].lower() == "active" ):
                        reg_active.append(scc_info[I]['identifier'])
    #        print(str(scc_info[I]['identifier']) + ": " + str(scc_info[I]['status']))
    #        print(scc_info[I])
    #    print("\n")
        if( len(reg_active) > 0 ):
            pat.update_status(core.SUCC, "System Registered through " + str(reg_service) + ": " + ' '.join(reg_list))
        elif( len(reg_list) > 0 ):
            if( len(reg_service) > 0 ):
                pat.update_status(core.SUCC, "System Remotely Registered through " + str(reg_service) + ": " + ' '.join(reg_list))
            else:
                pat.update_status(core.SUCC, "System Remotely Registered: " + ' '.join(reg_list))
        elif( len(reg_noreg) > 0 ):
            if( len(reg_service) > 0 ):
                if( reg_auth ):
                    pat.update_status(core.SUCC, "System Remotely Registered through " + str(reg_service) + ": " + ' '.join(reg_noreg))
                else:
                    pat.update_status(core.WARN, "Validate Remote Registration through " + str(reg_service) + ", missing credentials: " + ' '.join(reg_noreg))
            else:
                if( reg_auth ):
                    pat.update_status(core.WARN, "Invalid System Registration, Found credentials but no registration server")
                else:
                    pat.update_status(core.CRIT, "System Not Registered and may be Unsupported")
        else:
            pat.update_status(core.WARN, "Validate System Registration")
    else:
        if( len(reg_service) > 0 ):
            if( reg_auth ):
                pat.update_status(core.SUCC, "System Registered through " + str(reg_service))
            else:
                pat.update_status(core.CRIT, "System Not Registered and may be Unsupported - No Credentials")
        else:
            pat.update_status(core.CRIT, "System Not Registered and may be Unsupported")

    pat.print_results()

# Entry point
if __name__ == '__main__':
    pat = suse.SCAPatternGen2('Basic Health', 'ALP', 'Registration')
    pat.set_id(os.path.basename(__file__))
    pat.set_tid('000018546')
    pat.add_solution_link('SCC', 'https://scc.suse.com/dashboard')
    pat.add_solution_link('Register', 'https://www.suse.com/support/')
    pat.add_solution_link('Video', 'https://youtu.be/um4XQFG_nCo')
    main(sys.argv)

