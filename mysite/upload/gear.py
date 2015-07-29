import logging, datetime, re, os, glob
from pytz import timezone

class Gear(object):
    """
    Utility primitive class, not intented to be directly loaded as a gear
    """

    regex_split_filename_extend = re.compile(r'\/?(?P<signifiant>[^\/]+)\.(?P<extend>[^\/\.]+)$')

    def __init__(self):
        self.context = []

    def fail_on_message(self, message, fail_is_fatal=True):
        if not 'fail_on' in self.context:
            self.context['fail_on'] = []
        self.context['fail_on'].append(message)
        logging.warn(message)
        if fail_is_fatal is True:
            self.context['validated'] = False

    def remove_any_kind_files(self, kind):
        for filename in glob.glob(self.context['working_directory']+kind+'.*'):
            os.unlink(filename)

    def create_working_dir(self):
        path = self.context['working_directory']
        if self.context['validated']:
            if not os.path.isdir(path):
                try:
                    os.makedirs(path)
                except:
                    message = 'Permission denied on {}'.format(path)
                    self.fail_on_message(message)
                    return False
            else:
                self.remove_any_kind_files('raw')
        return True

    def legacy_path(self):
        return '{path}{key}/'.format(
            path = self.context['legacy_repository_path'],
            key  = self.context['publication']['key']
            )

    def legacy_normalized_name(self, extend):
        trigger = self.context['publication']['key'].upper().replace('_', '-')
        return '{trigger}_{datepub}_{issuenr}.{extend}'.format(
            trigger = trigger,
            datepub = self.context['record']['publication_date'].strftime('%Y%m%d'),
            issuenr = self.context['record']['number'],
            extend  = extend
            )

    def publication_date_is_past(self):
        now = self.now()
        if type(self.context['record']['publication_date']) is datetime.date:
            now = now.date()
        return self.context['record']['publication_date'] <= now

    def now(self):
        return datetime.datetime.now(timezone('Europe/Paris'))

    def remove_insensitive_case_double_entries(self, entries):
        check = []
        out = []
        for i in entries:
            if not i.lower() in check:
                check.append(i.lower())
                out.append(i)
            else:
                logging.warning('Source listing presents {} twice by sensitive case error !'.format(i))
        return out
