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


# payload
ah_out_txt = '' ;


# +--------------------------------------------------------------+
# | create sorted list of account items...                       |
# | - stock accounts only (i.e., no loan, mortgage, ccard, etc.) |
# +--------------------------------------------------------------+

ai_dict = wxacct.list_acct_item() ;
ah_dict = {} ; # dict to hold account item data (for output)
ah_list = [] ; # list to hold account item IDs (for iteration)

i = 0 ;

for ai_item_key , ai_item_val in sorted( ai_dict.items() , key=lambda x: x[1] ): # sort dict by tuple values
    if ai_item_val[1] == 'stocks': # omit accts w/out holdings
        ah_list.append( ai_item_key ) ; # all account (*)
        ah_dict.update( { i : [ ai_item_key , ai_item_val[0] ] } ) ;
        i += 1 ;


# +-----------------------------------------+
# | single account: show valid account menu |
# +-----------------------------------------+

if ah_aon == '1':
    print '\nActive Accounts...\n' ;
    for ah_item_key , ah_item_val in sorted( ah_dict.items() ):
        print ' [' + str( ah_item_key ) + '] ' + ah_item_val[1] + ' (' + str( ah_item_val[0] ) + ')' ;

    ah_one = raw_input( "\nEnter the line [#] of the account...\n> " ) ;

    # * = overwrite list of ALL account IDs w/ the user-specified ID
    ah_list = [ ah_dict[ int( ah_one ) ][0] ] ;


# +---------------------------------------------------+
# | for item(s) -- 1 or all -- get holdings json blob |
# +---------------------------------------------------+

# iterate over account items
for item in ah_list:

    # kludge!
    item_id = item ;

    # get item holdings
    ah_json = wxacct.list_acct_item_holding( item_id ) ;

    # debug: json output
    # print ah_json ; exit(0) ;

    # ascii-box
    box_dsh = '' ;
    len_nm  = len( ah_json[ 'itemDisplayName' ] ) ;
    len_id  = len( str( item_id ) ) ;
    len_all = len_nm + len_id + 18 ;
    for x in range ( 1 , len_all ): box_dsh += '-' ;

    # top-level account label
    ah_out_txt += \
        '\n' + \
        '+' + box_dsh + '+\n' + \
        '| HOLDINGS :: ' + \
        ah_json[ 'itemDisplayName' ] + \
        ' (' + \
        str( item_id ) + \
        ') |\n' + \
        '+' + box_dsh + '+\n' ;

    # how many account items?
    ah_acct_num = len( ah_json[ 'itemData' ][ 'accounts' ] ) ;

    # iterate over account items
    for i in range( ah_acct_num ):

        # debug: account JSON
        # print ah_json[ 'itemData' ][ 'accounts' ][i] ;

        # init output vars
        ah_out_dict = {} ;

        # acct descriptor
        ah_out_txt += \
            '\n' + \
            ah_json[ 'itemData' ][ 'accounts' ][i][ 'accountName' ] + \
            ' (' + \
            str( ah_json[ 'itemData' ][ 'accounts' ][i][ 'itemAccountId' ] ) + \
            ')...\n' ;

        # at least 1 holding -> get details
        if 'holdings' in ah_json[ 'itemData' ][ 'accounts' ][i]:

            # how many holdings?
            ah_hold_num = len( ah_json[ 'itemData' ][ 'accounts' ][i][ 'holdings' ] ) ;

            # iterate over holdings
            for j in range( ah_hold_num ):

                # some investments don't have symbols :(
                ah_hold_sym = '' ;
                if 'symbol' in ah_json[ 'itemData' ][ 'accounts' ][i][ 'holdings' ][j]:
                    ah_hold_sym = ah_json[ 'itemData' ][ 'accounts' ][i][ 'holdings' ][j][ 'symbol' ] ;

                # vars
                ah_hold_val =      ah_json[ 'itemData' ][ 'accounts' ][i][ 'holdings' ][j][ 'value' ][ 'amount' ] ;
                ah_hold_dsc =      ah_json[ 'itemData' ][ 'accounts' ][i][ 'holdings' ][j][ 'description' ] ;
                ah_hold_qty = str( ah_json[ 'itemData' ][ 'accounts' ][i][ 'holdings' ][j][ 'quantity' ] ) ;
                ah_hold_pri = str( ah_json[ 'itemData' ][ 'accounts' ][i][ 'holdings' ][j][ 'price' ][ 'amount' ] ) ;

                ah_hold_txt = \
                    ah_hold_sym + ' (' + \
                    ah_hold_dsc + ') >> ' + \
                    ah_hold_qty + ' @ $' + \
                    ah_hold_pri + '\n' ;

                # stuff dict (item)
                ah_out_dict.update( { ah_hold_val : ah_hold_txt } ) ;

        # no holdings -> show equity balances
        else:

            # equity balance :: total
            if 'totalBalance' in ah_json[ 'itemData' ][ 'accounts' ][i]:
                ah_hold_val = ah_json[ 'itemData' ][ 'accounts' ][i][ 'totalBalance' ][ 'amount' ] ;
                ah_hold_txt = 'Balance (Total)\n' ;
                ah_out_dict.update( { ah_hold_val : ah_hold_txt } ) ;

            # equity balance :: total (unvested)
            if 'totalUnvestedBalance' in ah_json[ 'itemData' ][ 'accounts' ][i]:
                ah_hold_val = ah_json[ 'itemData' ][ 'accounts' ][i][ 'totalUnvestedBalance' ][ 'amount' ] ;
                ah_hold_txt = 'Balance (Unvested)\n' ;
                ah_out_dict.update( { ah_hold_val : ah_hold_txt } ) ;

            # equity balance :: total (vested)
            if 'totalVestedBalance' in ah_json[ 'itemData' ][ 'accounts' ][i]:
                ah_hold_val = ah_json[ 'itemData' ][ 'accounts' ][i][ 'totalVestedBalance' ][ 'amount' ] ;
                ah_hold_txt = 'Balance (Vested)\n' ;
                ah_out_dict.update( { ah_hold_val : ah_hold_txt } ) ;

        # iterate over dict to build output string
        for item in sorted( ah_out_dict , reverse=True ):
            ah_out_txt += \
                ' $' + \
                '{:,.2f}'.format( item ).rjust(13) + \
                ' :: ' + \
                ah_out_dict[ item ] ;

# spew
print ah_out_txt ;

# fin
