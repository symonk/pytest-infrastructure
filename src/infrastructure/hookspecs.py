from pluggy import HookspecMarker, HookimplMarker

hookspec = HookspecMarker("pytest-infra")
hookimpl = HookimplMarker("pytest-infra")


class InfrastructureHooks:
    @hookspec
    def collect_functions(self):
        """ collect validation functions """

    @hookspec
    def validate(self):
        """ validate the functions """
