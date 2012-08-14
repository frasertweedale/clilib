import clilib


class CalculatorCommand(clilib.Command):
    args = [
        (['--radix'], dict(type=int)),
        (['inputs'], dict(type=int, nargs='+')),
    ]

    def __call__(self):
        if self._args.radix:
            mapper = lambda x: int(str(x), self._args.radix)
        else:
            mapper = lambda x: int(x)
        inputs = (mapper(x) for x in self._args.inputs)
        print reduce(self._reduce, inputs)


class Add(CalculatorCommand):
    """Add values."""
    def _reduce(self, a, b):
        return a + b


class Sub(CalculatorCommand):
    """Subtract values."""
    def _reduce(self, a, b):
        return a - b


dispatcher = clilib.Dispatcher()
dispatcher.add_command(Add)
dispatcher.add_command(Sub)
dispatcher.dispatch()
