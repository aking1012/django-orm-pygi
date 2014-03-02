'''
Only compatible with py3k.
I have neither the desire nor the inclination to support 2.6+.
'''

from gi.repository import Gtk
global settings
from django.conf import settings
from django.core.management import execute_from_command_line

class TextEntryBox(Gtk.VBox):
    def __init__(self, a_tuple):
        super().__init__()
        self.add(Gtk.Label(a_tuple[0]))
        self.entry = Gtk.Entry()
        self.entry.set_text(a_tuple[1])
        self.add(self.entry)

class ORMConfigBox(Gtk.VBox):
    def __init__(self):
        super().__init__()
        '''
        Config params
        '''
        self.name = "testdb"
        self.user = ""
        self.password = ""
        self.host = ""
        self.port = ""
        self.apps = ()
        self.cb_fields = []
        self.engine = 'sqlite'
        self.db_dict = {'sqlite' : 'django.db.backends.sqlite3',
                        'postgres' : 'django.db.backends.postgresql_psycopg2'}
        '''
        Actual GUI components
        '''
        #Database engine selector
        engine_box = Gtk.VBox()
        engine_label = Gtk.Label('Database engine')
        engine_store = Gtk.ListStore(str)
        engines = ["sqlite", "postgres"]
        for engine in engines:
            engine_store.append([engine])
        engine_combo = Gtk.ComboBox.new_with_model(engine_store)
        engine_combo.connect("changed", self.cb_engine_change)
        renderer_text = Gtk.CellRendererText()
        engine_combo.pack_start(renderer_text, True)
        engine_combo.add_attribute(renderer_text, "text", 0)
        engine_box.add(engine_label)
        engine_box.add(engine_combo)
        self.add(engine_box)
        self.cb_fields = []
        self.user
        self.password
        self.host
        self.port
        for item in [('Database Name', self.name),
                    ('User', self.user),
                    ('Password', self.password),
                    ('Host', self.host),
                    ('Port', self.port)]:
            entry = TextEntryBox(item)
            self.cb_fields.append(entry.entry.get_text)
            self.add(entry)
        button = Gtk.Button('Apply')
        button.connect('clicked', self.cb_apply)
        self.add(button)

    def set_apps(self, apps):
        self.apps = apps

    def cb_engine_change(self, w):
        tree_iter = w.get_active_iter()
        if tree_iter != None:
            model = w.get_model()
            engine = model[tree_iter][0]
            self.engine = engine

    def cb_apply(self, w):
        self.name = self.cb_fields[0]()
        self.user = self.cb_fields[1]()
        self.password = self.cb_fields[2]()
        self.host = self.cb_fields[3]()
        self.port = self.cb_fields[4]()

        self.init_db_settings()
        self.sync_db_schema()

    def init_db_settings(self):
        DATABASES = {}
        DATABASES['default'] = {}
        DATABASES['default']['ENGINE'] = self.db_dict[self.engine]
        DATABASES['default']['NAME'] = self.name
        DATABASES['default']['PASSWORD'] = self.password
        DATABASES['default']['HOST'] = self.host
        DATABASES['default']['PORT'] = self.port
        settings.configure(DEBUG=False, DATABASES=DATABASES, INSTALLED_APPS=self.apps) 

    def sync_db_schema(self):
        execute_from_command_line(['manage.py', 'syncdb'])

if __name__ == '__main__':
    win = Gtk.Window()
    orm_conf = ORMConfigBox()
    orm_conf.set_apps(('stockmodels', 'moremodels'))
    win.add(orm_conf)
    win.show_all()
    win.connect("delete-event", Gtk.main_quit)
    Gtk.main()