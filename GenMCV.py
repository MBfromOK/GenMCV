__author__ = 'graham'

from definitions import ROOT_DIR, CONFIG_PATH, SLASH
from configparser import ConfigParser
from itertools import chain, repeat
from string import Template
from pathlib import Path
import importlib
import sys
import os

# generator for web2py views
# in web2py the code should be in or run from the project's directory, ie the top level as created by PyCharm
#  the paths in the code take this location into account
# NOTE the templates directory should also be in the same location: /project/GenMCV/templates
#


config = ConfigParser()
print("======================================================================================================")
print("\nVerifying files are where they belong...")
if Path(CONFIG_PATH, 'config.ini').is_file():
    config.read(Path(CONFIG_PATH, 'config.ini'))
    osType = Path(config.get('Main', 'osType'))
    w2p_loc = Path(config.get('Web2Py', 'root'))
    w2p_fldr = Path(config.get('Web2Py', 'folder'))
    w2p_apps = Path(config.get('Web2Py', 'apps'))
    w2p_scripts = Path(config.get('Web2Py', 'scripts'))
    w2p_packs = Path(config.get('Web2Py', 'site-packages'))
    genMCV_loc = Path(config.get('GenMCV', 'root'))
    genMCV_fldr = Path(config.get('GenMCV', 'folder'))
    genMCV_templates = Path(config.get('GenMCV', 'templates'))
    print("\tConfig Loaded...\n")
    print("======================================================================================================")
else:
    print("\tNo Config file found...Building")
    config.read(CONFIG_PATH)
    config.add_section('Main')
    if SLASH == '\\':
        config.set('Main', 'osType', 'Windows')
    else:
        config.set('Main', 'osType', '*nix')
    config.add_section('Web2Py')
    if os.path.exists(ROOT_DIR + SLASH + 'web2py'):
        print('GenMCV found a web2py folder at: ' + ROOT_DIR + SLASH + 'web2py.')
        answers = {'y', 'n', ''}
        prompts = chain(['Would you like to use this folder? [Y/n]'],
                        repeat('Would you like to use ' + ROOT_DIR + SLASH + 'web2py? [Y/n]'))
        replies = map(input, prompts)
        w2p = next(filter(answers.__contains__, replies))
        if w2p == 'y' or w2p == '':
            config.set('Web2Py', 'root', ROOT_DIR + SLASH)
            config.set('Web2Py', 'folder', ROOT_DIR + SLASH + 'web2py')
            config.set('Web2Py', 'apps', ROOT_DIR + SLASH + 'web2py' + SLASH + 'applications')
            config.set('Web2Py', 'scripts', ROOT_DIR + SLASH + 'web2py' + SLASH + 'scripts')
            config.set('Web2Py', 'site-packages', ROOT_DIR + SLASH + 'web2py' + SLASH + 'site-packages')
        else:
            set_web2py_config(config)
    else:
        set_web2py_config(config)
    if os.path.exists(ROOT_DIR + SLASH + 'GenMCV'):
        print('GenMCV found a GenMCV folder at: ' + ROOT_DIR + SLASH + 'GenMCV')
        answers = {'y', 'n', ''}
        prompts = chain(['Would you like to use this folder? [Y/n]'],
                        repeat('Would you like to use ' + ROOT_DIR + SLASH + 'GenMCV? [Y/n]'))
        replies = map(input, prompts)
        GenMCV = next(filter(answers.__contains__, replies))
        if GenMCV == 'y' or GenMCV == '':
            config.set('GenMCV', 'root', ROOT_DIR + SLASH)
            config.set('GenMCV', 'folder', ROOT_DIR + SLASH + 'GenMCV' + SLASH)
            config.set('GenMCV', 'templates', ROOT_DIR + SLASH + 'GenMCV' + SLASH + 'templates' + SLASH)
        else:
            set_genmcv_config(config)
    else:
        set_genmcv_config(config)
    with open(CONFIG_PATH, 'w') as f:
        config.write(f)
    print("\t\tConfig File Created\n")
    print("======================================================================================================")


def set_web2py_config(config):
    w2p_path = input(
        'Please provide the full path to the web2py folder: '
        ' \n\t\tWARNING: Not Validated!!!'
    )
    if w2p_path[len(w2p_path) - len(SLASH):len(w2p_path)] != SLASH:
        config.set('Web2Py', 'root', w2p_path + SLASH)
        config.set('Web2Py', 'apps', w2p_path + SLASH + 'applications' + SLASH)
        config.set('Web2Py', 'scripts', w2p_path + SLASH + 'scripts' + SLASH)
        config.set('Web2Py', 'site-packages', w2p_path + SLASH + 'site-packages' + SLASH)
    else:
        config.set('Web2Py', 'root', w2p_path)
        config.set('Web2Py', 'apps', w2p_path + 'applications' + SLASH)
        config.set('Web2Py', 'scripts', w2p_path + 'scripts' + SLASH)
        config.set('Web2Py', 'site-packages', w2p_path + 'site-packages' + SLASH)


def set_genmcv_config(config):
    genMCV_script = input(
        'Please provide the full path to the GenMCV.py file: '
        ' \n\t\tWARNING: Not Validated!!!'
    )
    genMCV_path = input(
        'Please provide the full path to the GenMCV folder: '
        ' \n\t\tWARNING: Not Validated!!!'
    )
    if genMCV_path[len(genMCV_path)-len(SLASH):len(genMCV_path)] != SLASH:
        config.set('GenMCV', 'root', genMCV_script + SLASH)
        config.set('GenMCV', 'folder', genMCV_path + SLASH)
        config.set('GenMCV', 'templates', genMCV_path + SLASH + 'templates' + SLASH)
    else:
        config.set('GenMCV', 'root', genMCV_script)
        config.set('GenMCV', 'folder', genMCV_path)
        config.set('GenMCV', 'templates', genMCV_path + 'templates')


