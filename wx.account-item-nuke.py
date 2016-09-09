#! /usr/bin/python

import requests ;
import wxcore ;

# remove account
rai_item = raw_input( "\nEnter the itemAccountId of the account you wish to remove...\n> " ) ;
rai_auth = wxcore.auth() ;
rai_data = { 'cobSessionToken' : rai_auth[0] , 'userSessionToken' : rai_auth[1] , 'itemAccountId' : rai_item } ;
rai_url  = wxcore.api_url + '/jsonsdk/ItemAccountManagement/removeItemAccount' ;
rai_post = requests.post( rai_url , data=rai_data) ;

if rai_post.status_code == 200:
    print "SUCCESS: account item removed" ;
else:
    print "ERROR: Non-200 response code from Account Item Removal API" ;

# fin
