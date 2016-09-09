#! /usr/bin/python

from lxml import etree ;

import json ;
import requests ;
import wxcore ;


# +-------------------------+
# | data :: account summary |
# +-------------------------+

as_auth = wxcore.auth() ;

as_url = \
    wxcore.api_url + \
    'account/summary/all?cobSessionToken=' + \
    as_auth[0].rstrip() + \
    '&userSessionToken=' + \
    as_auth[1].rstrip() ;

as_get  = requests.get( as_url , headers=wxcore.api_hdr_json ) ;


# +---------------------------------------------+
# | debug :: print / write json payload to file |
# +---------------------------------------------+
# print as_get.text ; exit(0) ;
# file_json = open( '/tmp/wx.account-summary.json' , 'w' ) ;
# file_json.write( as_get.text ) ;
# file_json.close() ;


# valid response?
if as_get.status_code != 200: print 'ERROR: Non-200 REST API server response (Account Summary), exiting' ; exit(1) ;
if 'ItemContainer' not in as_get.text: print 'ERROR: JSON response missing (Account Summary), exiting' ; exit(1) ;

# load bigass JSON payload into dict for iteration
as_dict = json.loads( as_get.text ) ;


# +---------------------------+
# | Order of account types... |
# | - 0: LOANS                |
# | - 1: MORTGAGE             |
# | - 2: CREDITS              |
# | - 3: BANK                 |
# | - 4: STOCKS               |
# +---------------------------+


# +-----------------+
# | data :: (loan)s |
# +-----------------+

total_loan    = 0 ;
blurb_loan_ba = '' ;

for acct in as_dict[ 'ItemContainer' ][0][ 'LoanItemAccountSummary' ]:

    loan_id  = acct[ 'itemId' ] ;
    loan_bal = acct[ 'Balance' ][ 'amount' ] ;
    loan_nom = str( acct[ 'AccountName' ] ).replace( '- Loan -' , '' ) ;

    # bofa (car)
    if 'Bank of America' in loan_nom:
        loan_nom = loan_nom.replace( ' Installment Loanx2442' , '(x2442)' ) ;
        blurb_loan_ba += ' $' + '{:,.2f}'.format( loan_bal ).rjust(13) + ' :: [' + loan_id + '] ' + loan_nom + '\n' ;

    # all
    total_loan += loan_bal ;


# +--------------------+
# | data :: (mort)gage |
# +--------------------+

total_mort    = 0  ;
blurb_mort_cl = '' ;

for acct in as_dict[ 'ItemContainer' ][1][ 'MortageItemAccountSummary' ]: # [sic]

    mort_id  = acct[ 'itemId' ] ;
    mort_bal = acct[ 'Balance' ][ 'amount' ] ;
    mort_nom = str( acct[ 'AccountName' ] ).replace( '- Loan -' , '' ) ;

    # cenlar (house)
    if 'Cenlar' in mort_nom:
        mort_nom = mort_nom.replace( '- Mortgage - xxxx3351' , '(x3351)' ) ;
        blurb_mort_cl += ' $' + '{:,.2f}'.format( mort_bal ).rjust(13) + ' :: [' + mort_id + '] ' + mort_nom + '\n' ;

    # all
    total_mort += mort_bal ;


# +-----------------+
# | data :: (card)s |
# +-----------------+

total_card    = 0 ;
total_card_ch = 0 ;
blurb_card_ch = '' ;
total_card_up = 0 ;
blurb_card_up = '' ;

for acct in as_dict[ 'ItemContainer' ][2][ 'CCItemAccountSummary' ]:

    card_id  = acct[ 'itemId' ] ;
    card_bal = acct[ 'Balance' ][ 'amount' ] ;
    card_nom = str( acct[ 'AccountName' ] ).replace( '- Credit Card - CREDIT CARD' , '' ) ;

    # chase (mc)
    if 'Chase' in card_nom:
        total_card_ch += card_bal ;
        blurb_card_ch += ' $' + '{:,.2f}'.format( card_bal ).rjust(13) + ' :: [' + card_id + '] ' + card_nom + '\n' ;

    # upromise/barclay (visa)
    if 'Barclay' in card_nom:
        card_nom = card_nom.replace( 'Barclaycard - ' , '' ) ;
        total_card_up += card_bal ;
        blurb_card_up += ' $' + '{:,.2f}'.format( card_bal ).rjust(13) + ' :: [' + card_id + '] ' + card_nom + '\n' ;

    # all
    total_card += card_bal ;



# +-----------------+
# | data :: banking |
# +-----------------+

total_bank    = 0 ;
total_bank_ba = 0 ;
blurb_bank_ba = '' ;

for acct in as_dict[ 'ItemContainer' ][3][ 'BankingItemAccountSummary' ]:

    bank_id  = acct[ 'itemId' ] ;
    bank_bal = acct[ 'Balance' ][ 'amount' ] ;
    bank_nom = acct[ 'AccountName' ] ;

    # bofa
    if 'Bank of America' in bank_nom:
        bank_nom = bank_nom.replace( 'Bank of America - Bank - ' , '' ) ;
        bank_nom = bank_nom.replace( 'Bank of America ' , '' ) ;
        total_bank_ba += bank_bal ;
        blurb_bank_ba += ' $' + '{:,.2f}'.format( bank_bal ).rjust(13) + ' :: [' + bank_id + '] ' + bank_nom + '\n' ;

    # all
    total_bank += bank_bal ;


# +----------------------+
# | data :: (inv)estment |
# +----------------------+

total_inv    = 0 ;
total_inv_et = 0 ;
total_inv_fd = 0 ;
total_inv_vg = 0 ;

blurb_inv_et = '' ;
blurb_inv_fd = '' ;
blurb_inv_vg = '' ;

