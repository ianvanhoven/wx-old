#! /usr/bin/python

import wxacct ;

# map: (a)cct (s)ite ID > user-friendly name
as_map_dict = wxacct.map_id_name( 'as' ) ;

# list: acct [id,name]
as_list_dict = wxacct.list_acct_site() ;

as_list_out = '\nList of "account site" IDs and names...\n\n' ;

for id in sorted( as_list_dict ):
    as_list_out += \
        str( id ).strip() + \
        ' :: ' + \
        as_map_dict[ str( id ).strip() ] + \
        '\n' ;

# spew
print as_list_out ;

# fin
