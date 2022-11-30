from __future__ import absolute_import, unicode_literals, print_function, division

import sublime_plugin
import sublime
from collections import defaultdict
import tempfile
import binascii
import re
import os.path
import json

try:
    from .sublimerepl import manager, SETTINGS_FILE
except (ImportError, ValueError):
    from sublimerepl import manager, SETTINGS_FILE



escape_dict={'\\':r'\\',
           '\a':r'\a',
           '\b':r'\b',
           '\c':r'\c',
           '\f':r'\f',
           '\n':r'\n',
           '\r':r'\r',
           '\t':r'\t',
           '\v':r'\v',
           '\'':r'\'',
           '\"':r'\"',
           '\0':r'\0',
           '\1':r'\1',
           '\2':r'\2',
           '\3':r'\3',
           '\4':r'\4',
           '\5':r'\5',
           '\6':r'\6',
           '\7':r'\7',
           '\8':r'\8',
           '\9':r'\9'}        

def raw(text):
    """Returns a raw string representation of text"""
    new_string=''
    for char in text:
        try: new_string+=escape_dict[char]
        except KeyError: new_string+=char
    return new_string

class Q(sublime_plugin.TextCommand):
    def run(self, edit, scope="selection", action="send"):
        text = ""
        if scope == "selection":
            text = self.selected_text()
        elif scope == "lines":
            text = self.selected_lines()
        elif scope == "function":
            text = self.selected_functions()
        elif scope == "block":
            text = self.selected_blocks()
        elif scope == "file":
            text = self.selected_file()

        print(text)
        
        # orig_repl = ":executeK4Query(\"" + raw(text)+ "\")";
        orig_repl = text
        cmd = "repl_" + action
        self.view.window().run_command(cmd, {"external_id": self.repl_external_id(), "text": orig_repl})

    def repl_external_id(self):
        return self.view.scope_name(0).split(" ")[0].split(".")[1]

    def selected_text(self):
        v = self.view
        parts = [v.substr(region) for region in v.sel()]
        return "\\n".join(parts)

    def selected_blocks(self):
        # TODO: Clojure only for now
        v = self.view
        strs = []
        old_sel = list(v.sel())
        v.run_command("expand_selection", {"to": "brackets"})
        v.run_command("expand_selection", {"to": "brackets"})
        for s in v.sel():
            strs.append(v.substr(s))
        v.sel().clear()
        for s in old_sel:
            v.sel().add(s)
        return "\\n".join(strs)

    def selected_lines(self):
        v = self.view
        parts = []
        for sel in v.sel():
            for line in v.lines(sel):
                parts.append(v.substr(line))
        return "\n".join(parts)

    def selected_file(self):
        v = self.view
        return v.substr(sublime.Region(0, v.size()))

class QChart(sublime_plugin.TextCommand):  
    def run(self, edit, scope="selection", action="send"):
        orig_repl = ":chart"
        
        cmd = "repl_" + action
        self.view.window().run_command(cmd, {"external_id": self.repl_external_id(), "text": orig_repl})

    def repl_external_id(self):
        return self.view.scope_name(0).split(" ")[0].split(".")[1]


class QChangeServer(sublime_plugin.TextCommand):
    def run(self, edit, scope="selection", action="send"):
        v = self.view
        text = v.substr(sublime.Region(0, v.size()))
        # regex = re.compile("(/\s.+:.+:\d*:.*:.*)")
        # r = regex.findall(text)
        text = self.get_hp(text)

        text = text + self.get_sbl()
        self.text = [ v for (i,v) in enumerate(text) if v not in text[0:i] ]
        self.action = action
        print(text)
        if len(text) == 0 :
            return

        if self.text:
            sublime.active_window().show_quick_panel(self.text, self.on_chosen)

    def get_hp(self,text):
        regex = re.compile("(/\s.+:.+:\d*:.*:.*)")
        return regex.findall(text)


    def repl_external_id(self):
        return self.view.scope_name(0).split(" ")[0].split(".")[1]

    def get_sbl(self):
        project_data = sublime.active_window().project_data()
        project = project_data.get("folders")

        if not project:
            project = []
        project = project + [{'path' : os.path.dirname(sublime.active_window().project_file_name()) }]

        folders = [ p["path"]+"\\cfg\\system.sbl" for p in project ]
        folders = [f for f in folders if os.path.isfile(f) ]        
        folders = [self.get_hp(open(f).read()) for f in folders]
        folders = [item for sublist in folders for item in sublist]

        return folders

    def on_chosen(self,index):
        if index == -1 :
            return
        print(self.text)
        text = self.text
        text = text[index]

        text = ":addSetServer(\"" + text + "\");\n"
        cmd = "repl_" + self.action
        self.view.window().run_command(cmd, {"external_id": self.repl_external_id(), "text": text})
