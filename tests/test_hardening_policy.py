import os
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_installer(tmp_path: Path, *args: str) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")
    env["AGENTS_HOME"] = str(tmp_path / "agents-home")
    env["CODEX_HOME"] = str(tmp_path / "codex-home")
    env["CLAUDE_HOME"] = str(tmp_path / "claude-home")
    env["GEMINI_HOME"] = str(tmp_path / "gemini-home")
    env["GROK_HOME"] = str(tmp_path / "grok-home")
    env["HERMES_HOME"] = str(tmp_path / "hermes-home")
    return subprocess.run(
        ["bash", str(ROOT / "install.sh"), *args, "--source", "local"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_skill_declares_hardened_name_and_auto_trigger_scope():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "name: seo-audit" in skill
    assert "SEO-led copywriting" in skill
    assert "resources/references/source-policy.md" in skill
    assert "Google Search states that it does not use" in skill


def test_installed_guidance_does_not_prescribe_page_word_counts():
    checked = [ROOT / "SKILL.md"]
    checked.extend((ROOT / "resources").rglob("*.md"))
    checked.extend((ROOT / "scripts").glob("*.py"))
    combined = "\n".join(path.read_text(encoding="utf-8") for path in checked)

    forbidden = (
        "Minimum Word Counts",
        "Content minimums",
        "Optimal passage length",
        "aim for 3-5 relevant links per 1000 words",
        "1-2% density",
    )
    for phrase in forbidden:
        assert phrase not in combined


def test_installers_do_not_expand_online_scope_or_force_overwrites():
    shell = (ROOT / "install.sh").read_text(encoding="utf-8")
    powershell = (ROOT / "install.ps1").read_text(encoding="utf-8")

    assert 'SKILL_NAME="seo-audit"' in shell
    assert 'TARGET="codex"' in shell
    assert "ONLINE_MODE=1; FORCE=1" not in shell
    assert 'TARGET="all"' not in shell

    assert "$SKILL_NAME      = 'seo-audit'" in powershell
    assert "$TARGET          = 'codex'" in powershell
    assert "$ONLINE_MODE = $true; $FORCE = $true" not in powershell
    assert "$TARGET = 'all'" not in powershell
    assert "search visibility, keywords, local SEO" in shell
    assert "search visibility, keywords, local SEO" in powershell


def test_local_codex_install_is_isolated_and_non_destructive(tmp_path):
    first = run_installer(tmp_path, "--target", "codex")
    assert first.returncode == 0, first.stderr

    installed = tmp_path / "codex-home" / "skills" / "seo-audit"
    assert (installed / "SKILL.md").is_file()
    assert (installed / "agents" / "openai.yaml").is_file()
    assert (installed / "LICENSE").is_file()
    assert (installed / "NOTICE.md").is_file()

    second = run_installer(tmp_path, "--target", "codex")
    assert second.returncode != 0
    assert "Use --force to overwrite" in second.stderr


def test_shared_install_links_all_local_agent_skill_directories(tmp_path):
    result = run_installer(tmp_path, "--target", "shared")
    assert result.returncode == 0, result.stderr

    canonical = tmp_path / "agents-home" / "skills" / "seo-audit"
    assert (canonical / "SKILL.md").is_file()

    for home_name in ("codex-home", "claude-home", "gemini-home", "grok-home", "hermes-home"):
        link = tmp_path / home_name / "skills" / "seo-audit"
        assert link.is_symlink()
        assert link.resolve() == canonical.resolve()


def test_shared_install_preflights_conflicts_before_any_mutation(tmp_path):
    conflict = tmp_path / "claude-home" / "skills" / "seo-audit"
    conflict.mkdir(parents=True)
    marker = conflict / "owned-by-user.txt"
    marker.write_text("preserve", encoding="utf-8")

    result = run_installer(tmp_path, "--target", "shared")

    assert result.returncode != 0
    assert "No files were changed" in result.stderr
    assert marker.read_text(encoding="utf-8") == "preserve"
    assert not (tmp_path / "agents-home" / "skills" / "seo-audit").exists()
    assert not (tmp_path / "codex-home" / "skills" / "seo-audit").exists()


def test_shell_installer_rejects_skill_name_path_traversal(tmp_path):
    result = run_installer(
        tmp_path,
        "--target", "codex",
        "--skill-name", "../../escaped",
    )

    assert result.returncode != 0
    assert "one safe path component" in result.stderr
    assert not (tmp_path / "escaped").exists()


def test_powershell_installer_rejects_skill_name_path_traversal_when_available(tmp_path):
    pwsh = shutil.which("pwsh")
    if not pwsh:
        return

    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")
    env["CODEX_HOME"] = str(tmp_path / "codex-home")
    result = subprocess.run(
        [pwsh, "-NoProfile", "-File", str(ROOT / "install.ps1"),
         "--target", "codex", "--skill-name", "../../escaped", "--source", "local"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "one safe path component" in (result.stdout + result.stderr)
    assert not (tmp_path / "escaped").exists()
