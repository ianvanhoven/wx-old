#! /usr/bin/python

import wxacct ;

al_dict = wxacct.list() ;

for id in al_dict:
    print str( id ).strip() , '::' , al_dict[ id ] ;

# fin