class objData(object):
    def __init__(self, appl_name, object_name):
        sys.path.append('.' + SLASH + 'web2py')
        self.app_root = SLASH + appl_name + SLASH
        self.appl_file_path = '.' + SLASH + 'web2py' + SLASH + 'applications' + SLASH + appl_name + SLASH
        self.obj_name = object_name
        self.obj_Name = self.obj_name[0].upper() + self.obj_name[1:]
#    obj_Name = obj_name.capitalize()
        self.obj_imp = importlib.import_module('applications.' + appl_name + '.modules.' + self.obj_name)
        self.obj_local = getattr(self.obj_imp, self.obj_Name)
        self.obj_instance = self.obj_local()
        self.tname = self.obj_instance.tablename
#
        if hasattr(self.obj_instance, 'hasOne') and len(self.obj_instance.hasOne) > 0:
            self.hasOneflag = True
        else:
            self.hasOneflag = False
        if hasattr(self.obj_instance, 'hasMany') and len(self.obj_instance.hasMany) > 0:
            self.hasManyflag = True
        else:
            self.hasManyflag = False
        if hasattr(self.obj_instance, 'isMany'):
            self.isManyflag = True
        else:
            self.isManyflag = False


def makehmfields(appl_name, oname, hname, hName):
# common creation of hasMany table of fields for formdata and show html files
    hobj_imp = importlib.import_module('applications.' + appl_name + '.modules.' + hname)
    hobj_local = getattr(hobj_imp, hName)
    hobj_inst = hobj_local()
    hmf_str = []
    hmf_str.append("""\
{{if """ + oname + '_' + hname + """_rowscount > 0:}}
    <table>
        <thead>
        <tr>
""")
    j = 1
    for field in hobj_inst.table:
        hmf_str.append("""\
            <td>""" + hobj_inst.table[field.name].label + "</td>\n")
        j = j + 1
    hmf_str.append("""\
        </tr>
        </thead>
        <tbody>
{{for arow in """ + oname + '_' + hname + """_rows:}}
        <tr>
""")
    j = j + 1
    for field in hobj_inst.table:
        if field.name == 'id':
            hmf_str.append("""\
            <td class="objid">{{=arow['id']}}</td>\n""")
        elif field.name == hname + '_name':
            hmf_str.append("""\
            <td class="objname">{{=arow['""" + field.name + "']}}</td>\n""")
        else:
            hmf_str.append("""\
            <td>{{=arow['""" + field.name + "']}}</td>\n")
        j = j + 1
#
    hmf_str.append("""\
        </tr>
{{pass}}
        </tbody>
    </table>
{{else:}}
None defined
{{pass}}
""")
    print('hmf str')
    print(hmf_str)
    return hmf_str



def gview(appl_name, object_name):
# first get the relevant class object
# todo - note that path is hard-coded for the moment,
# as is the object name
#    print(sys.path)
# use objData
    objD = objData(appl_name, object_name)
    app_root = objD.app_root
    appl_file_path = objD.appl_file_path
    obj_name = object_name
    obj_Name = objD.obj_Name
    hasOneflag = objD.hasOneflag
    hasManyflag = objD.hasManyflag
    isManyflag = objD.isManyflag
    obj_instance = objD.obj_instance
    tname = objD.tname

#
#    sys.path.append('./web2py')
#    app_root = '/' + appl_name + '/'
#    appl_file_path = './web2py/applications/' + appl_name + '/'
#    obj_name = object_name
#    obj_Name = obj_name[0].upper() + obj_name[1:]
#    obj_imp = importlib.import_module('applications.' + appl_name + '.modules.' + obj_name)
#    obj_local = getattr(obj_imp, obj_Name)
#    obj_instance = obj_local()
#    tname = obj_instance.tablename
##
#    if hasattr(obj_instance, 'hasOne') and len(obj_instance.hasOne) > 0:
#        hasOneflag = True
#    else:
#        hasOneflag = False
#    if hasattr(obj_instance, 'hasMany') and len(obj_instance.hasMany) > 0:
#        hasManyflag = True
#    else:
#        hasManyflag = False
#
# first check is the model's sub=directory in views exists, create it if not...
#
    outdir = appl_file_path + 'views' + SLASH + tname
    try:
        os.makedirs(outdir, exist_ok=True)
    except FileExistsError:
        # directory already exists
        pass
