from clingo.application import Application, clingo_main, Flag
from clingo.symbol import Function

import os


class Clintest(Application):
    program_name = 'clintest'
    version = '0.0.1-dev'
    option_group = 'Clintest Options'
    show_model = Flag(False)
    test_process = True
    test_success = True
    base_model = []

    def print_model(self, model, printer):
        if not self.test_process:
            print(model)
            self.base_model.append(model)
        else:
            answer = ''
            test = '\n### CLINTEST OUTPUT ###\n'
            for s in model.symbols(shown=True):
                if s.name != 'clintest':
                    answer += str(s) + ' '
                else:
                    # Clintest symbols found
                    if s.arguments:
                        if len(s.arguments) == 1:
                            if s.arguments[0].name == 'sat':
                                pass
                                # print('SAT')
                        if len(s.arguments) >= 2:
                            if s.arguments[0].name == 'trueInAll':
                                miss = 0
                                total = 0
                                symbols_missing = []
                                for a in s.arguments[1:]:
                                    total += 1
                                    if not model.contains(a):
                                        self.test_success = False
                                        miss += 1
                                        symbols_missing.append(a)

                                test += f'Result for test {s}\n'
                                test += f'Total\t\t: {total}\n'
                                test += f'Total missing\t: {miss}\n'
                                if symbols_missing:
                                    strms = ''
                                    for ms in symbols_missing:
                                        strms += f'{str(ms)} '

                                    test += f'Missing symbols : {strms}\n\n'

                            if s.arguments[0].name == 'trueInOne':
                                miss = 0
                                total = 0
                                symbols_missing = []
                                success = True
                                for a in s.arguments[1:]:
                                    total += 1
                                    if not model.contains(a):
                                        miss += 1
                                        symbols_missing.append(a)
                                        success = False
                                if success :
                                    self.test_success = True

                                test += f'Result for test {s}\n'
                                test += f'Total\t\t: {total}\n'
                                test += f'Total missing\t: {miss}\n'
                                if symbols_missing:
                                    strms = ''
                                    for ms in symbols_missing:
                                        strms += f'{str(ms)} '

                                    test += f'Missing symbols : {strms}\n\n'    

                            

            
            if self.test_success:
                test += 'CLINTEST RESULT : FAIL'
            else:
                test += 'CLENTEST RESULT : PASS'
            print(answer)
            print(test)

    def main(self, ctl, files):
        # for path in files:
        #     ctl.load(path)
        # if not files:
        #     ctl.load('-')
        ctl.load('example/simpleTest.lp')
        ctl.ground([('base', [])], context=self)
        ctl.ground([('clintest', [])], context=self)
        ctl.solve()

    def register_options(self, options):
        options.add_flag(
            self.option_group,
            'show-model',
            'Show models in the output',
            self.show_model,
        )


def main():
    clingo_main(Clintest())


print(os.getcwd())

main()
