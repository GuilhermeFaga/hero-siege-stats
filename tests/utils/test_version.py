import subprocess

from src.utils import version


def test_current_version_prefers_environment_variable(monkeypatch):
    monkeypatch.setenv("HERO_SIEGE_STATS_VERSION", "v9.9.9")
    monkeypatch.setattr(version, "_read_version_file", lambda: "v1.0.0")
    monkeypatch.setattr(version, "_read_git_tag", lambda: "v2.0.0")

    assert version.current_version() == "v9.9.9"


def test_current_version_reads_generated_version_file(monkeypatch, tmp_path):
    version_file = tmp_path / "version.txt"
    version_file.write_text("v1.2.3", encoding="utf-8")
    monkeypatch.delenv("HERO_SIEGE_STATS_VERSION", raising=False)
    monkeypatch.setattr(version, "VERSION_FILE_PATHS", [version_file])
    monkeypatch.setattr(version, "_read_git_tag", lambda: "v2.0.0")

    assert version.current_version() == "v1.2.3"


def test_current_version_falls_back_to_git_tag(monkeypatch):
    monkeypatch.delenv("HERO_SIEGE_STATS_VERSION", raising=False)
    monkeypatch.setattr(version, "_read_version_file", lambda: None)
    monkeypatch.setattr(version, "_read_git_tag", lambda: "v2.0.0")

    assert version.current_version() == "v2.0.0"


def test_current_version_falls_back_to_dev(monkeypatch):
    monkeypatch.delenv("HERO_SIEGE_STATS_VERSION", raising=False)
    monkeypatch.setattr(version, "_read_version_file", lambda: None)
    monkeypatch.setattr(version, "_read_git_tag", lambda: None)

    assert version.current_version() == "dev"


def test_read_git_tag_returns_tag(monkeypatch):
    def run(*args, **kwargs):
        return subprocess.CompletedProcess(args=args, returncode=0, stdout="v1.0.0\n")

    monkeypatch.setattr(subprocess, "run", run)

    assert version._read_git_tag() == "v1.0.0"


def test_is_release_version_returns_false_for_dev_versions():
    assert version.is_release_version("dev") is False
    assert version.is_release_version(None) is False


def test_is_release_version_returns_true_for_tag_versions():
    assert version.is_release_version("2026.4.4") is True
