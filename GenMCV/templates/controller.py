__author__ = 'graham'

from $obj_name import $obj_Name
$$hasOneimports
$$hasManyimports

# the controller for the $obj_Name objects


def index():
#  the default action - just show a list of $obj_Name s, if there are any
    ${obj_name}_instance = $obj_Name()
    ${obj_name}_list = ${obj_name}_instance.list_all('all', limitby=(0, 25))
    return dict(rows=${obj_name}_list)


def list():
#
    ${obj_name}_instance = $obj_Name()
    ${obj_name}_list = ${obj_name}_instance.list_all('all', limitby=(0, 25))
    return dict(rows=${obj_name}_list)


def select():
    ${obj_name}_instance = $obj_Name()
    ${obj_name}_list = ${obj_name}_instance.list_all('all', limitby=(0, 25))
    return dict(rows=${obj_name}_list)


def show():
# shows an individual record
    r_id = request.args(0)
    ${obj_name}_instance = $obj_Name()
    ${obj_name}_instance.dbget(r_id)
    vdict = ${obj_name}_instance.toview()
# processing for any hasOne fields
$$hasOneShow
$$hasManyShow
    return vdict


def create():
# create a new record, returns an empty form but with defaults
#
    ${obj_name}_instance = $obj_Name()
    vdict = ${obj_name}_instance.toview()
#    adict = ${obj_name}_address.toview()
#    vdict.update(adict)
# processing for any hasOne fields
$$hasOneCreate
$$hasManyCreate
    return vdict


def save():
# saves the record created or amended by the user
    ${obj_name}_instance = $obj_Name()
    ${obj_name}_instance.bindtotable(${obj_name}_instance.request.post_vars, True)
# validate and if correct save to database

    sid = ${obj_name}_instance.dbinsert()

    redirect(URL('show', args=sid))
    return


def amend():
#
    r_id = request.args(0)
    ${obj_name}_instance = $obj_Name()
    ${obj_name}_instance.dbget(r_id)
    session.amend_id = r_id
    vdict = ${obj_name}_instance.toview()
# processing for any hasOne fields
$$hasOneShow
$$hasManyShow
    return vdict


def update():
# first get the required record,
# then validate the new values
# finally if no errors, update with the amended values
    r_id = request.args(0)
    ${obj_name}_instance = $obj_Name()
    ${obj_name}_instance.dbget(r_id)
    ${obj_name}_instance.bindtotable(${obj_name}_instance.request.post_vars, True)
    sid = ${obj_name}_instance.dbupdate(r_id)
    redirect(URL('show', args=sid))
    return


def delete():
# deletes the given record - needed ?
    r_id = request.args(0)
    ${obj_name}_instance = $obj_Name()
    sid = ${obj_name}_instance.dbdelete(r_id)
    return sid


$$isMany