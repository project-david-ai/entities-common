"""Public execution-ledger contract registration test."""

from projectdavid_common.validation import ValidationInterface


def test_execution_ledger_public_contracts():
    """Seven public schemas must be available through ValidationInterface."""

    expected = (
        "ExecutionActorRead",
        "ExecutionEpochRead",
        "ExecutionPage",
        "DelegationRead",
        "DelegationPage",
        "ExecutionEventRead",
        "ExecutionEventPage",
    )

    for name in expected:
        schema = getattr(ValidationInterface, name, None)
        assert schema is not None, f"Missing schema: {name}"
        assert callable(schema), f"Invalid schema: {name}"

    # Verify the public response envelopes can be instantiated.
    execution = ValidationInterface.ExecutionPage(
        root_run_id="run_test",
        data=[],
        has_more=False,
        next_cursor=None,
    )

    delegations = ValidationInterface.DelegationPage(
        root_run_id="run_test",
        data=[],
        has_more=False,
        next_cursor=None,
    )

    events = ValidationInterface.ExecutionEventPage(
        root_run_id="run_test",
        data=[],
        has_more=False,
        next_cursor=None,
    )

    assert execution.object == "list"
    assert delegations.object == "list"
    assert events.object == "list"

    assert execution.root_run_id == "run_test"
    assert delegations.root_run_id == "run_test"
    assert events.root_run_id == "run_test"
