#! /usr/bin/python

import requests ;
import wxcore ;

# remove account site
ras_site = raw_input( "\nEnter the memSiteAccId of the account site you wish to remove...\n> " ) ;
ras_auth = wxcore.auth() ;
ras_data = { 'cobSessionToken' : ras_auth[0] , 'userSessionToken' : ras_auth[1] , 'memSiteAccId' : ras_site } ;
ras_url  = wxcore.api_url + '/jsonsdk/SiteAccountManagement/removeSiteAccount' ;
ras_post = requests.post( ras_url , data=ras_data) ;

if ras_post.status_code == 200:
    print "SUCCESS: account site removed" ;
else:
    print "ERROR: Non-200 response code from Account Site Removal API" ;

# fin