#
# 1. list: this is just a list of the objects
# -------------------------------------------------
#
    list_str1_1 = []
    list_str1_1.append("""\
<div>
""")
    list_str1_2 = []
    list_str1_2.append("    <h3>List of " + obj_Name + """</h3>
""")
    list_str1_3 = []
    list_str1_3.append("""\
<script>
    $(function() {
        $("table").on("click", ".objid", function () {
            var aid = $(this).html();
            var url = '""" + app_root + obj_name + """/show/' + aid;
            alert("url " + url);
            if (""" + obj_name + """LoadedFromSelect) {
                var aname = $(this).siblings(".objname").html();
                alert(" select name " + aname);
                """ + obj_name + """Selected = true;
                update""" + obj_Name + """(aid, aname);
            }
            else {
                $.get(url, function(data){$('#""" + obj_name + """Div').html(data)});
            };
            return false;
        });
        if (""" + obj_name + """LoadedFromSelect) {
            $('#cancelbutton""" + obj_Name + """').css('display', 'inline');
        }
        else {
            $('#cancelbutton""" + obj_Name + """').css('display', 'none');
        }
    })
</script>
""")
    list_str2 = []
    list_str2.append("""\
<fieldset>
    <button name="create" value="create"
            onclick="$.get('""" + app_root + obj_name + "/create', function(getdata){$('#" + obj_name + """Div').html(getdata)});return false;">CREATE</button>
    <button name="cancel" value="cancel" id="cancelbutton""" + obj_Name + """"
            onclick="cancel""" + obj_Name + """(); return false;" style="display: none">CANCEL</button>
""")
    list_str2_2 = []
    list_str2_2.append("""
</fieldset>
""")
    list_str = []
    list_str.append("""\
<fieldset>
    <table>
        <thead>
        <tr>
""")
    j = 1
    for field in obj_instance.table:
        list_str.append("""\
            <td>""" + obj_instance.table[field.name].label + "</td>\n")
        j = j + 1
    list_str.append("""\
        </tr>
        </thead>
        <tbody>
{{for arow in rows:}}
        <tr>
""")
    j = j + 1
    for field in obj_instance.table:
        if field.name == 'id':
            list_str.append("""\
            <td class="objid">{{=arow['id']}}</td>\n""")
        elif field.name == obj_name + '_name':
            list_str.append("""\
            <td class="objname">{{=arow['""" + field.name + "']}}</td>\n""")
        else:
            list_str.append("""\
            <td>{{=arow['""" + field.name + "']}}</td>\n")
        j = j + 1
#
    list_str.append("""\
        </tr>
{{pass}}
        </tbody>
    </table>
</fieldset>
""")
    list_str4 = []
    list_str4.append("""\
</div>
""")
#
#    print('list-str')
#    print(list_str)
#    viewfile = open('../templates/views/index.html', 'r')
#    view = viewfile.read()
    outfile = open(appl_file_path + 'views' + SLASH + tname + SLASH + 'list.html', 'w')
    for ent in list_str1_1:
        outfile.write(ent)
    for ent in list_str1_2:
        outfile.write(ent)
    for ent in list_str1_3:
        outfile.write(ent)
    for ent in list_str2:
        outfile.write(ent)
    for ent in list_str2_2:
        outfile.write(ent)
    for ent in list_str:
        outfile.write(ent)
    for ent in list_str4:
        outfile.write(ent)
    outfile.close()

#
# 1b. index: the initial and full page reload html page
# ------------------------------------------------------
#
    index_str = []
    index_str.append("""\
{{extend 's3layout.html'}}
<script>
var """ + obj_name + """LoadedFromSelect = false;
var """ + obj_name + """LoadedFromOwner = false;
</script>
<div id='""" + obj_name + """Div'>
{{include '""" + obj_name + """/list.html'}}
</div>""")

    outfile = open(appl_file_path + 'views' + SLASH + tname + SLASH + 'index.html', 'w')
#    outfile = open('./web2py/applications/plants/views/' + tname + '/index.html', 'w')
    for ent in index_str:
        outfile.write(ent)
    outfile.close()

#
# 1c. select:
# -------------------------------------------------------------------------------------------------------
# to allow selection of object, usually called from another module; almost the same as 'list', so uses
# parts of the 'list' text plus its own Javascript to action the 'select'
#
    select_str1_1 = []
    select_str1_1.append("""\
<script>
var """ + obj_name + """LoadedFromSelect = true;
</script>
""")
    select_str1_2 = []
    select_str1_2.append("""    <fieldset>
    <legend>Select (or create) """ + obj_Name + """</legend>
""")
#    select_str2 = []
#    select_str2.append("""\
#    <button name="cancel" value="cancel"
#            onclick='""" + "cancel" + obj_Name + """Id();return false;'>CANCEL</button>
#""")

    select_str4 = []
    select_str4.append("""\
</fieldset>
</div>
""")
    outfile = open(appl_file_path + 'views' + SLASH + tname + SLASH + 'select.html', 'w')
#    outfile = open('./web2py/applications/plants/views/' + tname + '/index.html', 'w')
    for ent in select_str1_1:
        outfile.write(ent)
    for ent in list_str1_1:
        outfile.write(ent)
    for ent in select_str1_2:
        outfile.write(ent)
    for ent in list_str1_3:
        outfile.write(ent)
    for ent in list_str2:
        outfile.write(ent)
#    for ent in select_str2:
#        outfile.write(ent)
    for ent in list_str2_2:
        outfile.write(ent)
    for ent in list_str:
        outfile.write(ent)
    for ent in select_str4:
        outfile.write(ent)
    outfile.close()

#
# 2. formdata:
# ------------
# this is the basic entry/amend data entry structure, the various 'input' tags but without
# the 'form' tag and buttons, these are provided by the modules that use formdata namely 'create' and 'amend'
#
# NOTE that ho_div_str holds <div>...</div> entries for any hasOne fields but is not used in the
# formdata.html but in the later create and amend.html files
#
    default_len = 32
    fd_str = []
    fd_str2 = []
    fd_str3 = []
    ho_div_str = []
    for field in obj_instance.table:
        if field.name != 'id':
            if obj_instance.table[field.name].type == 'string':
                f_len = obj_instance.table[field.name].length if obj_instance.table[field.name].length else default_len
            elif obj_instance.table[field.name].type == 'integer':
                f_len = 10
            fname_on_page = tname + "_" + field.name
            if (not hasOneflag) or not (field.name in obj_instance.hasOne):
                fd_str.append("<div>\n")
                fd_str.append("<label for='" + fname_on_page + "' class='col_2'>\n")
                fd_str.append(obj_instance.table[field.name].label + "\n")
                fd_str.append("</label>\n")
                fd_str.append("<input id='" + fname_on_page + "'")
                fd_str.append(" name='" + fname_on_page + "'")
                if obj_instance.table[field.name].type == 'boolean':
                    fd_str.append(" type='checkbox' {{if " + fname_on_page + ":}}checked {{pass}}")
                else:
                    fd_str.append(" maxlength='" + str(f_len) + "'")
                fd_str.append(" value='{{=" + fname_on_page + "}}' class='col_4'>\n")
                fd_str.append("</div>\n")
            elif hasOneflag and field.name in obj_instance.hasOne:
