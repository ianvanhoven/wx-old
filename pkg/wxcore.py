#! /usr/bin/python


# +-----------+
# | saddle up |
# +-----------+

import json ;
import os.path ;
import requests ;
import time ;


# +---------+
# | globals |
# +---------+

api_dir = '/space/home/ivh/tool/wealthx/' ;
api_dir_data = api_dir + 'data/' ;
api_hdr_json = { 'Content-Type' : 'application/json' , 'Accept' : 'application/json' } ;
api_hdr_xml = { 'Content-Type' : 'application/xml' , 'Accept' : 'application/xml' } ;
api_url = 'https://rest.developer.yodlee.com/services/srest/restserver/v1.0/' ;


# +----------------------------------------------+
# | auth :: co-brand & user login session tokens |
# +----------------------------------------------+

def auth():

    # check for existing valid token(s)...
    # - co-brand token expires every 100m
    # - user login token expires every 30m
    # ...which is annoying/pointless...
    # ...so 29m as co-expiry for simplicity

    wx_auth_dir = api_dir + 'data/' ;
    wx_auth_token_new = 1 ;
    wx_auth_token_txt = wx_auth_dir + 'wx.auth.token.txt' ;
    wx_time_now = int( time.time() ) ;

    # check presence/age of existing auth tokens
    if os.path.isfile( wx_auth_token_txt ):

        f = open( wx_auth_token_txt , 'r' ) ;
        wx_auth_token_data = f.readlines() ;
        f.close() ;

        # use existing unexpired tokens
        wx_time_old = int( wx_auth_token_data[0] ) ;
        if wx_time_now - wx_time_old <= 1740: # 29:00 (see above ^)
            cb_auth = wx_auth_token_data[1] ;
            ul_auth = wx_auth_token_data[2] ;
            wx_auth_token_new = 0 ;

    else: print '[pkg/wxcore.py] ERROR: Cannot find/open token auth file' ; exit(1) ;

    # existing auth tokens missing or expired: create/store new tokens
    if wx_auth_token_new == 1:

        # co-brand
        wx_auth_cobrand_txt = wx_auth_dir + 'wx.auth.cobrand.txt' ;
        if os.path.isfile( wx_auth_cobrand_txt ):
            f = open( wx_auth_cobrand_txt , 'r' ) ;
            wx_auth_cobrand_data = f.readlines() ;
            f.close() ;
        else: print '[pkg/wxcore.py] ERROR: Cannot find/open cobrand auth file' ; exit(1) ;

        cb_data = { 'cobrandLogin' : wx_auth_cobrand_data[0].rstrip() , 'cobrandPassword' : wx_auth_cobrand_data[1].rstrip() } ;
        cb_url  = api_url + 'authenticate/coblogin' ;
        cb_post = requests.post( cb_url , data=cb_data ) ;
        if cb_post.status_code != 200: print '[pkg/wxcore.py] ERROR: Non-200 REST API server response (Co-Brand Login), exiting' ; exit(1) ;
        if 'sessionToken' not in cb_post.text: print '[pkg/wxcore.py] ERROR: Co-Brand Login session token missing, exiting' ; exit(1) ;
        cb_dict = json.loads( cb_post.text ) ;
        cb_auth = cb_dict[ 'cobrandConversationCredentials' ][ 'sessionToken' ] ;

        # user login
        wx_auth_user_txt = wx_auth_dir + 'wx.auth.user.txt' ;
        if os.path.isfile( wx_auth_user_txt ):
            f = open( wx_auth_user_txt , 'r' ) ;
            wx_auth_user_data = f.readlines() ;
            f.close() ;
        else: print '[pkg/wxcore.py] ERROR: Cannot find/open user auth file' ;

        ul_data = { 'cobSessionToken' : cb_auth , 'login' : wx_auth_user_data[0].rstrip() , 'password' : wx_auth_user_data[1].rstrip() } ;
        ul_url  = api_url + 'authenticate/login' ;
        ul_post = requests.post( ul_url , data=ul_data ) ;
        if ul_post.status_code != 200: print '[pkg/wxcore.py] ERROR: Non-200 REST API server response (User Login), exiting' ; exit(1) ;
        if 'sessionToken' not in ul_post.text: print '[pkg/wxcore.py] ERROR: User Login session token missing, exiting' ; exit(1) ;
        ul_dict = json.loads( ul_post.text ) ;
        ul_auth = ul_dict[ 'userContext' ][ 'conversationCredentials' ][ 'sessionToken' ] ;

        # write time + tokens to auth file
        f = open( wx_auth_token_txt , 'w' ) ;
        f.write( '{:.0f}'.format( wx_time_now ) + '\n' + cb_auth + '\n' + ul_auth ) ;
        f.close() ;

    # paydirt
    return [ cb_auth , ul_auth ] ;

# fin
