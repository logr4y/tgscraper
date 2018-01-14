import json
import os
import config

class DB:
    logfile = ''

    def __init__(self, lgroup):
        """ Class constructor """
        self.logfile = '{}{}.json'.format(config.output_folder, lgroup.lower())
        if not os.path.exists(config.output_folder):
            os.makedirs(config.output_folder)

    def load_data(self):
        """ Returns current conversation """
        try:
            with open(self.logfile) as fp:
                return json.load(fp)
        except IOError:
            fp = open(self.logfile, 'w')
            fp.close()
            return {}

    def write_data(self, ldb):
        """ Saves conversation to file """
        print('Writing to {}...'.format(self.logfile))
        with open(self.logfile, 'w') as fp:
            json.dump(ldb, fp)
