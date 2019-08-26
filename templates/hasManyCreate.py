# processing for hasMany fields
# these are not present in the define_table() but are defined in the 'hasMany' list
# for create, just have entries set to zero etc.
    print 'in hasmany'
    vdict3 = {}
    for hasManyObj in ${obj_name}_instance.hasMany:
        print hasManyObj
        HasManyObj = hasManyObj[0].upper() + hasManyObj[1:]
        fullname = '${obj_name}_' + hasManyObj + '_rows'
        fullnamecount = fullname + 'count'
        vdict3[fullnamecount] = 0
        vdict3[fullname] = None
        print vdict3
#   add 'hasMany' names to returned dict
    vdict.update(vdict3)
