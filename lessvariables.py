import sublime, sublime_plugin, os, re

class ListLessVariables(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings('lessvariables.sublime-settings')

        handle_imports = settings.get("readImported")
        read_all_views = settings.get("readAllViews")

        regex = "(@[^\s\\]]*): *(.*);"
        self.edit = edit
        fn = self.view.file_name().encode("utf_8")
        if not fn.endswith(b'.less'):
            return
            
        # Handle imports
        imports = []
        imported_vars = []

        if handle_imports:
            self.view.find_all("@import-once [\'\"](.*)[\'\"]", 0, "/$1", imports)
            self.view.find_all("@import [\'\"](.*)[\'\"]", 0, "/$1", imports)

            file_dir = os.path.dirname(fn)

            for i, val in enumerate(imports):
                try:
                    filename = val

                    if re.search(".less(import)?", filename) == None:
                        filename += ".less"

                    f = open(os.path.normpath(file_dir.decode("utf-8") + filename), 'r')
                    contents = f.read()
                    f.close()

                    m = re.findall(regex, contents)
                    imported_vars = imported_vars + m
                except:
                    print('Could not load file ' + val)

            # Convert a list of tuples to a list of lists
            imported_vars = [list(item) for item in imported_vars]

        self.variables = []

        vars_from_views = []

        if read_all_views:
            for view in self.view.window().views():
                viewfn = view.file_name().encode("utf_8")
                if viewfn.endswith(b'.less') or viewfn.endswith(b'.lessimport'):
                    viewvars = []
                    view.find_all(regex, 0, "$1|$2", viewvars)
                    vars_from_views += viewvars
        else:
            self.view.find_all(regex, 0, "$1|$2", self.variables)
            
        self.variables += vars_from_views
        self.variables = list(set(self.variables))
        for i, val in enumerate(self.variables):
            self.variables[i] = val.split("|")
        self.variables = imported_vars + self.variables
        self.variables.sort()
        self.view.window().show_quick_panel(self.variables, self.insert_variable, sublime.MONOSPACE_FONT)

    def insert_variable(self, choice):
        if choice == -1:
            return
        self.view.run_command('insert_text', {'string': self.variables[choice][0]})

class InsertText(sublime_plugin.TextCommand):
    def run(self, edit, string=''):
        self.view.insert(edit, self.view.sel()[-1].end(), string)
