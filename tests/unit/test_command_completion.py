from __future__ import annotations

import pytest

from pip._internal.commands.completion import CompletionCommand


@pytest.mark.parametrize(
    "prog, expected",
    [
        ("pip", "pip"),
        ("pip3", "pip3"),
        ("pip3.12", "pip3.12"),
        ("pip.exe", "pip"),
        ("pip3.exe", "pip3"),
        ("PIP.EXE", "PIP"),
        (".exe", "pip"),
        ("", "pip"),
        ("/usr/bin/python -m pip", "pip"),
        (
            r"C:\Users\user\AppData\Local\Microsoft\WindowsApps\python.exe -m pip",
            "pip",
        ),
    ],
)
def test_fish_completion_uses_valid_command_name(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    prog: str,
    expected: str,
) -> None:
    monkeypatch.setattr("pip._internal.commands.completion.get_prog", lambda: prog)

    cmd = CompletionCommand("completion", "summary")
    options, args = cmd.parse_args(["--fish"])
    cmd.run(options, args)

    out = capsys.readouterr().out
    assert f'complete -fa "(__fish_complete_pip)" -c {expected}\n' in out


def test_fish_completion_strips_carriage_returns(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("pip._internal.commands.completion.get_prog", lambda: "pip")

    cmd = CompletionCommand("completion", "summary")
    options, args = cmd.parse_args(["--fish"])
    cmd.run(options, args)

    out = capsys.readouterr().out
    assert r"string trim -r -c \r -- $completions" in out
