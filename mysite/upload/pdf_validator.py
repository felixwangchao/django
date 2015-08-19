# -*- coding: utf-8 -*-

from gear import Gear
import os, re, subprocess, logging

class PdfValidator(Gear):
    """
    Check on this issue pdf files to validate if it conforms to parameterized tests
    """

    exploder_dump_pdfinfo = re.compile(r'^([\w \d]*)\:\s+(.*)$')
    exploder_page_size = re.compile(r'^(\d+\.?\d*) x (\d+\.?\d*) .*$')
    fatal_parameter = '_fail'

    def __init__(self, issue_context):
        if 'parameters' not in issue_context:
            raise RuntimeError('Attempt to run DownloadedIssueValidator without parameters.')
        if 'pdf_validation_tests' not in issue_context['parameters']:
            raise RuntimeError('Attempt to run DownloadedIssueValidator without pdf_validation_tests declared in parameters.')
        if 'working_directory' not in issue_context:
            raise RuntimeError('Attempt to run DownloadedIssueValidator without a working_directory context.')
        if not os.path.isdir(issue_context['working_directory']):
            raise RuntimeError('Attempt to run DownloadedIssueValidator without an existing working_directory.')
        self.context = issue_context
        self.log = logging
        self.dump = ''
        self.data = False
        self.filename = ''

    def get_pdfinfo_data(self, filename):
        try:
            print 'pdfinfo -meta ',filename
            self.dump = subprocess.check_output('pdfinfo -meta "{0}"'.format(filename), shell=True)
            print "find no error"
            return True
        except subprocess.CalledProcessError:
            print "find error"
            self.context['pdf_validator_dump'] = self.dump
            return False

    def get_explode_dump(self):
        self.data = {}
        for line in self.dump.split('\n'):
            groups = self.exploder_dump_pdfinfo.match(line)
            if groups is not None:
                self.data[groups.group(1)] = groups.group(2)

    def check_portrait(self, void=True):
        if 'Page size' not in self.data:
            message = 'Attempt for {} to check_mode_portrait in PdfValidator without Page size informations.'.format(self.filename)
            self.fail_on_message(message)
            return False
        groups = self.exploder_page_size.match(self.data['Page size'])
        return float(groups.group(1)) < float(groups.group(2))

    def _check_pages_multiple_of(self, multiple):
        if 'Pages' not in self.data:
            message = 'Attempt for {} to check_pages_even in PdfValidator without Pages informations.'.format(self.filename)
            self.fail_on_message(message)
            return False
        return int(self.data['Pages']) % multiple == 0

    def check_pages_even(self, should_be=True):
        return self._check_pages_multiple_of(2) == should_be

    def check_4p_multiple(self, should_be=True):
        return self._check_pages_multiple_of(4) == should_be

    def check_8p_multiple(self, should_be=True):
        return self._check_pages_multiple_of(8) == should_be

    def check_minimum_pages(self, should_be=1):
        return int(self.data['Pages']) >= should_be

    def check_maximum_pages(self, should_be=1):
        return int(self.data['Pages']) <= should_be

    def checking_filename(self, filename):
        self.filename = filename
        filename = self.context['working_directory']+filename
        if not os.path.isfile(filename):
            message = 'Attempt to run PdfValidator but {} is not a existing file to validate.'.format(filename)
            self.fail_on_message(message)
            return False

        self.get_pdfinfo_data(filename)
        self.get_explode_dump()
        fail_is_fatal = True
        if self.fatal_parameter in self.context['parameters']['pdf_validation_tests']:
            fail_is_fatal = self.context['parameters']['pdf_validation_tests'][self.fatal_parameter]

        if 'Pages' not in self.data:
            message = 'Attempt for {} to PdfValidator without Pages informations.'.format(filename)
            self.fail_on_message(message, fail_is_fatal)
            return False

        for (test_name, parameter) in self.context['parameters']['pdf_validation_tests'].items():
            if (test_name != self.fatal_parameter) and (not getattr(self, 'check_'+test_name)(parameter)):
                self.context['pdf_validator_dump'] = self.dump
                message = 'PdfValidator for {} failed_on {}'.format(self.filename, test_name)
                self.fail_on_message(message, fail_is_fatal)
                return False
        return True

    def checking(self):
        for test_file in self.context['files_to_validate']:
            if not self.checking_filename(test_file):
                return False
        return True            

    def run(self):
        self.checking()
        if not 'validated' in self.context:
            self.context['validated'] = True
        return self.context