# if a 'hasOne' entry then the field must be called 'othertablename' and we need to generate two <input>
# one for the id of the other table record (which is populated but 'hidden') and another that holds the name
# on that record, this is visible but 'readonly'
                f_len = 10
                fd_str.append("<script>var popsel" + field.name + "= new jBox('Modal',{\n")
                fd_str.append("    minWidth: 600,\n")
                fd_str.append("    reposition: true,\n")
                fd_str.append("    repositionOnContent: true,\n")
                fd_str.append("    repositionOnOpen: true\n")
                fd_str.append("});\n")
                fd_str.append("function update" + field.name[0].upper() + field.name[1:] + "(newId, newName){\n")
                fd_str.append("if (" + field.name + "Selected) {\n")
                fd_str.append("$('#" + fname_on_page + "').val(newId);\n")
                fd_str.append("$('#" + fname_on_page + "_name').val(newName);\n")
                fd_str.append("popsel" + field.name + ".close();\n")
#                fd_str.append("$('#" + field.name + "Div').hide();\n")
                fd_str.append("}\n}\n")
                fd_str.append("function cancel" + field.name[0].upper() + field.name[1:] + "(){\n")
                fd_str.append("popsel" + field.name + ".close();\n")
#                fd_str.append("$('#" + field.name + "Div').hide();\n")
                fd_str.append("}\n")
                fd_str.append("function dopopsel" + field.name[0].upper() + field.name[1:] + "(){\n")
                fd_str.append("$.get('" + app_root + field.name + "/select', function(getdata){\n")
                fd_str.append("    $('#" + field.name + "Div').html(getdata);\n")
                fd_str.append("popsel" + field.name + ".setContent($('#" + field.name + "Div'));\n")
                fd_str.append("popsel" + field.name + ".position();\n")
                fd_str.append("popsel" + field.name + ".open();\n")
                fd_str.append("});\n")
                fd_str.append("}\n")
#
                fd_str.append("var " + field.name + "Selected = false;\n")
                fd_str.append("var " + field.name + "Id = 0;\n")
                fd_str.append("</script>\n")
                fd_str.append("<div>\n<label for='" + fname_on_page + "' class='col_2'>\n")
                fd_str.append("{{if " + fname_on_page + "  == 0:}}\n")
                fd_str.append(obj_instance.table[field.name].label + " - select\n")
                fd_str.append("{{else:}}\n")
                fd_str.append(obj_instance.table[field.name].label + " - re-select or remove\n")
                fd_str.append("{{pass}}\n")
                fd_str.append("</label>\n")
                fd_str.append("<input id='" + fname_on_page + "'")
                fd_str.append(" name='" + fname_on_page + "'")
                fd_str.append(" maxlength='" + str(f_len) + "'")
                fd_str.append(" value='{{=" + fname_on_page + "}}' type='hidden'>\n")
                fd_str.append("<input id='" + fname_on_page + "_name'")
                fd_str.append(" name='" + fname_on_page + "_name'")
                fd_str.append(" maxlength='" + str(f_len) + "'")
                fd_str.append(" value='{{=" + fname_on_page + "_name}}' READONLY class='col_4'>\n")
                fd_str.append("{{if " + fname_on_page + "  == 0:}}\n")
                fd_str.append("<button name='select' value='select'\n")
                fd_str.append("""onclick="dopopsel""" + field.name[0].upper() + field.name[1:] + "();")
#                fd_str.append("""onclick="$.get('""" + app_root + field.name + """/select', """)
#                fd_str.append("""function(getdata){$('#""" + field.name + """Div').html(getdata)});""")
                fd_str.append("""return false;">SELECT</button>\n""")
                fd_str.append("{{else:}}\n")
                fd_str.append("<button name='select' value='select'\n")
                fd_str.append("""onclick="dopopsel""" + field.name[0].upper() + field.name[1:] + "();")
                fd_str.append("""return false;">SELECT</button>\n""")
#                fd_str.append("""onclick="$.get('""" + app_root + field.name + """/select', """)
#                fd_str.append("""function(getdata){$('#""" + field.name + """Div').html(getdata)});""")
#                fd_str.append("""$('#""" + field.name + """Div').show();return false;">SELECT</button>\n""")
                fd_str.append("<button name='remove' value='remove'\n")
                fd_str.append("""onclick="$('#""" + fname_on_page + """').val('0');return false;">REMOVE</button>\n""")
                fd_str.append("{{pass}}\n")
                fd_str.append("</div>\n")
                ho_div_str.append("<div id='" + field.name + "Div' style='display: none'>\n</div>\n")
