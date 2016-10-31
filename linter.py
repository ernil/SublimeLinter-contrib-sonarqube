#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by 
# Copyright (c) 2016 
#
# License: MIT
#

"""This module exports the Sonarqube plugin class."""

import json
import sublime
import pprint
from SublimeLinter.lint import Linter, util


class Sonarqube(Linter):
    """Provides an interface to sonarqube."""

    syntax = ('javascript', 'php', 'java')
    executable = 'sonar-runner'
    version_args = '--version'
    version_re = r'Scanner (?P<version>[0-9]\.[0-9])'
    version_requirement = '>= 1.0'
    regex = (
        r'^.+?(?:(?P<error>major)|(?P<warning>minor))'
    )
    multiline = False

    def cmd(self):
        """Return the command line to execute."""
        command = [self.executable_path, '-Dsonar.sources=' + self.filename]

        return command + ['*']

    def find_errors(self, output):

        settings = sublime.load_settings('SublimeLinter.sublime-settings').get('user')

        json_data=open(settings["sonar_report_path"]).read()

        if json_data:
            data = json.loads(json_data)
            issues = data["issues"]

            for issue in issues:
                yield self.get_issue(issue)

        return None, None, None, None, None, '', None


    def get_issue(self, issue):

        match = {}
        severity = issue.get("severity", "MAJOR");
        match["message"] =  severity + ": " + issue.get("message", '')
        match["line"] = issue.get("line", 1) - 1
        match["col"] = 0

        error = None
        warning = None
        if severity == "MAJOR":
            match["type"] = 'error'
            error = True
        elif severity == "MINOR":
            match["type"] = 'warning'
            warning = True

        return match, match["line"], 0, error, warning, match["message"], None


