def create_owned():
# create a new record, but action has come from the owner transaction so owner_type
# and owner_id are already set
#
# note this can only be called from get_all_for_owner.html and the two post variables below
# have non standard names, but when passed into create.html must have the standard names (attrib_...)
    ${obj_name}_instance = ${obj_Name}()
    vdict = ${obj_name}_instance.toview()
#    print request.post_vars
    vdict['${obj_name}_ownerType'] = request.post_vars['ownerType']
    vdict['${obj_name}_ownerId'] = request.post_vars['ownerId']

# but we use the standard create view
    response.view = '${obj_name}/create.html'
#    print 'create owned '
#    print vdict
    return vdict


def get_all_for_owner():
# note the following post vars are not named as standard data items - see get_all_for_owner.html
    owner = request.post_vars['ownerType']
    owner_id = request.post_vars['ownerId']
#    print 'get all for '
#    print owner, owner_id
    ${obj_name}_instance = ${obj_Name}()
    ${obj_name}_list = ${obj_name}_instance.dbget_all_for(owner, owner_id, 'all', limitby=None)
    gafo = dict(rows=${obj_name}_list)
    gafo['ownerType'] = owner
    gafo['ownerId'] = owner_id
    return gafo