# now check for hasMany - not set up as separate fields but in the hasMany list
    fd_strhm = []
    if hasManyflag:
        for hmname in obj_instance.hasMany:
            hmName = hmname[0].upper() + hmname[1:]
            print('hasmany ')
            print(hmName)
            fd_strhm.append("""\
<!--- hasMany --->
<div>
<script>
if (typeof """ + obj_name + hmname + """Loaded == 'undefined'){
// if not already loaded then create the vars and define the functions
    var """ + obj_name + hmname + """Loaded = true;
    var owner_type = '""" + obj_name + """';
    var owner_id = '{{=""" + obj_name + """_id}}';
    var """ + hmname + """LoadedFromOwner = true;
    var """ + hmname + """ReloadNeeded = false;
    var popOwned""" + hmName + """;
    var pop""" + obj_Name + hmName + """;
    var cancelPoppedOwner""" + hmName + """;
    var doPopOwner""" + hmName + """;
    function cancel""" + obj_Name + hmName + """(){
        pop""" + obj_Name + hmName + """.close();
    }
    function dopop""" + obj_Name + hmName + """(){
        $.post('""" + app_root + hmname + "/get_all_for_owner', {ownerType: '" + obj_name + """', ownerId: owner_id}, function(getdata){
            $('#""" + obj_name + hmname + """Div').html(getdata);
        pop""" + obj_Name + hmName + ".setContent($('#" + obj_name + hmname + """Div'));
        pop""" + obj_Name + hmName + ".setTitle('Showing all " + hmname + "s for " + obj_name + """ ' + owner_id);
        pop""" + obj_Name + hmName + """.position();
        pop""" + obj_Name + hmName + """.open();
        });
    }
}
if (typeof pop""" + obj_Name + hmName + """!= 'object') {
    pop""" + obj_Name + hmName + """ = new jBox('Modal',{
        title: '""" + hmname + """',
        minWidth: 600,
        reposition: true,
        repositionOnContent: true,
        repositionOnOpen: true,
        draggable: 'title',
        dragOver: true,
        target: '""" + obj_name + hmname + """Div'
    });
}
// and then the assignments for this (re-)load
owner_type = '""" + obj_name + """';
owner_id = '{{=""" + obj_name + """_id}}';
""" + hmname + """LoadedFromOwner = true;
""" + hmname + """ReloadNeeded = false;
cancelPoppedOwner""" + hmName + """ = cancel""" + obj_Name + hmName + """;
doPopOwner""" + hmName + """ = dopop""" + obj_Name + hmName + """;

</script>
<fieldset>
<legend>""" + hmName + """</legend>
<label class='col_2'>""" + hmName + """</label>
<button name='amend_""" + hmname + "' value='amend_" + hmname + """'
 onclick="dopop""" + obj_Name + hmName + """();return false;">Amend """ + hmName + """</button>
""")
#  ************************* the hasMany's fields go here
#            tests = makehmfields(appl_name, obj_name, hmname, hmName)
#            print(tests)
#            fd_str2.append(tests)
            fd_strhm.append(makehmfields(appl_name, obj_name, hmname, hmName))
            fd_strhm.append("""\
</fieldset>
</div>
<div id='""" + obj_name + hmname + """Div' style='display: none'></div>
""")
    outfile = open(appl_file_path + 'views' + SLASH + tname + SLASH + 'formdata.html', 'w')
    for ent in fd_str:
        outfile.write(ent)
    for ent in fd_strhm:
        if isinstance(ent, str):
            outfile.write(ent)
        elif isinstance(ent, list):
#            print(ent)
            for lent in ent:
#                print('in lent ')
#                print(lent)
                outfile.write(lent)
            else:
                print('error')
#    for ent in fd_str3:
#        outfile.write(ent)
#    outfile.close()

#
# 3. create: the basic entry form which uses the formdata component
# -----------------------------------------------------------------
#
    cr_str = []
    cr_str.append("""\
<h3>Create  """)
    cr_str.append(obj_Name + """</h3>
<div>""")
    if isManyflag:
        cr_str.append("""
<script>
$(function() {
    if (""" + obj_name + """LoadedFromOwner) {
        $('#cancelcreate""" + obj_name + """button').css('display', 'none');
        $('#returncreate""" + obj_name + """button').css('display', 'inline')
    }
})
</script>""")
    cr_str.append("""
    <form id='""" + obj_name + """Form'>
    <fieldset>
    {{include '""" + obj_name + """/formdata.html'}}
    </fieldset>
    <fieldset>
        <button name="save" value="save"
            onclick="$.post('""" + app_root + obj_name + "/save', $('#" + obj_name + "Form').serialize(), function(postdata){$('#" + obj_name + """Div').html(postdata)});return false;">SAVE</button>
        <button name='cancel' value='cancel' id='cancelcreate""" + obj_name + """button'
            onclick="$.get('""" + app_root + obj_name + "/list', function(getdata){$('#" + obj_name + """Div').html(getdata)});return false;">CANCEL</button>
""")
    if isManyflag:
        cr_str.append("""\
        <button name='return' value='return' id='returncreate""" + obj_name + """button' style='display: none'
            onclick="cancelOwned""" + obj_Name + """();return false;">RETURN without saving</button>
""")
    cr_str.append("""\
    </fieldset>
    </form>
""")
    cr_str2 = []
    cr_str2.append("""\
</div>
""")

    outfile = open(appl_file_path + 'views' + SLASH + tname + SLASH + 'create.html', 'w')
    for ent in cr_str:
        outfile.write(ent)
    for ent in ho_div_str:
        outfile.write(ent)
    for ent in cr_str2:
        outfile.write(ent)
    outfile.close()

