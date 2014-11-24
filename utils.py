# -*- coding: utf-8 -*-

import numpy as np

def to_int(val):
    
    try:
        if isinstance(val, str):
            val = val.replace('\xc2\xa0', '').encode('utf-8')
            return np.float64(val)
        return val
    except ValueError, e:
        print e
        print val

def best_by_role(data, role, nret=5):
    """ returns a dataframe filtered by role and 
        sorted by the evaluation assigned.
        
        :param data, dataframe of players.
        :param role, str with the role (eg: player)
        :param nret int, number of player in the output dataframe.
    """
    player = data[data['Role'].isin(role)]
    
    # score must be integer
    return player.sort(['Lega'], ascending=[False])[:nret]