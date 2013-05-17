import sublime, sublime_plugin, os, re

class ListLessVariables(sublime_plugin.TextCommand):
    def run(self, edit):
        fn = self.view.file_name().encode("utf_8")
        if not fn.endswith(".less"):
            return
            
        # Handle imports
        imports = []
        imported_vars = []
        self.view.find_all("@import \"(.*)\";", 0, "/$1.less", imports)

        file_dir = os.path.dirname(fn)

        for i, val in enumerate(imports):
            try:
                filename = val

                if filename.find(".") == -1:
                    filename += ".less"

                f = open(os.path.normpath(file_dir) + filename, 'r')
                contents = f.read()

                m = re.findall("(@[^\s\\]]*): *(.*);", contents)
                imported_vars = imported_vars + m
            except:
                print "Could not load file " + val

        # Convert a list of tuples to a list of lists
        imported_vars = [list(item) for item in imported_vars]

        self.variables = []
        self.view.find_all("(@[^\s\\]]*): *(.*);", 0, "$1|$2", self.variables)
        self.variables = list(set(self.variables))
        for i, val in enumerate(self.variables):
            self.variables[i] = val.split("|")
        self.variables = imported_vars + self.variables
        self.variables.sort()
        self.view.window().show_quick_panel(self.variables, self.insert_variable, sublime.MONOSPACE_FONT)

    def insert_variable(self, choice):
        if choice == -1:
            return
        edit = self.view.begin_edit()
        startloc = self.view.sel()[-1].end()
        self.view.insert(edit, startloc, self.variables[choice][0])
        self.view.end_edit(edit)