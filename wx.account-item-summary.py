#! /usr/bin/python

import requests ;
import wxcore ;

# (a)ccount (h)oldings
ah_auth = wxcore.auth() ;
ah_data = { 'cobSessionToken' : ah_auth[0] , 'userSessionToken' : ah_auth[1] } ;
ah_url  = wxcore.api_url + '/jsonsdk/DataService/getItemSummariesWithoutItemData' ;
ah_post = requests.post( ah_url , data=ah_data) ;
print ah_post.text ;

# fin
