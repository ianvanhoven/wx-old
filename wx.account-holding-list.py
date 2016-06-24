#! /usr/bin/python


# +---------------------------+
# | accounts: all, one, none? |
# +---------------------------+

ah_aon = raw_input( "\nView holdings for all accounts (default), just one (1) or exit (0)?...\n> " ) ;

# bail
if ah_aon == '0': print "Exiting\n" ; exit(0) ;


# load up
import json ;
import requests ;
import wxacct ;
import wxcore ;


# +-----------------------------------------------------------+
# | create sorted list of account items (stock accounts only) |
# +-----------------------------------------------------------+

ai_dict = wxacct.list_acct_item() ;
ah_dict = {} ; # dict to hold account item data
ah_list = [] ; # list to hold account item IDs

i = 0 ;

for ai_item_key , ai_item_val in sorted( ai_dict.items() , key=lambda x: x[1] ): # sort dict by tuple values
    if ai_item_val[1] == 'stocks': # omit credit, loan, etc. (i.e., accts w/out holdings)
        ah_list.append( ai_item_key ) ; # all accounts
        ah_dict.update( { i : [ ai_item_key , ai_item_val[0] ] } ) ;
        i += 1 ;


# +--------------------------------------------+
# | single account: show valid account choices |
# +--------------------------------------------+

if ah_aon == '1':
    print '\nActive Accounts...' ;
    for ah_item_key , ah_item_val in sorted( ah_dict.items() ):
        print '[' + str( ah_item_key ) + '] ' + ah_item_val[1] + ' (' + str( ah_item_val[0] ) + ')' ;

    ah_one = raw_input( "\nEnter the line [#] of the account...\n> " ) ;

    # overwrite list of ALL account IDs w/ the user-specified ID
    ah_list = [ ah_dict[ int( ah_one ) ][0] ] ;


# +------------------------------------------------------+
# | request params for list of (a)ccount item (h)oldings |
# +------------------------------------------------------+

ah_auth = wxcore.auth() ;
ah_url  = wxcore.api_url + '/jsonsdk/DataService/getItemSummaryForItem1' ;

# iterate over account items
for item in ah_list:

    ah_data = {
        'cobSessionToken'     : ah_auth[0] ,
        'userSessionToken'    : ah_auth[1] ,
        'itemId'              : item ,
        'dex.startLevel'      : 0 ,
        'dex.endLevel'        : 0 ,
        'dex.extentLevels[0]' : 0 ,
        'dex.extentLevels[1]' : 2
    } ;

    # http post -> json response
    ah_post = requests.post( ah_url , data=ah_data ) ;
    ah_json = json.loads( ah_post.text ) ;

    # debug: json output
    # print ah_json ; exit(0) ;

    # init output
    ah_hold_out = '' ;

    # how many account items?
    ah_acct_num = len( ah_json[ 'itemData' ][ 'accounts' ] ) ;

    # iterate over account items
    for i in range( ah_acct_num ):

        ah_hold_out += \
            '\nHoldings: ' + \
            ah_json[ 'itemDisplayName' ] + \
            ' -- ' + \
            ah_json[ 'itemData' ][ 'accounts' ][i][ 'accountName' ] + \
            ' (' + \
            str( item ) + \
            ') ...\n' ;

        # at least 1 holding -> get details
        if 'holdings' in ah_json[ 'itemData' ][ 'accounts' ][i]:

            # how many holdings?
            ah_hold_num = len( ah_json[ 'itemData' ][ 'accounts' ][i][ 'holdings' ] ) ;

            # iterate over holdings
            for j in range( ah_hold_num ):

                # some investments don't have symbols :(
                ah_hold_sym = '' ;
                if 'symbol' in ah_json:
                    ah_hold_sym = str( ah_json[ 'itemData' ][ 'accounts' ][i][ 'holdings' ][j][ 'symbol' ] ) + ' :: ' ;

                ah_hold_dsc = str( ah_json[ 'itemData' ][ 'accounts' ][i][ 'holdings' ][j][ 'description' ] ) ;
                ah_hold_val =      ah_json[ 'itemData' ][ 'accounts' ][i][ 'holdings' ][j][ 'value' ][ 'amount' ] ;
                ah_hold_qty = str( ah_json[ 'itemData' ][ 'accounts' ][i][ 'holdings' ][j][ 'quantity' ] ) ;
                ah_hold_pri = str( ah_json[ 'itemData' ][ 'accounts' ][i][ 'holdings' ][j][ 'price' ][ 'amount' ] ) ;

                ah_hold_out += \
                    '-- $' + \
                    '{:,.2f}'.format( ah_hold_val ).rjust(13) + ' :: ' + \
                    ah_hold_sym + \
                    ah_hold_dsc + ' :: ' + \
                    ah_hold_qty + ' @ $' + \
                    ah_hold_pri + '\n' ;

        # no holdings: show equity balances instead
        else:

            # (e)quity (b)alance :: (t)otal
            ah_hold_ebt = ah_json[ 'itemData' ][ 'accounts' ][i][ 'totalBalance' ][ 'amount' ] ;
            ah_hold_out += '-- $' + '{:,.2f}'.format( ah_hold_ebt ).rjust(13) + ' :: balance (total) \n' ;

            # (e)quity (b)alance :: (u)nvested
            if 'totalUnvestedBalance' in ah_json[ 'itemData' ][ 'accounts' ][i]:
                ah_hold_ebu = ah_json[ 'itemData' ][ 'accounts' ][i][ 'totalUnvestedBalance' ][ 'amount' ] ;
                ah_hold_out += '-- $' + '{:,.2f}'.format( ah_hold_ebu ).rjust(13) + ' :: balance (unvested) \n' ;

            # (e)quity (b)alance :: (v)ested
            if 'totalVestedBalance' in ah_json[ 'itemData' ][ 'accounts' ][i]:
                ah_hold_ebv = ah_json[ 'itemData' ][ 'accounts' ][i][ 'totalVestedBalance' ][ 'amount' ] ;
                ah_hold_out += '-- $' + '{:,.2f}'.format( ah_hold_ebv ).rjust(13) + ' :: balance (vested) \n' ;

    # spew
    print ah_hold_out ;

# fin
