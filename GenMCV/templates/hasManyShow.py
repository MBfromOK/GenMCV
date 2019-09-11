# processing for hasMany fields
# these are not present in the define_table() but are defined in the 'hasMany' list
    print 'in hasmany'
    vdict3 = {}
    for hasManyObj in ${obj_name}_instance.hasMany:
        print hasManyObj
        HasManyObj = hasManyObj[0].upper() + hasManyObj[1:]
        fullname = '${obj_name}_' + hasManyObj + '_rows'
        fullnamecount = fullname + 'count'
        hmObject = globals()[HasManyObj]
        hm_instance = hmObject()
        hmObject_list = hm_instance.dbget_all_for('${obj_name}', r_id, 'all')
        listcount = sum(1 for row in hmObject_list)
        vdict3[fullnamecount] = listcount
        print 'list count '
        print listcount
        print 'hm list '
        print hmObject_list
        print 'fullname ' + fullname
        vdict3[fullname] = hmObject_list
        print vdict3
#   add 'hasMany' names to returned dict
    vdict.update(vdict3)

