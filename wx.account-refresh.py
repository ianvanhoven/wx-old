#! /usr/bin/python

import json ;
import requests ;
import wxcore ;

# refresh account
ra_item = raw_input( "\nEnter the itemId of the account you wish to refresh...\n> " ) ;
ra_auth = wxcore.auth() ;

ra_data = { \
    'cobSessionToken' : ra_auth[0] , \
    'userSessionToken' : ra_auth[1] , \
    'itemId' : ra_item , \
    'refreshParameters.refreshMode.refreshMode' : 'NORMAL' , \
    'refreshParameters.refreshMode.refreshModeId' : '2' , \
    'refreshParameters.refreshPriority' : '1' \
} ;

ra_url  = wxcore.api_url + '/jsonsdk/Refresh/startRefresh7' ;
ra_post = requests.post( ra_url , data=ra_data) ;

if ra_post.status_code == 200:

    ra_post_code = [ \
        'STATUS_UNKNOWN_CODE' , \
        'SUCCESS_NEXT_REFRESH_SCHEDULED_CODE' , \
        'REFRESH_ALREADY_IN_PROGRESS_CODE' , \
        'UNSUPPORTED_OPERATION_FOR_SHARED_ITEM_CODE' , \
        'SUCCESS_START_REFRESH_CODE' , \
        'ITEM_CANNOT_BE_REFRESHED_CODE' , \
        'ALREADY_REFRESHED_RECENTLY_CODE' , \
        'UNSUPPORTED_OPERATION_FOR_CUSTOM_ITEM_CODE' , \
        'SUCCESS_REFRESH_WAIT_FOR_MFA_CODE' \
    ] ;

    ra_dict = json.loads( ra_post.text ) ;

    print 'SUCCESS: ' + ra_post_code[ ra_dict[ 'status' ] ] ;

else:

    print 'ERROR: Non-200 response code from Account Refresh API' ;

# fin
