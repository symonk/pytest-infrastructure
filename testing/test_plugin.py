# -*- coding: utf-8 -*-
from _pytest.config import ExitCode
from _pytest.pytester import Testdir


def test_plugin_not_registered_when_skipped(testdir: Testdir) -> None:
    testdir.makepyfile(
        """
        from infrastructure import infrastructure
        from infrastructure import PytestValidate
        
        
        @infrastructure(order=1)
        def infra_checks():
            print('ok')
            
        def test_this(infrastructure_funcs):
            assert len(infrastructure_funcs) == 1
        """
    )
    result = testdir.runpytest("-s", "--tb=long")
    assert result.ret == ExitCode.OK
