from typer.testing import CliRunner

from paracelsus.cli import app

from .utils import mermaid_assert

runner = CliRunner()


def test_graph(package_path):
    result = runner.invoke(
        app,
        [
            "graph",
            "example.base:Base",
            "--import-module",
            "example.models",
            "--python-dir",
            str(package_path),
        ],
    )

    assert result.exit_code == 0
    mermaid_assert(result.stdout)


def test_inject_check(package_path):
    result = runner.invoke(
        app,
        [
            "inject",
            str(package_path / "README.md"),
            "example.base:Base",
            "--import-module",
            "example.models",
            "--python-dir",
            str(package_path),
            "--check",
        ],
    )
    assert result.exit_code == 1


def test_inject(package_path):
    result = runner.invoke(
        app,
        [
            "inject",
            str(package_path / "README.md"),
            "example.base:Base",
            "--import-module",
            "example.models",
            "--python-dir",
            str(package_path),
        ],
    )
    assert result.exit_code == 0

    with open(package_path / "README.md") as fp:
        readme = fp.read()
        mermaid_assert(readme)


def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