for acct in as_dict[ 'ItemContainer' ][4][ 'InvestmentAccountSummary' ]:

    inv_id  = acct[ 'itemId' ] ;
    inv_nom = str( acct[ 'AccountName' ] ).replace( 'Investments -' , '' ) ;
    inv_val = acct[ 'Balance' ][ 'amount' ] ;

    # etrade
    if 'E*TRADE' in inv_nom:
        inv_nom = inv_nom.replace( 'E*TRADE' , '' ) ;
        inv_nom = inv_nom.replace( 'Employee Stock Plans' , '' ) ;
        inv_nom = inv_nom.replace( ' - ' , '' ) ;
        total_inv_et += inv_val ;
        blurb_inv_et += ' $' + '{:,.2f}'.format( inv_val ).rjust(13) + ' :: [' + inv_id + '] ' + inv_nom + '\n' ;

    # fidelity
    if 'Fidelity' in inv_nom:
        inv_nom = inv_nom.replace( 'Fidelity' , '' ) ;
        total_inv_fd += inv_val ;
        blurb_inv_fd += ' $' + '{:,.2f}'.format( inv_val ).rjust(13) + ' :: [' + inv_id + ']' + inv_nom + '\n' ;

    # vanguard
    if 'Vanguard' in inv_nom:
        inv_nom = inv_nom.replace( 'Vanguard - ' , '' ) ;
        total_inv_vg += inv_val ;
        blurb_inv_vg += ' $' + '{:,.2f}'.format( inv_val ).rjust(13) + ' :: [' + inv_id + ']' + inv_nom + '\n' ;

    # all
    total_inv += inv_val ;


# +------------------------+
# | home value (zestimate) |
# +------------------------+

hom_zws = 'X1-ZWz19oxuwxlyx7_ako3m' ; # zillow webservice ID
hom_pid = '15602526' ; # zillow property ID (196 Crescent, PV CA 94028)
hom_url = 'http://www.zillow.com/webservice/GetZestimate.htm?zws-id=' + hom_zws + '&zpid=' + hom_pid ;
hom_get = requests.get( hom_url ) ; # returns XML :(

hom_xml = etree.XML( hom_get.content ) ;

hom_loc  = '' ;
hom_loc += hom_xml.findtext( './/response/address/street' ) + ', ' ;
hom_loc += hom_xml.findtext( './/response/address/city' )   + ' ' ;
hom_loc += hom_xml.findtext( './/response/address/state' )  + ' ' ;
hom_loc += hom_xml.findtext( './/response/address/zipcode' ) ;

hom_est = hom_xml.findtext( './/response/zestimate/amount' ) ;

total_hom = int( hom_est ) ;



# +---------+
# | do math |
# +---------+

total_all_debt = total_loan + total_mort + total_card ;
total_all_cred = total_bank + total_inv + total_hom ;
total_all_net  = total_all_cred - total_all_debt ;


# +------+
# | spew |
# +------+

print \
'\n+--------------+' \
'\n| Debt :: Loan |' \
'\n+--------------+\n' \
'\n' , blurb_loan_ba , \
'\nTOTAL (All Loans): ${:,.2f}'.format( total_loan ) , '\n' ;

print \
'\n+------------------+' \
'\n| Debt :: Mortgage |' \
'\n+------------------+\n' \
'\n' , blurb_mort_cl , \
'\nTOTAL (All Mortgages): ${:,.2f}'.format( total_mort ) , '\n' ;

print \
'\n+---------------------+' \
'\n| Debt :: Credit Card |' \
'\n+---------------------+\n' \
'\n' , blurb_card_ch , blurb_card_up , \
'\nTOTAL (All Cards): ${:,.2f}'.format( total_card ) , '\n' ;

print \
'\n+----------------+' \
'\n| Credit :: Bank |' \
'\n+----------------+\n' \
'\nBank of America...\n'  , blurb_bank_ba , ' $' , '{:,.2f}'.format( total_bank_ba ).rjust(12) , ':: Subtotal\n' \
'\nTOTAL (All Banks): ${:,.2f}'.format( total_bank ) , '\n' ;

print \
'\n+----------------------+' \
'\n| Credit :: Investment |' \
'\n+----------------------+\n' \
'\nE*Trade...\n'  , blurb_inv_et , ' $' , '{:,.2f}'.format( total_inv_et ).rjust(12) , ':: Subtotal\n' \
'\nFidelity...\n' , blurb_inv_fd , ' $' , '{:,.2f}'.format( total_inv_fd ).rjust(12) , ':: Subtotal\n' \
'\nVanguard...\n' , blurb_inv_vg , ' $' , '{:,.2f}'.format( total_inv_vg ).rjust(12) , ':: Subtotal\n' \
'\nTOTAL (All Investments): ${:,.2f}'.format( total_inv ) , '\n' ;

print \
'\n+--------------------------+' \
'\n| Credit :: Property (Est) |' \
'\n+--------------------------+\n' \
'\n $' , '{:,.2f}'.format( total_hom ).rjust(12) , '::' , hom_loc , '\n' \
'\nTOTAL (All Property): ${:,.2f}'.format( total_hom ).rjust(12) , '\n' ;

print \
'\n+-------------------------+' \
'\n| SUMMARY :: All Accounts |' \
'\n+-------------------------+\n' \
'\n$' , '{:,.2f}'.format( total_all_cred ).rjust(12) , ':; Total (Credits)' \
'\n$' , '{:,.2f}'.format( total_all_debt ).rjust(12) , ':; Total (Debts)' \
'\n$' , '{:,.2f}'.format( total_all_net ).rjust(12)  , ':; TOTAL (Net)\n' ;

# fin!
exit( 0 ) ;
