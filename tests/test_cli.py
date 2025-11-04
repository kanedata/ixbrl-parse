import io
import json
import subprocess
import sys

import pytest
from click.testing import CliRunner

import ixbrlparse.__main__ as ixmain
from ixbrlparse.cli import ixbrlparse_cli

_ = ixmain

cli_options = [
    [sys.executable, "-m", "ixbrlparse"],
    ["ixbrlparse"],
]


def test_cli():
    buffer = io.StringIO()
    runner = CliRunner()
    result = runner.invoke(
        ixbrlparse_cli,
        ["--outfile", buffer, "tests/test_accounts/account_1.html"],
    )  # type: ignore
    assert result.exit_code == 0
    assert ",CurrentAssets,2909.0," in buffer.getvalue()


@pytest.mark.parametrize("cli_command", cli_options)
def test_cli_raw(tmp_path, cli_command):
    f = tmp_path / "output.csv"
    result = subprocess.run(  # noqa: S603
        [
            *cli_command,
            "--outfile",
            str(f),
            "tests/test_accounts/account_1.html",
        ],
        check=False,
        capture_output=True,
        text=True,
    )  # type: ignore
    assert result.returncode == 0
    with open(f) as file:
        assert ",CurrentAssets,2909.0," in file.read()


def test_cli_json():
    buffer = io.StringIO()
    runner = CliRunner()
    result = runner.invoke(
        ixbrlparse_cli,  # type: ignore
        [
            "--outfile",
            buffer,
            "--format",
            "json",
            "tests/test_accounts/account_1.html",
        ],  # type: ignore
    )
    assert result.exit_code == 0
    data = json.loads(buffer.getvalue())
    assert data["numeric"][2]["name"] == "CurrentAssets"
    assert data["numeric"][2]["value"] == 2909.0


@pytest.mark.parametrize("cli_command", cli_options)
def test_cli_json_raw(tmp_path, cli_command):
    f = tmp_path / "output.json"
    result = subprocess.run(  # noqa: S603
        [
            *cli_command,
            "--outfile",
            str(f),
            "--format",
            "json",
            "tests/test_accounts/account_1.html",
        ],
        check=False,
        capture_output=True,
        text=True,
    )  # type: ignore
    assert result.returncode == 0
    with open(f) as file:
        data = json.load(file)
        assert data["numeric"][2]["name"] == "CurrentAssets"
        assert data["numeric"][2]["value"] == 2909.0


def test_cli_unknown_format():
    buffer = io.StringIO()
    runner = CliRunner()
    result = runner.invoke(
        ixbrlparse_cli,  # type: ignore
        [
            "--outfile",
            buffer,
            "--format",
            "flurg",
            "tests/test_accounts/account_1.html",
        ],  # type: ignore
    )
    assert result.exit_code != 0
    data = buffer.getvalue()
    assert not data


@pytest.mark.parametrize("cli_command", cli_options)
def test_cli_unknown_format_raw(tmp_path, cli_command):
    f = tmp_path / "output.txt"
    result = subprocess.run(  # noqa: S603
        [
            *cli_command,
            "--outfile",
            str(f),
            "--format",
            "flurg",
            "tests/test_accounts/account_1.html",
        ],
        check=False,
        capture_output=True,
        text=True,
    )  # type: ignore
    assert result.returncode != 0
    assert not f.exists()


def test_cli_jsonl():
    buffer = io.StringIO()
    runner = CliRunner()
    result = runner.invoke(
        ixbrlparse_cli,  # type: ignore
        [
            "--outfile",
            buffer,
            "--format",
            "jsonl",
            "tests/test_accounts/account_1.html",
        ],  # type: ignore
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


@pytest.mark.parametrize("cli_command", cli_options)
def test_cli_jsonl_raw(tmp_path, cli_command):
    f = tmp_path / "output.jsonl"
    result = subprocess.run(  # noqa: S603
        [
            *cli_command,
            "--outfile",
            str(f),
            "--format",
            "jsonl",
            "tests/test_accounts/account_1.html",
        ],
        check=False,
        capture_output=True,
        text=True,
    )  # type: ignore
    assert result.returncode == 0
    with open(f) as file:
        lines = file.readlines()
        for line in lines:
            data = json.loads(line)
            if data["name"] == "CurrentAssets":
                assert data["value"] == 2909.0
                break
        else:
            msg = "CurrentAssets not found"
            raise AssertionError(msg)