#
# 4. amend:
#  --------
# uses the same entry form but the action is different (and, of course, is filled with the
# existing values when first displayed)
#
    am_str = []
    am_str.append("""\
<h3>Amend  """)
    am_str.append(obj_Name + """</h3>
<div>""")
    if isManyflag:
        am_str.append("""
<script>
$(function() {
    if (""" + obj_name + """LoadedFromOwner) {
        $('#cancelamend""" + obj_name + """button').css('display', 'none');
        $('#returnamend""" + obj_name + """button').css('display', 'inline')
    }
})
</script>""")
    am_str.append("""
    <form id='""" + obj_name + "AmendForm'>")
    am_str.append("""
    <fieldset>
        {{include '""" + obj_name + """/formdata.html'}}
    </fieldset>
    <fieldset>
        <button name="update" value="update"
            onclick="$.post('""" + app_root + obj_name + "/update/{{=" + obj_name + "_id}}', $('#" + obj_name + "AmendForm').serialize(), function(postdata){$('#" + obj_name + """Div').html(postdata)});return false;">UPDATE</button>
        <button name='cancel' value='cancel' id='cancelamend""" + obj_name + """button'
            onclick="$.get('""" + app_root + obj_name + "/list', function(getdata){$('#" + obj_name + """Div').html(getdata)});return false;">CANCEL</button>
""")
    if isManyflag:
        am_str.append("""\
        <button name='return' value='return' id='returnamend""" + obj_name + """button' style='display: none'
            onclick="cancelOwned""" + obj_Name + """();return false;">RETURN without saving</button>
""")
    am_str.append("""\
    </fieldset>
    </form>
""")
    am_str2 = []
    am_str2.append("""\
</div>
""")

    outfile = open(appl_file_path + 'views' + SLASH + tname + SLASH + 'amend.html', 'w')
    for ent in am_str:
        outfile.write(ent)
    for ent in ho_div_str:
        outfile.write(ent)
    for ent in am_str2:
        outfile.write(ent)
    outfile.close()

#
# 5. show
# -------
# essentially a read-only version of the create/amend page but, of course, not in a form so
# we have to create another file
#
    sh_str = []
    sh_str.append("""\
<h3>""" + obj_Name + """</h3>
<div>
<script>
    $(function() {
        if (""" + obj_name + """LoadedFromSelect) {
            $('#select""" + obj_name + """button').css('display', 'inline');
            $('#list""" + obj_name + """button').css('display', 'none');
        }
        else {
            $('#select""" + obj_name + """button').css('display', 'none');
            $('#list""" + obj_name + """button').css('display', 'inline');
        }
""")
    if isManyflag:
        sh_str.append("""
    if (""" + obj_name + """LoadedFromOwner) {
        $('#list""" + obj_name + """button').css('display', 'none');
        $('#returnshow""" + obj_name + """button').css('display', 'inline')
    }
""")
    sh_str.append("""\
})
</script>
<fieldset>
<button name='list' value='list' id='list""" + obj_name + """button'
    onclick="$.get('""" + app_root + obj_name + "/list', function(getdata){$('#" + obj_name + """Div').html(getdata)});return false;">LIST</button>
<button name='select' value='select' id='select""" + obj_name + """button' style='display: none'
    onclick="$.get('""" + app_root + obj_name + "/select', function(getdata){$('#" + obj_name + """Div').html(getdata)});return false;">SELECT FROM LIST</button>
<button name='amend' value='amend'
    onclick="$.get('""" + app_root + obj_name + "/amend/{{=" + obj_name + "_id}}', function(getdata){$('#" + obj_name + """Div').html(getdata)});return false;">AMEND</button>
""")
    if isManyflag:
        sh_str.append("""\
<button name='return' value='return' id='returnshow""" + obj_name + """button' style='display: none'
    onclick="closeOwned""" + obj_Name + """();return false;">RETURN</button>
""")
    sh_str.append("""\
</fieldset>
<fieldset>
""")
    for field in obj_instance.table:
        default_len = 32
        if field.name != 'id':
            if obj_instance.table[field.name].type == 'string':
                f_len = obj_instance.table[field.name].length if obj_instance.table[field.name].length else default_len
            elif obj_instance.table[field.name].type == 'integer':
                f_len = 10
            fname_on_page = tname + "_" + field.name
            sh_str.append("<div>\n")
            sh_str.append("<label for='" + fname_on_page + "' class='col_2'>\n")
            sh_str.append(obj_instance.table[field.name].label + "\n")
            sh_str.append("</label>\n")
            sh_str.append("<input READONLY ")
            if obj_instance.table[field.name].type == 'boolean':
                sh_str.append(" type='checkbox' {{if " + fname_on_page + ":}}checked {{pass}}")
            else:
                sh_str.append(" maxlength='" + str(f_len) + "'")
            if (not hasOneflag) or not (field.name in obj_instance.hasOne):
                sh_str.append(" id='" + fname_on_page + "'")
                sh_str.append(" name='" + fname_on_page + "'")
                sh_str.append(" value='{{=" + fname_on_page + "}}' class='col_4'>\n")
            else:
                sh_str.append(" id='" + fname_on_page + "_name'")
                sh_str.append(" name='" + fname_on_page + "_name'")
                sh_str.append(" value='{{=" + fname_on_page + "_name}}' class='col_4'>\n")
            sh_str.append("</div>\n")
# ************** hasMany's fields go here - see also formdata
    if hasManyflag:
        for hmname in obj_instance.hasMany:
            hmName = hmname[0].upper() + hmname[1:]
            sh_str.append("""<div>
<label class='col_2'>""" + hmname + """</label>
""")
            sh_str.append(makehmfields(appl_name, obj_name, hmname, hmName))

            sh_str.append("""</div>
""")

    sh_str.append("""</fieldset>
</div>
""")
    outfile = open(appl_file_path + 'views' + SLASH + tname + SLASH + 'show.html', 'w')
    for ent in sh_str:
#        print(type(ent))
        if isinstance(ent, str):
            outfile.write(ent)
        elif isinstance(ent, list):
#            print(ent)
            for lent in ent:
#                print('in lent ')
#                print(lent)
                outfile.write(lent)
            else:
                print('error')


    outfile.close()

