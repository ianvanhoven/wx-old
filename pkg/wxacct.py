#! /usr/bin/python

# +-------------------------------+
# | account-related funcs...      |
# | - [list|map] site account IDs |
# | - list account item IDs       |
# | - list account holdings       |
# +-------------------------------+


# +------------------------------------------------------------------------------------------+
# | CAVEAT: no freaking clue how "site account ID" & "account item ID" differ :( yodlee #wtf |
# +------------------------------------------------------------------------------------------+


# slurp
import json ;
import os.path ;
import requests ;
import wxcore ;


# +--------------------------------------+
# | account :: list (s)ite (a)ccount IDs |
# +--------------------------------------+

def list_acct_site():

    as_auth = wxcore.auth() ;
    as_data = { 'cobSessionToken' : as_auth[0] , 'userSessionToken' : as_auth[1] } ;
    as_url  = wxcore.api_url + '/jsonsdk/SiteAccountManagement/getAllSiteAccounts' ;
    as_post = requests.post( as_url , data=as_data ) ;
    as_json = json.loads( as_post.text ) ;

    # debug: spew raw account listing json
    # print as_post.text.encode( 'utf-8' ) ;

    as_dict = {} ;

    # return dict of {id,name} -- even though client may use mapped name instead (see below)
    for acct in as_json:
        as_dict.update( { acct[ 'siteAccountId' ] : acct[ 'siteInfo' ][ 'defaultDisplayName' ] } ) ;

    # paydirt
    return as_dict ;


# +-----------------------------------------------------+
# | account :: map (s)ite (a)ccount IDs to custom names |
# +-----------------------------------------------------+

def map_id_name( map_type ):

    map_types = { \
        'ai' : 'acct-item' , \
        'as' : 'acct-site'
        } ;

    map_data = {} ;

    map_file = wxcore.api_dir_data + 'wx.map.' + map_types[ map_type ] + '.txt' ;

    if os.path.isfile( map_file ):
        f = open( map_file , 'r' ) ;
        map_line = f.readlines() ;
        f.close() ;

    else: print '[pkg/wxacct.py] ERROR: Cannot find/open id -> name mapping file' ; exit(1) ;

    map_len = len( map_line ) ;

    for i in range ( 0 , map_len ):
        #map_line[i].rstrip() ;
        map_item = map_line[i].rstrip().split( '#' ) ;
        map_data.update( { map_item[0] : map_item[1] } ) ;

    return map_data ;
    
 
# +--------------------------------------+
# | account :: list (a)ccount (i)tem IDs |
# +--------------------------------------+

def list_acct_item():

    # list of (s)ite (a)ccount IDs
    as_dict = list_acct_site() ;

    # request params for list of (a)ccount (i)tems
    ai_auth = wxcore.auth() ;
    ai_url  = wxcore.api_url + '/jsonsdk/DataService/getItemSummariesForSite' ;

    ai_dict = {} ;

    for id in as_dict:

        ai_data = { \
            'cobSessionToken'  : ai_auth[0] , \
            'userSessionToken' : ai_auth[1] , \
            'memSiteAccId'     : id
        } ;

        ai_post = requests.post( ai_url , data=ai_data ) ;
        ai_json = json.loads( ai_post.text ) ;

        # debug: print raw account item listing
        # print id , '\n' , ai_post.text ; # .encode( 'utf-8' ) ;

        for item in ai_json:

            # +---------------------+
            # | include...          |
            # | - key: account ID   |
            # | - val: account name |
            # | - val: account type |
            # +---------------------+

            if 'itemDisplayName' in item:
                ai_dict.update( { \
                    item[ 'itemId' ] : [ item[ 'itemDisplayName' ] , \
                    item[ 'contentServiceInfo' ][ 'containerInfo' ][ 'containerName' ] ] \
                } ) ;

    # paydirt
    return ai_dict ;


# +---------------------------------------------+
# | account :: list (a)ccount (i)tem (h)oldings |
# +---------------------------------------------+

def list_acct_item_holding( aih_item ):

    aih_auth = wxcore.auth() ;
    aih_url  = wxcore.api_url + '/jsonsdk/DataService/getItemSummaryForItem1' ;

    # see http://goo.gl/pvGHf1 for dex.extentLevels[*] settings
    aih_data = {
        'cobSessionToken'     : aih_auth[0] ,
        'userSessionToken'    : aih_auth[1] ,
        'itemId'              : aih_item ,
        'dex.startLevel'      : 0 ,
        'dex.endLevel'        : 0 ,
        'dex.extentLevels[0]' : 0 ,
        'dex.extentLevels[1]' : 2
    } ;

    # http post -> json response
    aih_post = requests.post( aih_url , data=aih_data ) ;
    aih_json = json.loads( aih_post.text ) ;

    # paydirt
    return aih_json ;


# fin
