import io
import json

from click.testing import CliRunner

import ixbrlparse.__main__ as ixmain
from ixbrlparse.cli import ixbrlparse_cli

_ = ixmain


def test_cli():
    buffer = io.StringIO()
    runner = CliRunner()
    result = runner.invoke(ixbrlparse_cli, ["--outfile", buffer, "tests/test_accounts/account_1.html"])  # type: ignore
    assert result.exit_code == 0
    assert ",CurrentAssets,2909.0," in buffer.getvalue()


def test_cli_json():
    buffer = io.StringIO()
    runner = CliRunner()
    result = runner.invoke(
        ixbrlparse_cli,  # type: ignore
        ["--outfile", buffer, "--format", "json", "tests/test_accounts/account_1.html"],  # type: ignore
    )
    assert result.exit_code == 0
    data = json.loads(buffer.getvalue())
    assert data["numeric"][2]["name"] == "CurrentAssets"
    assert data["numeric"][2]["value"] == 2909.0


def test_cli_unknown_format():
    buffer = io.StringIO()
    runner = CliRunner()
    result = runner.invoke(
        ixbrlparse_cli,  # type: ignore
        ["--outfile", buffer, "--format", "flurg", "tests/test_accounts/account_1.html"],  # type: ignore
    )
    assert result.exit_code != 0
    data = buffer.getvalue()
    assert not data


def test_cli_jsonl():
    buffer = io.StringIO()
    runner = CliRunner()
    result = runner.invoke(
        ixbrlparse_cli,  # type: ignore
        ["--outfile", buffer, "--format", "jsonl", "tests/test_accounts/account_1.html"],  # type: ignore
    )
    assert result.exit_code == 0
    lines = buffer.getvalue().splitlines()
    for line in lines:
        data = json.loads(line)
        if data["name"] == "CurrentAssets":
            assert data["value"] == 2909.0
            break
    else:
        msg = "CurrentAssets not found"
        raise AssertionError(msg)