#
# 6. get_all_for_owner
# --------------------
# Only available when the object is on the many side of a one to many relationship and this HTML
# sets up the Many side's entry for subsequent processing (if required)
#
    if isManyflag:
        gafo_str = []
        gafo_str.append("""\
<div id='""" + obj_name + """Div' style='display: none'></div>
<h3>Showing all """ + obj_Name + """s for {{=ownerType}} {{=ownerId}}</h3>
<script>
""" + obj_name + """LoadedFromOwner = true;
""" + obj_name + """ReloadNeeded = false;
$(function() {
    """ + obj_name + """LoadedFromOwner = true;
    """ + obj_name + """ReloadNeeded = false;
    if (""" + obj_name + """LoadedFromOwner) {
        $('#returnbutton""" + obj_Name + """').css('display', 'inline');
        $('#refreshbutton""" + obj_Name + """').css('display', 'inline');
    }
    if (typeof popOwned""" + obj_Name + """ != 'object') {
// only create this jBox once
        popOwned""" + obj_Name + """ = new jBox('Modal', {
            title: '""" + obj_name + """',
            minWidth: 600,
            reposition: true,
            repositionOnContent: true,
            repositionOnOpen: true,
            draggable: 'title',
            dragOver: true,
            target: '""" + obj_name + """Div'
        });
    };
});

if (typeof """ + obj_name + """Loaded == 'undefined') {
// if not already loaded then create variables and functions
    var """ + obj_name + """Loaded = true;
    var lownertype = '';
    var lownerid = '';

    function cancelOwned""" + obj_Name + """(){
        popOwned""" + obj_Name + """.close();
    }
    function closeOwned""" + obj_Name + """(){
        popOwned""" + obj_Name + """.close();
        """ + obj_name + """ReloadNeeded = true;
    }
    function doPopOwned""" + obj_Name + "(action, " + obj_name + """_id) {
        var """ + obj_name + "url = '" + app_root + obj_name + """/' + action;
        if (action == 'amend' ||
                action == 'delete') {
            """ + obj_name + "url += '/' + " + obj_name + """_id;
            $.get(""" + obj_name + """url, function (getdata) {
                $('#""" + obj_name + """Div').html(getdata);
                popOwned""" + obj_Name + ".setContent($('#""" + obj_name + """Div'));
                popOwned""" + obj_Name + ".setTitle('""" + obj_Name + " ' + " + obj_name + """_id);
                popOwned""" + obj_Name + """.position();
                popOwned""" + obj_Name + """.open();
            });
        }
        else {
            """ + obj_name + """url += '_owned';
            $.post(""" + obj_name + """url, {ownerType: '{{=ownerType}}', ownerId: '{{=ownerId}}'}, function (getdata) {
                $('#""" + obj_name + """Div').html(getdata);
                popOwned""" + obj_Name + ".setContent($('#""" + obj_name + """Div'));
                popOwned""" + obj_Name + ".setTitle('new """ + obj_Name + """');
                popOwned""" + obj_Name + """.position();
                popOwned""" + obj_Name + """.open();
            });
        }
    }
}
lownertype = '{{=ownerType}}';
lownerid = '{{=ownerId}}';
</script>
<div>
    <button name='add""" + obj_name + "' value='add" + obj_name + """'
            onclick="doPopOwned""" + obj_Name + """('create', '0');return false;">ADD """ + obj_Name + """</button>
    <button name="return" value="return" id='returnbutton""" + obj_Name + """'
            onclick="cancelPoppedOwner""" + obj_Name + """(); return false;" style="display: none">RETURN</button>
    <button name="refresh" value="refresh" id='refreshbutton""" + obj_Name + """'
            onclick="doPopOwner""" + obj_Name + """(); return false;" style="display: none">REFRESH</button>
<fieldset>
    <table>
        <thead>
        <tr>
""")
        j = 1
        for field in obj_instance.table:
            gafo_str.append("""\
            <td>""" + obj_instance.table[field.name].label + "</td>\n")
            j = j + 1
        gafo_str.append("""\
        </tr>
        </thead>
        <tbody>
{{for arow in rows:}}
        <tr>
""")
        j = j + 1
        for field in obj_instance.table:
            gafo_str.append("""\
            <td>{{=arow['""" + field.name + """']}}</td>
""")
        gafo_str.append("""\
            <td><button name='amend' value='amend'
onclick="doPopOwned""" + obj_Name + """('amend', '{{=arow['id']}}'); return false;">Amend</button>
</td>
            <td><button name='delete' value='delete'
onclick="doPopOwned""" + obj_Name + """('delete', '{{=arow['id']}}'); return false;">Delete</button>
</td>
        </tr>
{{pass}}
        </tbody>
    </table>
</fieldset>
</div>
""")

        outfile = open(appl_file_path + 'views' + SLASH + tname + SLASH + 'get_all_for_owner.html', 'w')
        for ent in gafo_str:
            outfile.write(ent)
        outfile.close()
    return

def gcontr(appl_name, object_name):
    objD = objData(appl_name, object_name)
    lobj_n = object_name
    lobj_N = objD.obj_Name
#    lobj_N = object_name.capitalize()
    cfile = open('.' + SLASH + 'GenMCV' + SLASH + 'templates' + SLASH + 'controller.py', 'r')
    outfile = open('.' + SLASH + 'web2py' + SLASH + 'applications' + SLASH + appl_name + SLASH + 'controllers' + SLASH + object_name + '.py', 'w')
    cont = cfile.read()
    fields_to_use = dict(obj_name=lobj_n, obj_Name=lobj_N)
    g1controller = Template(cont).substitute(fields_to_use)
