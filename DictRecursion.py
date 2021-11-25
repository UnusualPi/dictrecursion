def recursive_dict_items(d, sep='_', ancestor_keys=True, flat_only=True, p_key=[]):
    """
    |--------------------------------------------------------------------
    | Feed this a dict with nested dicts and it'll find all the key value pairs.
    |
    | Parameters
    |--------------------------------------------------------------------
    | d : dict
    |   Pass a dictionary here.
    | sep : str, default '_'
    |   separator using in constructing new keys. *ancestor_keys must = True
    | ancestor_keys : bool, default True
    |   True combines all the ancestor keys using the sep, use this for keeping
    |   keys unique and/or showing key hierarchy, yields a dict.
    |   False makes no changes to keys, and yields tuples instead of a dict
    |   due to risk of duplicate keys in nested dicts.
    | flat_only : bool, default True
    |   True returns only the flat key, value pairs meaning key, value pairs
    |   where the value is a dict will be discarded.  False includes all key,
    |   value pairs found in the dict.
    | p_key : list, default []
    |   Only used in the regression, don't pass a value here.
    |
    | Example
    |--------------------------------------------------------------------
    | >>> d = {'K.0.1': 'V.0.1',
    |          'K.0.2': 'V.0.2',
    |          'K.0.3': {'K.1.1': 'V.1.1'},
    |          'K.0.4': {'K.1.2': {'K.2.1': 'V.2.1'}},
    |          'K.0.5': 'V.0.3'}
    | >>> x = recursive_dict_items(d,
    |                              sep=' | ',
    |                              flat_only=True,
    |                              ancestor_keys=True)
    | >>> print(*x, sep='\\n')
    | {'K.0.1': 'V.0.1'}
    | {'K.0.2': 'V.0.2'}
    | {'K.0.3 | K.1.1': 'V.1.1'}
    | {'K.0.4 | K.1.2 | K.2.1': 'V.2.1'}
    | {'K.0.5': 'V.0.3'}
    |--------------------------------------------------------------------
    """
    ancestors=p_key
    for k, v in d.items():
        if isinstance(v, dict) == True:
            ancestors.append(str(k)+sep)
            if flat_only == False:
                yield {k:v}
            yield from recursive_dict_items(v, sep=sep,
                                            ancestor_keys=ancestor_keys,
                                            flat_only=flat_only,
                                            p_key=ancestors)
            ancestors=[]
        else:
            yield (k,v) if ancestor_keys==False else {''.join(p_key)+k:v}
            ancestors=[]
