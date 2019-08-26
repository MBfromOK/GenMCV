__author__ = 'graham'


from gluon import current
from gluon.dal import DAL


class Smodel(object):

    def __init__(self):
        if hasattr(current, 'db'):
# use input db
            self.db = current.db
#        self.db = DAL("sqlite://mydb.sqlite")
            self.session = current.session
            self.request = current.request
            self.response = current.response
            self.cache = current.cache
        else:
            self.db = DAL(None)
#        print 'in constructor'
#        print self.db
        self.tablename = None
        self.define_table()
        self.set_validators()
        self.vars = self.setupvars()
        print 'end smodel const'

    def setupvars(self):
# just set up the names from the table's field definitions in 'self.newv' and initialise
#  to any default value as set in the field definition, note that the default default is 'None'
        newv = {}
        for f in self.table:
#            print 'field ' + f.name
            newv[f.name] = f.default
        return newv

    def bindtotable(self, datadict, include_object_names=True):
# sets the values in the dict 'self.vars' to the corresponding values in 'datadict'
# when handling user input the 'datadict' is the 'request.post_vars' while after a 'get'
# from the database it is the retrieved row
#
# include_object_name is used to deal with inputs from 'request.post_vars' which will have the
# object name prepended (e.g. object_field), this is to allow for different objects on a view form
# which therefore need to be differentiated easily when the request is received
#
# TODO need to add 'include' and 'exclude' list
        print 'in btt'
        for field in self.table:
            fname = field.name
            if include_object_names:
                vname = self.tablename + '_' + fname
            else:
                vname = fname
            if vname in datadict:
                field = datadict[vname]
                print field
                self.vars[fname] = field

    def toview(self, include_object_names=True):
# creates and returns a simple dict containing the name and value pairs derived from the values in self.vars
# this can then be used to send to a View.
# Currently if a table field (variable) is not present in 'self.vars' then it is given a blank
# value but this is not really correct - it should take the field's default value or not be included
# at all in the dict (not sure about the consequences of the latter)
#
# include_object_name is used to deal with outputs to views which will have the
# object name prepended (e.g. object_field), this is to allow for different objects on a view form
#
# TODO need to add 'include' and 'exclude' list
        viewdict = {}
        print 'smodel - toview'
        for field in self.table:
            fname = field.name
            if include_object_names:
                vname = self.tablename + '_' + fname
            else:
                vname = fname
#            print 'fname'
#            print fname
            if fname in self.vars:
                if self.vars[fname] is not None:
                    viewdict[vname] = self.vars[fname]
                else:
                    viewdict[vname] = ' '
            else:
                viewdict[vname] = ' '
#            if self.vars[fname]:
#                viewdict[fname] = self.vars[fname]
#            else:
#                viewdict[fname] = ' '
        print 'viewdict '
        print viewdict
        return viewdict

    def todb(self):
# creates and returns a simple dict containing the name and value pairs derived from the values in self.vars
# which can be used in the db insert
# note it just uses toview() (note the False so that the object name is not included) but deletes the
# entry for the db key 'id'
        dbdict = {}
        dbdict = self.toview(False)
        del dbdict['id']
        print 'end of todb'
        return dbdict

    def genview(self):
# generates and returns a piece of HTML that can be saved and used as a View file
# currently just creates simple minded text entry boxes
# TODO needs elaborating to deal with different types of fields
        viewhtml = '<fieldset>'
        for field in self.table:
            fname = field.name
# label
            viewhtml = viewhtml + "<label for = '" + fname + "'>"
            viewhtml = viewhtml + self.table[fname].label + ' : '
            viewhtml = viewhtml + "</label> "
# <input ...
            viewhtml = viewhtml + "<input id = '" + fname + "' name = '" + fname
            viewhtml = viewhtml + "' value='{{=" + fname + "}}'/>\n"
        viewhtml = viewhtml + '</fieldset>'
        return viewhtml

# database access methods

    def dbget(self, record_id):
        print 'in smodel dbget'
        suppget = self.db[self.tablename][record_id]
        print suppget
        self.bindtotable(suppget, False)
        return suppget

    def dbinsert(self):
        print 'in smodel dbins2'
        dbdict = self.todb()
        print 'after todb'
        print dbdict
        rid = self.db[self.tablename].insert(**dbdict)
        print rid
        return rid

    def dbupdate(self, record_id):
        print 'in smodel dbupdate'
        dbdict = self.todb()
        print 'after todb'
        self.db(self.db[self.tablename]._id==record_id).update(**dbdict)
        print record_id
        return record_id

    def dbdelete(self, record_id):
        print 'in smodel dbdelete'
#        dbdict = self.todb()
#        print 'after todb'
        self.db(self.db[self.tablename]._id==record_id).delete()
        print record_id
        return record_id


# the following are just placeholders for the methods that must be defined by the real object classes

    def define_table(self):
# contains the db table definitions e.g.:
#        self.table = self.db.define_table("branch",
#                Field("name"),
#                Field("description"),
#                Field('comments')
#         )
#
# a placeholder to be overridden in the real class
#        print 'in porm def tab'
#        print 'nothing to do end'
        return

    def set_validators(self):
# contains the definitaion of the field validations e.g.:
#        self.table.name.requires = IS_NOT_EMPTY()
#
# a placeholder to be overridden in the real class
#        print 'in PORM setval'
#        print 'end'
        return


