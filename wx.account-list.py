#! /usr/bin/python

import requests ;
import wxcore ;

# list accounts
la_auth = wxcore.auth() ;
la_data = { 'cobSessionToken' : la_auth[0] , 'userSessionToken' : la_auth[1] } ;
la_url  = wxcore.api_url + '/jsonsdk/SiteAccountManagement/getAllSiteAccounts' ;
la_post = requests.post( la_url , data=la_data) ;
print la_post.text.encode( 'utf-8' ) ;

# fin
