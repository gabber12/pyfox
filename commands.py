#!/Users/shubham.ppe/workspace/offer-engine/venv/bin/python2.7
from __future__ import unicode_literals
import json
import os
from client import Foxtrot
from processors import FoxtrotTextProcessor, FoxtrotQueryProcessor
from prompt_toolkit import prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.history import FileHistory
from prompt_toolkit.token import Token
from prompt_toolkit.contrib.completers import WordCompleter
from pygments.lexers import SqlLexer
from utils import traverse_nested_dict
from view import JsonFormatter, PagedPresenter


class FoxtrotShell(object):

    def __init__(self, text_processor):
        self.configuration_directory = os.environ.get('HOME')+"/.foxtrot"
        self.text_processor = text_processor
        self.completion_array = []
        self.history = FileHistory(self.configuration_directory+"/history")

    def _setup_configuration_diretory(self):
        if not os.path.exists(self.configuration_directory):
            os.makedirs(self.configuration_directory)
        return self

    def _setup_history(self):
        return self

    def _setup_completion(self):
        self.completion_array = ['select', 'from', 'where', '==', '>=', '<=', 'exit']
        if not os.path.exists(self.configuration_directory+"/completion.json"):
            self._sync_completion()
        self._load_completion()
        return self

    def _sync_completion(self):
        with open(self.configuration_directory+'/completion.json', 'w') as data_file:
            data_file.write(json.dumps(self.completion_array))
        return self

    def _load_completion(self):
        with open(self.configuration_directory+'/completion.json') as data_file:
            self.completion_array = json.loads(data_file.read())

    def _update_completion(self, results):
        for each in results.rows():
            for k, _ in traverse_nested_dict(each):
                self.completion_array.append(k)
        self.completion_array = list(set(self.completion_array))
        self._sync_completion()

    def init(self):
        self._setup_configuration_diretory()._setup_completion()._setup_history()

    def start_prompt(self):
        self.init()
        connection_status = 'http://foxtrot.traefik.prod.phonepe.com/foxtrot/'
        style = style_from_dict({
            Token.Toolbar: '#ffffff bg:#333333',
        })

        def get_bottom_toolbar_tokens(cli):
            return [(Token.Toolbar, 'Status - %s' % connection_status)]
        sql_completer = WordCompleter(self.completion_array, ignore_case=True)

        # repl
        # TODO: Too much kwargs try unpack from dict
        while True:
            try:
                query_text = prompt("> ", lexer=SqlLexer, history=self.history,
                                    completer=sql_completer, get_title=lambda: "Foxtrot", enable_history_search=True,
                                    get_bottom_toolbar_tokens=get_bottom_toolbar_tokens, style=style)

                results = self.text_processor.process(query_text)
                PagedPresenter(JsonFormatter()).present(results)
                self._update_completion(results)
            except KeyboardInterrupt:
                print "Press Ctrl-D to exit"
            except EOFError:
                print "GoodBye"
                break


def boot():
    client = Foxtrot('http://foxtrot.traefik.prod.phonepe.com/foxtrot/')
    query_processor = FoxtrotQueryProcessor(client)
    input_processor = FoxtrotTextProcessor(query_processor)
    shell = FoxtrotShell(input_processor)

    shell.start_prompt()


if __name__ == '__main__':
    boot()