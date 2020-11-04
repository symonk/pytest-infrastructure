def test_fetch_isolated_is_accurate(manager, dummy_callable) -> None:
    manager.register(dummy_callable())
    assert manager.get_squashed(), manager.get_threaded() == (1, 1)


def test_non_minus_one_isolated_is_considered_threaded(manager, dummy_callable) -> None:
    manager.register(dummy_callable(order=0))
    assert manager.get_squashed(), manager.get_isolated() == (1, 1)


def test_active_is_correct(manager, dummy_callable) -> None:
    staging = "staging"
    manager.register(dummy_callable(ignored_on={staging}))
    manager.register(dummy_callable())
    assert len(manager.get_active(staging)) == 1


def test_active_none_is_correct(manager) -> None:
    assert not manager.get_active()
    assert not manager.get_squashed()
    assert not manager.get_isolated()
    assert not manager.get_threaded()
