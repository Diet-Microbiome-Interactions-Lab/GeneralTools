"""
caragols.clix

I am the Command Line Invocation eXtension (clix)

The basic idea is to rely on JSON or YAML documents for default and/or complex configuration.
The command arguments are interpreted as a sequence of edit commands to the configuration object.
The edit commmands are the same syntax and semantics as defined in the app.condo.Condex.sed method.

For instance, the following command line ...

RGB thumbnail ^defaults ^myconf landingzone: $HOME/APPF/LZ
              thumbnails.Q: $HOME/APPF/Q thumbnails.ARK: $HOME/APPF/ARK
              thumbnails.catalog+ hello.png thumbnails.processed! thumnails.cleaned~

... runs the RGB program with thumbnail as the command, with the default conf updated
    by loading in myconf.yml and then applying the changes described in the rest of
    the line.
"""
import sys
import os.path
import glob
import logging

from GeneralTools.caragols import carp
from GeneralTools.caragols import condo

DEFAULT_LOG_LEVEL = logging.WARN


class App:
    """
    """

    DEFAULTS = {
        "log.level":    logging.WARN,
        "report.form": 'prose'
    }

    def __init__(self, name=None, run_mode="cli", comargs=['help'], defaults=None, _mode='debug', filetype=None, **kwargs):
        self.filetype, self._mode = filetype, _mode
        if self._mode == 'debug':
            print(f'# ~~~~~~~~~~ INIT Start: CLIX ~~~~~~~~~~ #')
            print('DEBUG: (i) Starting init for clix')
        self.run_mode = run_mode
        self.comargs = comargs
        self.actions = []
        self.dispatches = []
        self._name = name
        # if self._mode == 'debug':
        #     print('\n(i) Configuration Setup')
        self.conf = condo.Condex()  # Default configuration
        if defaults:
            self.DEFAULTS = defaults

        if self.DEFAULTS:
            self.conf.update(self.DEFAULTS)

        # -------------------------------------------------------------------------
        # -- Set up basic logging before we allow for more advanced configuration |
        # -- Any subclass specific logging can be overridden in .configure_logger |
        # -------------------------------------------------------------------------
        self.initialize_logger()

        # ---------------------------------------------------------------------------
        # -- load any configurations that are in expected places in the file system |
        # ---------------------------------------------------------------------------
        self.configure()
        # self._mode = self.conf.get('mode', 'normal')
        self.configure_logger()

        # -----------------------------------------------------------------------
        # -- the default dispatcher is loaded by reading self for .do_* methods |
        # -----------------------------------------------------------------------
        if self._mode == 'debug':
            print(f'\n\nDEBUG: (ii) Attr Parsing')
        for attr in dir(self):
            if attr.startswith("do_"):
                if self._mode == 'debug':
                    print(f'DEBUG: Parsing attr: {attr}')
                action = getattr(self, attr)
                if callable(action):
                    if self._mode == 'debug':
                        print(f'DEBUG: attr --> {attr} is callable!')
                    tokens = attr[3:].split('_')

                    self.dispatches.append((tokens, action))

        tokens = [' '.join(v[0]) for v in self.dispatches]
        if self._mode == 'debug':
            print(f'DEBUG: Dispatches found:\n{tokens}')

        # -----------------------------------------------------------------------
        # -- Perform the app.run() to setup the app                             |
        # -----------------------------------------------------------------------
        # TODO: Logic for running here or somewhere else
        # if something:
        #     self.run(run_mode=run_mode)
        # else:
        #     something else
        # TODO:
        self.prepare_for_run(run_mode)
        if self._mode == 'debug':
            print(f'# ~~~~~~~~~~ INIT End: CLIX ~~~~~~~~~~ #\n')


    # -----------------------------------
    # -- BEGIN embedded logging methods |
    # -----------------------------------
    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
    # ---------------------------------
    # -- END embedded logging methods |
    # ---------------------------------

    @property
    def name(self):
        if self._name is None:
            here = os.path.abspath(sys.argv[0])
            folder, scriptfile = os.path.split(here)
            appname, suffix = os.path.splitext(scriptfile)
            self._name = appname
        return self._name

    # --------------------------------
    # -- BEGIN configuration methods |
    # --------------------------------

    @property
    def configuration_folders(self):
        return self._get_configuration_folders()

    def _get_configuration_folders(self):
        """
        I answer a sequence of configuration folders where configuration data can be found.
        The folders are processed by .configure( ) in the same order as returned, here.
        Any subclasses that want a different sequence should override this method.
        """
        # -- This is the default sequence of configuration folders...
        return ['/etc/{}'.format(self.name),
                os.path.expanduser('~/.config/{}'.format(self.name))]

    def configure(self):
        # -- look in these folders ...
        for folder in self.configuration_folders:
            if self._mode == 'debug':
                print(f'DEBUG: Searching configuration files in folder {folder}...')
            # -- Look for any file that matches the pattern 'conf_*.yml'
            # -- Load any found conf files in canonical sorting order by file name.
            for confile in glob.glob(os.path.join(folder, "conf*.yml")):
                if self._mode == 'debug':
                    print(f'Looking at configuration file {confile}')
                self.debug("looking for configuration in {}".format(confile))
                # Instantiating a new Condex
                nuconf = condo.Condex()
                # Loading the new conf with the confile
                nuconf.load(confile)
                # Updating our configuration file based on it
                self.conf.update(nuconf)

    def initialize_logger(self):
        logging.basicConfig()
        self.logger = logging.getLogger()
        self.logger.setLevel(self.conf.get('log.level', DEFAULT_LOG_LEVEL))

    def configure_logger(self):
        self.logger = logging.getLogger(self.conf.get('log.key', self.name))
        # self.logger.setLevel( self.conf.get('log.level', DEFAULT_LOG_LEVEL) )

        if 'log.level' in self.conf:
            grade = self.conf['log.level']
            if isinstance(grade, str):
                if grade.isdigit():
                    # -- looks like the log.level was given as a number, e.g. 10 (for DEBUG)
                    grade = int(grade)
                else:
                    # -- looks like the log.level was given as a symbol, e.g. DEBUG or ERROR
                    # -- look for the given symbol in the logging module and use NOTSET (level 0) if I can't find it.
                    grade = vars(logging).get(grade, logging.NOTSET)
            self.logger.setLevel(grade)

    # ------------------------------
    # -- END configuration methods |
    # ------------------------------
    @property
    def idioms(self):
        """
        I am the list of actions available in the form of [(gravity, tokens, action), ...]
        """
        idioms = []
        for tokens, action in self.dispatches:
            gravity = len(tokens)
            idioms.append((gravity, tokens, action))
        idioms = list(sorted(idioms, reverse=True))
        if self._mode == 'debug':
            print(f'Created {len(idioms)} idioms')
        return idioms

    def cognize(self, comargs):
        """
        Given comargs, a "command" as a list of string tokens, I try to find a dispatch callable to act on the command.
        If I find a suitable method, I answer (action, barewords) where action is a reference to the callable (function, method, etc.)
        that matches the command barewords is the list of remaining tokens that are not part of the command.
        Othwerise, I answer None.
        """
        if self._mode == 'debug':
            print(f'DEBUG: Cognizing {comargs}')
        xtraopts = {'xtraopt': 'Pass for now'}

        matched = False
        for gravity, tokens, action in self.idioms:
            if comargs[:gravity] == tokens:
                if self._mode == 'debug':
                    print(f'DEBUG: Matched {comargs[:gravity]}. Breaking')
                matched = True
                break

        if matched:
            confargs = comargs[gravity:]
            if self._mode == 'debug':
                print(f'DEBUG: Confargs: {confargs}')
            barewords = self.conf.sed(confargs)
            if self._mode == 'debug':
                print(f'DEBUG: Barewords: {barewords}')
                print(f'DEBUG: Updated conf...')
                print(f'DEBUG: {self.conf.show()}')
            return (tokens, action, barewords, xtraopts)

        else:
            return None

    # ----------------------------
    # -- BEGIN app state methods |
    # ----------------------------
    def begun(self):
        """
        I am called after construction and initialization.
        Override my behavior in a subclass as a relatively easy way to do additional initialization ...
        ... after the configuration pile has been loaded and merged.
        """
        pass
    
    def run(self):
        if self._mode == 'debug':
            print(f'\n\nDEBUG: (v) Running the actual executable')
        xtraopts = self.xtraopts
        self.action(self.barewords, **xtraopts)
        # --------------------------------------------------
        # -- If the action did not complete with a report, |
        # -- this should be considered a crash!            |
        # --------------------------------------------------
        # TODO: Alter the below code to sort based off of CLI vs. GUI modes

        if self._mode == 'debug':
            print(f'\n\nDEBUG: (vi): Running the final report')
        if getattr(self, 'report', None) is None:
            self.report = self.crashed("no report returned by action!")

        form = self.conf.get('report.form', 'prose')

        if self.run_mode == "cli":
            sys.stdout.write(self.report.formatted(form))
            sys.stdout.write('\n')
            self.done()
            if self.report.status.indicates_failure:
                sys.exit(1)
            else:
                sys.exit(0)
        elif self.run_mode == "gui":
            return {'status': 'success'}

    def prepare_for_run(self, run_mode):
        """
        I am the central dispatcher.
        I gather arguments from the command line,
        then invoke the appropriate "do_*" method.
        I make a special case for the verb "explain".
        "explain" does not execute a method, but instead dumps the invocation request as a merged context.
        """
        if self._mode == 'debug':
            print(f'\n\nDEBUG: (iii) Preparing for run')
        # TODO: Tracking the build of the application before running.
        self.begun()

        # ------------------------------------------------------------------------
        # -- scan for a matching dispatch in order of highest gravity to lowest. |
        # -- Here, "gravity" is the number of tokens in the action, e.g.         |
        # -- "make catalog" has a gravity of 2, while ...                        |
        # -- "make new catalog" would have a gravity of 3.                       |
        # ------------------------------------------------------------------------
        explaining = False
        method = None
        report = None
        if run_mode.lower() == 'cli':
            # Super important ---> where the CL interacts
            self.comargs = sys.argv[1:]
        elif run_mode.lower() == 'gui':
            # TODO: Figure out how to account for sys.argv[1:]
            #                      comargs={???} if run_mode=='gui'
            comargs = ['help']
        else:
            # Idea --> in init has comargs=sys.argv[1:] if run_mode=='cli
            sys.exit(1)

        if self.comargs and (self.comargs[0] == 'explain'):
            explaining = True
            self.comargs = self.comargs[1:]
        matched = self.cognize(self.comargs)
        self.matched = matched

        if self._mode == 'debug':
            print(f'\n\n(iv) Matching & Configuration Update. {matched=}')
        if matched:
            tokens, action, barewords, xtraopts = matched
            self.configure_logger()

            if explaining:
                self.report = self.do_explain(
                    tokens, action, barewords, **xtraopts)
            else:
                try:
                    if self._mode == 'debug':
                        pass
                        # print(
                            # f'Running executable:\n\n#-----Executable~Start-----#\n')
                    # print(f'Running action: {action} with {barewords} and {xtraopts}')
                    # print(f'Setting up {action} with {barewords} and {xtraopts}')
                    self.action, self.barewords, self.xtraopts = action, barewords, xtraopts
                    return 0
                    # return (action, barewords, xtraopts)
                    action(barewords, **xtraopts)
                    # if self._mode == 'debug':
                    #     print(f'\n#-----Executable~Complete-----#\n')
                except Exception as err:
                    self.report = self.crashed(str(err))
        else:
            self.report = self.failed(
                'Bad request due to no "matched".\ntry using "help" command?')

        # # --------------------------------------------------
        # # -- If the action did not complete with a report, |
        # # -- this should be considered a crash!            |
        # # --------------------------------------------------
        # # TODO: Alter the below code to sort based off of CLI vs. GUI modes

        # if getattr(self, 'report', None) is None:
        #     self.report = self.crashed("no report returned by action!")

        # form = self.conf.get('report.form', 'prose')

        # if run_mode == "cli":
        #     sys.stdout.write(self.report.formatted(form))
        #     sys.stdout.write('\n')
        #     self.done()
        #     if self.report.status.indicates_failure:
        #         sys.exit(1)
        #     else:
        #         sys.exit(0)
        # elif run_mode == "gui":
        #     return {'status': 'success'}

    def done(self):
        """
        I do any finalization just before exiting.
        My default behavior is to do nothing; however,
        override my behavior if any additional "clean up" is needed after the app has run (and dispatched).
        """
        pass

    # -----------------------------------------------------------------
    # -- BEGIN completion methods                                     |
    # -- All do_* methods should end by calling one of these methods. |
    # -----------------------------------------------------------------

    def succeeded(self, msg="", dex=None, **kwargs):
        repargs = kwargs.copy()
        repargs['body'] = msg
        repargs['data'] = dex
        self.report = carp.Report.Success(**repargs)
        return self.report

    def finished(self, msg="", dex=None, **kwargs):
        repargs = kwargs.copy()
        repargs['body'] = msg
        repargs['data'] = dex
        self.report = carp.Report.Inconclusive(**repargs)
        return self.report

    def failed(self, msg="", dex=None, **kwargs):
        repargs = kwargs.copy()
        repargs['body'] = msg
        repargs['data'] = dex
        self.report = carp.Report.Failure(**repargs)
        return self.report

    def crashed(self, msg="", dex=None, **kwargs):
        repargs = kwargs.copy()
        repargs['body'] = msg
        repargs['data'] = dex
        # self.report     = carp.Report.Exception(msg, **repargs)
        self.report = carp.Report.Exception(**repargs)
        self.critical(msg)  # -- emit the message to our log.
        return self.report

    # ---------------------------
    # -- END completion methods |
    # ---------------------------

    # --------------------------------------------
    # -- BEGIN app operation, aka "do_*" methods |
    # --------------------------------------------

    def do_explain(self, comwords, action, barewords, **kwargs):
        '''Explain the action and context.'''
        d = {}
        d['invoke'] = {
            'idiom': ' '.join(comwords),
            'method': str(action),
            'args': barewords,
            'doc': action.__doc__
        }
        d['context'] = self.conf.toJDN()

        doc = """
		explaining "{}"
		{}
		""".format(" ".join(comwords), action.__doc__)

        return self.succeeded(doc, d)

    def do_help(self, barewords, **kwargs):
        """Show all command patterns and their help messages"""
        doclines = []
        for cnt, actionable in enumerate(sorted(self.dispatches)):
            tokens, action = actionable
            humanable = " ".join(tokens)
            doclines.append(f'{cnt}: \033[92m $ {self.name} {humanable} type: {self.filetype} file: example.{self.filetype}\033[0m')
            # doclines.append("* {} {}\n".format(self.name, humanable))
            if action.__doc__:
                # print(f'Action.doc: {action.__doc__}')
                for line in action.__doc__.strip().split('\n'):
                    doclines.append(line)
                doclines.append('\n')
        doc = "\n".join(doclines)
        return self.succeeded(doc)

    # ------------------------------
    # -- END app operation methods |
    # ------------------------------


class TestApp(App):

    def do_something(self, args):
        print('do something')
        for arg in args:
            print(arg)

    def do_something_else(self, args):
        print('do something else')
        for arg in args:
            print(arg)

    def do_other_things(self, args):
        print('do other things')
        for arg in args:
            print(arg)

    @classmethod
    def test(cls):
        app = cls()
        app.run()
