#! /usr/bin/python

import json ;
import requests ;
import wxcore ;

# +---------------------+
# | account :: list IDs |
# +---------------------+

def list():

    la_auth = wxcore.auth() ;
    la_data = { 'cobSessionToken' : la_auth[0] , 'userSessionToken' : la_auth[1] } ;
    la_url  = wxcore.api_url + '/jsonsdk/SiteAccountManagement/getAllSiteAccounts' ;
    la_post = requests.post( la_url , data=la_data ) ;
    la_json = json.loads( la_post.text ) ;

    # debug: print raw account listing
    # print la_post.text.encode( 'utf-8' ) ;

    la_dict = {} ;

    for acct in la_json:
        la_dict.update( { acct[ 'siteAccountId' ] : acct[ 'siteInfo' ][ 'defaultDisplayName' ] } ) ;

    # payload
    return la_dict ;

# fin
