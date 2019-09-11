#   now 'hasOne' fields - as it is a create, just initialise to spaces
    vdict2 = {}
    for hasOneObj in ${obj_name}_instance.hasOne:
        HasOneObj = hasOneObj[0].upper() + hasOneObj[1:]
        fullname = '${obj_name}_' + hasOneObj + '_name'
        vdict2[fullname] = ''
    vdict.update(vdict2)
