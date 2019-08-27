__author__ = 'graham'


from smodel import Smodel
from web2py.gluon.dal import Field
from web2py.gluon.validators import IS_NOT_EMPTY, IS_EMAIL, IS_LENGTH


class $obj_Name(Smodel):

    def __init__(self):
        Smodel.__init__(self)

    def define_table(self):
        self.table = self.db.define_table('$obj_name',
                Field('${obj_name}_name'),
#               etc.
                Field('comments'),
                format='%(${obj_name}_name)s'
        )
        self.tablename = '$obj_name'

    def set_validators(self):
        self.table.${obj_name}_name.requires = IS_NOT_EMPTY()

    def list_all(self, scope, limitby=None):
        queries = self.table.id>0
        return self.db(queries).select(limitby=limitby)

    def dbget(self, record_id):
        Smodel.dbget(self, record_id)
        return

    def dbinsert(self):
        rid = Smodel.dbinsert(self)
        return rid

    def dbupdate(self, record_id):
        rid = Smodel.dbupdate(self, record_id)
        return rid

    def dbdelete(self, record_id):
        rid = Smodel.dbdelete(self, record_id)
        return rid

# if the many of a hasMany---
# really ought to be optional but this skeleton is created before the hasMany/isOne etc. are added
# so *** DELETE if not on the many side of a one to many ***
    def dbget_all_for(self, owner, ownerid, scope, limitby=None):
        query = (self.table['ownerType'] == owner) & (self.table['ownerId'] == ownerid)
        return self.db(query).select(limitby=limitby)


