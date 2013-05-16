import sublime, sublime_plugin

class ListLessVariables(sublime_plugin.TextCommand):
    def run(self, edit):
        fn = self.view.file_name().encode("utf_8")
        if not fn.endswith(".less"):
            return
        self.variables = []
        self.view.find_all("(@[^\s\\]*;:,\{]*): *(.*);", 0, "$1|$2", self.variables)
        self.variables = list(set(self.variables))
        self.variables.sort()
        for i, val in enumerate(self.variables):
            self.variables[i] = val.split("|")
        self.view.window().show_quick_panel(self.variables, self.insert_variable, sublime.MONOSPACE_FONT)

    def insert_variable(self, choice):
        if choice == -1:
            return
        edit = self.view.begin_edit()
        startloc = self.view.sel()[-1].end()
        self.view.insert(edit, startloc, self.variables[choice][0])
        self.view.end_edit(edit)