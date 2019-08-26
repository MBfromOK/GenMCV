# hasOne section - takes the id of the hasOne'd field and gets it and puts the
# 'name' into vdict2; if the id is zero then puts 'not defined' in vdict2
    vdict2 = {}
    for hasOneObj in ${obj_name}_instance.hasOne:
        HasOneObj = hasOneObj[0].upper() + hasOneObj[1:]
        r_id2 = ${obj_name}_instance.vars[hasOneObj]
        fullname = '${obj_name}_' + hasOneObj + '_name'
        if r_id2 == 0:
            vdict2[fullname] = 'not defined'
        else:
            hoObject = globals()[HasOneObj]
            ho_instance = hoObject()
            ho_instance.dbget(r_id2)
            ho_name = hasOneObj + '_name'
            vdict2[fullname] = ho_instance.vars[ho_name]
#   add 'hasOne' names to returned dict
    vdict.update(vdict2)
