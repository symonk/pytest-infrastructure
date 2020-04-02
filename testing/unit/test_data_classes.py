from src.infrastructure.decorators import InfrastructureMeta


def test_default_not_on_env():
    assert isinstance(InfrastructureMeta().not_on_env, list)
