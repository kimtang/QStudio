from __future__ import absolute_import, unicode_literals, print_function, division

import sublime_plugin
import sublime
from collections import defaultdict
import tempfile
import binascii
import re

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
        
        orig_repl = "executeK4Query(\"" + raw(text)+ "\")";
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
        orig_repl = "chart()"
        
        cmd = "repl_" + action
        self.view.window().run_command(cmd, {"external_id": self.repl_external_id(), "text": orig_repl})

    def repl_external_id(self):
        return self.view.scope_name(0).split(" ")[0].split(".")[1]


class QChangeServer(sublime_plugin.TextCommand):
    def run(self, edit, scope="selection", action="send"):
        v = self.view
        text = v.substr(sublime.Region(0, v.size()))
        regex = re.compile("(/\s.+:.+:\d{1,4}:.*:.*)")
        r = regex.search(text)
        if not r:
            return

        text = r.groups()
        text = text[0]

        text = "addSetServer(\"" + text + "\")"
        print (text)
        cmd = "repl_" + action
        self.view.window().run_command(cmd, {"external_id": self.repl_external_id(), "text": text})

    def repl_external_id(self):
        return self.view.scope_name(0).split(" ")[0].split(".")[1]

    def selected_text(self):
        v = self.view
        parts = [v.substr(region) for region in v.sel()]
        return "".join(parts)

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
        return "\n\n".join(strs)

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