#    print(gcontroller)
# now deal with hasOnes....
    hasOneflag = objD.hasOneflag
    hasManyflag = objD.hasManyflag
    isManyflag = objD.isManyflag
    obj_instance = objD.obj_instance
    hOShow = ' '
    hOCreate = ' '
    hOimports = []
    print(hOShow)
    if hasOneflag:
        hasOneindex = 0
        hOfields = dict(obj_name=lobj_n)
        hOfile = open('.' + SLASH + 'GenMCV' + SLASH + 'templates' + SLASH + 'hasOneShow.py', 'r')
        hOdata = hOfile.read()
        hOShow = Template(hOdata).substitute(hOfields)
        hOfile.close()
        print(hOShow)
        hOCfile = open('.' + SLASH + 'GenMCV' + SLASH + 'templates' + SLASH + 'hasOneCreate.py', 'r')
        hOCdata = hOCfile.read()
        hOCreate = Template(hOCdata).substitute(hOfields)
        hOCfile.close()
        print(hOCreate)
        for hO in obj_instance.hasOne:
            HO = hO[0].upper() + hO[1:]
            print(hOimports)
            hOimports.append("from " + hO + " import " + HO)
#            horeplace = dict(hasOneimports=hOimports, hasOneShow="the cat sat on the mat")
        hOimpall = '\n'.join(hOimports)
        horeplace = dict(hasOneimports=hOimpall, hasOneShow=hOShow, hasOneCreate=hOCreate)
    else:
        horeplace = dict(hasOneimports='', hasOneShow='', hasOneCreate='')
#
# and hasMany
    hMShow = ' '
    hMCreate = ' '
    hMimports = []
    if hasManyflag:
        hasManyindex = 0
        hMfields = dict(obj_name=lobj_n)
        hMfile = open('.' + SLASH + 'GenMCV' + SLASH + 'templates' + SLASH + 'hasManyShow.py', 'r')
        hMdata = hMfile.read()
        hMShow = Template(hMdata).substitute(hMfields)
        hMfile.close()
        print(hMShow)
        hMCfile = open('./gener/templates/hasManyCreate.py', 'r')
        hMCdata = hMCfile.read()
        hMCreate = Template(hMCdata).substitute(hMfields)
        hMCfile.close()
        print(hMCreate)
        for hM in obj_instance.hasMany:
            HM = hM[0].upper() + hM[1:]
            print(hMimports)
            hMimports.append("from " + hM + " import " + HM)
#            horeplace = dict(hasOneimports=hOimports, hasOneShow="the cat sat on the mat")
        hMimpall = '\n'.join(hMimports)
        hmreplace = dict(hasManyimports=hMimpall, hasManyShow=hMShow, hasManyCreate=hMCreate)
    else:
        hmreplace = dict(hasManyimports='', hasManyShow='', hasManyCreate='')
    horeplace.update(hmreplace)
#
# and is object is an owned in one to many
    iMany = ' '
    if isManyflag:
        isManyfields = dict(obj_name=lobj_n, obj_Name=lobj_N)
        iMfile = open('.' + SLASH + 'GenMCV' + SLASH + 'templates' + SLASH + 'isMany.py', 'r')
        iMdata = iMfile.read()
        iMany = Template(iMdata).substitute(isManyfields)
        iMfile.close()
        print(iMany)
        imreplace = dict(isMany=iMany)
    else:
        imreplace = dict(isMany='')

    horeplace.update(imreplace)
#
    g2controller = Template(g1controller).substitute(horeplace)
    outfile.write(g2controller)
    outfile.close()
    cfile.close()
    print(hOimports)

    return


def gmodel(appl_name, object_name):
#    objD = objData(appl_name, object_name)
    #MB: Have to have the smodel.py file in each apps /modules folder
    try:
        modulePath = str(w2p_apps) + SLASH + appl_name + SLASH + 'modules' + SLASH + 'smodel.py'
        if not Path(modulePath).exists():
            copyfile(str(genMCV_templates) + SLASH + 'smodel.py', modulePath)
    except FileExistsError:
        # directory already exists
        pass
    lobj_n = object_name
    lobj_N = lobj_n[0].upper() + lobj_n[1:]
#    lobj_N = objD.obj_Name
#    lobj_N = object_name.capitalize()
    mfile = open('.' + SLASH + 'GenMCV' + SLASH + 'templates' + SLASH + 'model.py', 'r')
    outfile = open('.' + SLASH + 'web2py' + SLASH + 'applications' + SLASH + appl_name + SLASH
                   + 'modules' + SLASH + object_name + '.py', 'w')
    cont = mfile.read()
    fields_to_use = dict(obj_name=lobj_n, obj_Name=lobj_N)
    gmodel = Template(cont).substitute(fields_to_use)
#    print(gmodel)
    outfile.write(gmodel)
    outfile.close()
    mfile.close()
    return

print('Gener can create a skeleton model (in the modules directory) and controller')
print('in the controller directory using the model name you give it')
print('Additionally after you have entered the define_table lines to describe the')
print('structure of the database table, Gener can create a set of default views')
app_name = input('please enter application name : ')
lmodel = input('enter model name : ')
options = input('create model (M), controller(C), both (MC) or set of views (V) : ').lower()
create_model = False
create_view = False
create_contr = False
if options == 'm' or options == 'mc':
    create_model = True
elif options == 'c' or options == 'mc':
    create_contr = True
elif options == 'v':
        create_view = True
if create_model:
    gmodel(app_name, lmodel)
if create_contr:
    gcontr(app_name, lmodel)
if create_view:
    gview(app_name, lmodel)
if not create_model and not create_contr and not create_view :
        print('please try again')
#gview('supplier')
#gmodel('supplier')
#gcontr('supplier')

print('end')
