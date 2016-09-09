#! /usr/bin/python

import json ;
import requests ;
import wxacct ;
import wxcore ;

# map: (a)cct (s)ite ID > user-friendly name
map_dict_as = wxacct.map_id_name( 'as' ) ;

# map: (a)cct (i)tem ID > user-friendly name
map_dict_ai = wxacct.map_id_name( 'ai' ) ;

# list: acct [id,name]
al_dict = wxacct.list_acct_site() ;

# request params for list of account items
ai_auth = wxcore.auth()
ai_url  = wxcore.api_url + '/jsonsdk/DataService/getItemSummariesForSite' ;

ai_out_lst = [] ;

for id in al_dict:

    ai_data = { \
        'cobSessionToken'  : ai_auth[0] , \
        'userSessionToken' : ai_auth[1] , \
        'memSiteAccId'     : id
    } ;

    ai_post = requests.post( ai_url , data=ai_data ) ;
    ai_json = json.loads( ai_post.text ) ;

    # debug: spew raw json
    # print ai_post.text ; exit(0) ;

    ai_out_txt = map_dict_as[ str( id ).strip() ] + ' :: ' + str( id ) + '\n' ;

    # walk (totally fucked-up) json tree
    for item in ai_json:

        if 'itemDisplayName' in item:   # some items don't have this which is awesome

            sub_num = len( item[ 'itemData' ][ 'accounts' ] ) ;
            
            # at least 1 sub-account
            if sub_num > 0:

                for i in range( sub_num ):

                    ai_id = str( item[ 'itemData' ][ 'accounts' ][i][ 'accountId' ] ).strip() ;

                    # pref user-friendly 'map' name if available
                    if ai_id in map_dict_ai.keys():
                        ai_nm = map_dict_ai[ ai_id ] ;
                    else:
                        ai_nm = str( item[ 'itemData' ][ 'accounts' ][i][ 'accountDisplayName' ][ 'defaultNormalAccountName' ] ) ;

                    ai_out_txt += '-- ' + ai_id + ': ' + ai_nm + '\n' ;

    # chuck string into list for later sort+print
    ai_out_lst.append( ai_out_txt ) ;

# spew
for ai in sorted( ai_out_lst ): print ai ;

# fin
