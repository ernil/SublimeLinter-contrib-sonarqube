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

from SublimeLinter.lint import Linter, util


class Sonarqube(Linter):
    """Provides an interface to sonarqube."""

    syntax = ('javascript', 'php', 'javascriptnext')
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

    def split_match(self, match):
        """Return the match with ` quotes transformed to '."""

        if match:

            error = match.group('error')
            warning = match.group('warning')

            if error or warning:

                import webbrowser
                new = 2
                url = "file:////home/morion/projects/Easylitics-2012/.sonar/issues-report/issues-report.html"
                #webbrowser.open(url,new=new)

            return match, 0, 0, error, warning, '', None

        return match, None, None, None, None, '', None

