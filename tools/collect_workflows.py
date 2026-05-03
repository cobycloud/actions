from __future__ import annotations

import hashlib
import os
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
TARGET = WORKSPACE / "gh_actions"

SKIP_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "env",
    ".tox",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".uv-cache",
    "dist",
    "build",
    "site-packages",
    "__pycache__",
    ".next",
    ".nuxt",
    "coverage",
    "htmlcov",
    ".tmp",
    "tmp",
    "artifacts",
    "playwright-report",
}

SCRIPT_EXTS = (
    "py",
    "sh",
    "bash",
    "ps1",
    "psm1",
    "js",
    "mjs",
    "cjs",
    "ts",
    "tsx",
    "rb",
    "pl",
    "go",
    "rs",
)

SCRIPT_RE = re.compile(
    r"(?P<path>(?:\./|\.\./|[A-Za-z0-9_.-]+/)[A-Za-z0-9_./@+-]+"
    r"\.(?:py|sh|bash|ps1|psm1|js|mjs|cjs|ts|tsx|rb|pl|go|rs))"
)
USES_RE = re.compile(r"^\s*uses:\s*(.+?)\s*$", re.M)
RUN_RE = re.compile(r"^\s*run:\s*(.*)$", re.M)


def slug(value: str, limit: int = 170) -> str:
    value = re.sub(r"^[A-Za-z]:", "", value.replace("\\", "/"))
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_")
    return (value or "root")[:limit]


def short_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def unique_name(source: Path, display: str, suffix: str | None = None) -> str:
    source_rel = rel(source)
    base = slug(display, 140)
    ext = suffix if suffix is not None else source.suffix
    if ext and not ext.startswith("."):
        ext = f".{ext}"
    return f"{base}__{short_hash(source_rel)}{ext}"


def rel(path: Path, base: Path = WORKSPACE) -> str:
    return path.relative_to(base).as_posix()


def first_match(pattern: str, text: str, flags: int = re.M) -> str:
    match = re.search(pattern, text, flags)
    return match.group(1).strip().strip("\"'") if match else ""


def find_workflows() -> list[Path]:
    workflows: list[Path] = []
    for root, dirs, files in os.walk(WORKSPACE):
        root_path = Path(root)
        if root_path == TARGET or TARGET in root_path.parents:
            dirs[:] = []
            continue
        dirs[:] = [
            d
            for d in dirs
            if d not in SKIP_DIRS
            and not d.startswith(".pytest-tmp")
            and not d.startswith("workflow_logs")
            and d not in {".playwright-mcp", ".ruff_cache"}
        ]
        if root_path.name == "workflows" and root_path.parent.name == ".github":
            for filename in files:
                if filename.lower().endswith((".yml", ".yaml")):
                    workflows.append(root_path / filename)
    return sorted(workflows, key=lambda p: p.as_posix().lower())


def repo_root_for(workflow: Path) -> Path:
    parts = workflow.parts
    for index in range(len(parts) - 2):
        if parts[index] == ".github" and parts[index + 1] == "workflows":
            return Path(*parts[:index])
    return workflow.parent


def section_after_root_key(key: str, text: str) -> str:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(rf"^{re.escape(key)}\s*:", line):
            start = i + 1
            break
    if start is None:
        return ""
    out: list[str] = []
    for line in lines[start:]:
        if re.match(r"^[A-Za-z0-9_-]+\s*:", line):
            break
        out.append(line)
    return "\n".join(out)


def extract_jobs(text: str) -> list[dict[str, object]]:
    lines = text.splitlines()
    try:
        jobs_index = next(i for i, line in enumerate(lines) if re.match(r"^jobs\s*:", line))
    except StopIteration:
        return []

    jobs: list[dict[str, object]] = []
    current_id = None
    block: list[str] = []
    for line in lines[jobs_index + 1 :]:
        if re.match(r"^[A-Za-z0-9_-]+\s*:", line):
            break
        job_match = re.match(r"^\s{2}([A-Za-z0-9_.-]+)\s*:", line)
        if job_match and not line.lstrip().startswith("-"):
            if current_id:
                jobs.append(parse_job(current_id, "\n".join(block)))
            current_id = job_match.group(1)
            block = [line]
        elif current_id:
            block.append(line)
    if current_id:
        jobs.append(parse_job(current_id, "\n".join(block)))
    return jobs


def parse_job(job_id: str, block: str) -> dict[str, object]:
    step_names = []
    for match in re.finditer(r"^\s*-\s*name:\s*(.+?)\s*$", block, re.M):
        step_names.append(match.group(1).strip().strip("\"'"))
    run_blocks = [m.group(1).strip() for m in RUN_RE.finditer(block)]
    uses = [m.group(1).strip().strip("\"'") for m in USES_RE.finditer(block)]
    return {
        "id": job_id,
        "name": first_match(r"^\s*name:\s*(.+?)\s*$", block),
        "runs_on": first_match(r"^\s*runs-on:\s*(.+?)\s*$", block),
        "needs": first_match(r"^\s*needs:\s*(.+?)\s*$", block),
        "uses": uses,
        "runs": run_blocks,
        "steps": step_names,
    }


def classify_command(command: str) -> str:
    command = command.strip()
    if not command:
        return ""
    first = re.split(r"\s+", command)[0].lower()
    aliases = {
        "python3": "python",
        "pip3": "pip",
        "npx": "npm/npx",
        "npm": "npm/npx",
        "pnpm": "pnpm",
        "yarn": "yarn",
        "uv": "uv",
        "poetry": "poetry",
        "pytest": "pytest",
        "ruff": "ruff",
        "mypy": "mypy",
        "cargo": "cargo",
        "docker": "docker",
        "gh": "gh",
        "make": "make",
        "bash": "shell",
        "sh": "shell",
        "pwsh": "powershell",
        "powershell": "powershell",
        "node": "node",
    }
    return aliases.get(first, first)


def extract_commands(run_blocks: list[str]) -> list[str]:
    commands: list[str] = []
    for block in run_blocks:
        for line in block.splitlines() or [block]:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped in {"|", ">", ">-", "|-"}:
                continue
            commands.append(stripped)
    return commands


def resolve_script(repo_root: Path, text_path: str) -> Path | None:
    candidate = (repo_root / text_path).resolve()
    try:
        candidate.relative_to(repo_root.resolve())
    except ValueError:
        return None
    return candidate if candidate.exists() and candidate.is_file() else None


def extract_script_refs(repo_root: Path, text: str) -> list[dict[str, str]]:
    refs = []
    seen = set()
    for match in SCRIPT_RE.finditer(text):
        raw = match.group("path").strip("'\"")
        if raw.startswith(("http://", "https://")):
            continue
        resolved = resolve_script(repo_root, raw)
        key = (raw, str(resolved) if resolved else "")
        if key in seen:
            continue
        seen.add(key)
        refs.append(
            {
                "raw": raw,
                "resolved": str(resolved) if resolved else "",
                "exists": "yes" if resolved else "no",
            }
        )
    return refs


def infer_purpose(name: str, filename: str, jobs: list[dict[str, object]], commands: list[str]) -> str:
    haystack = " ".join([name, filename] + [str(j.get("id", "")) for j in jobs] + commands).lower()
    if any(k in haystack for k in ["publish", "release", "pypi", "npm publish"]):
        return "release and package publication"
    if any(k in haystack for k in ["deploy", "pages", "cloudflare", "vercel", "firebase"]):
        return "documentation or application deployment"
    if any(k in haystack for k in ["license", "metadata", "sbom", "audit", "security"]):
        return "compliance, metadata, or security validation"
    if any(k in haystack for k in ["test", "pytest", "vitest", "playwright", "coverage"]):
        return "test execution and validation"
    if any(k in haystack for k in ["lint", "ruff", "mypy", "format", "fmt", "prettier"]):
        return "static analysis, formatting, or type checks"
    if any(k in haystack for k in ["build", "docker", "cargo", "npm run build"]):
        return "build verification"
    return "automation workflow"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def workflow_report(
    workflow: Path,
    copied_to: Path,
    repo_root: Path,
    text: str,
    jobs: list[dict[str, object]],
    script_refs: list[dict[str, str]],
    commands: list[str],
    uses: list[str],
) -> str:
    name = first_match(r"^name:\s*(.+?)\s*$", text) or workflow.stem
    triggers = section_after_root_key("on", text).strip() or first_match(r"^on:\s*(.+?)\s*$", text)
    purpose = infer_purpose(name, workflow.name, jobs, commands)
    deps = sorted(set([u for u in uses] + [classify_command(c) for c in commands if classify_command(c)]))
    lines = [
        f"# {name}",
        "",
        f"- Source: `{rel(workflow)}`",
        f"- Copied workflow: `{rel(copied_to, TARGET)}`",
        f"- Source repository folder: `{rel(repo_root)}`",
        f"- Purpose: {purpose}",
        f"- Trigger surface: `{triggers.replace(chr(10), ' | ')[:500]}`" if triggers else "- Trigger surface: not detected",
        f"- Jobs: {len(jobs)}",
        f"- Dependencies/actions/commands: {', '.join(deps) if deps else 'none detected'}",
        "",
        "## Jobs",
    ]
    for job in jobs:
        lines.extend(
            [
                f"### `{job['id']}`",
                f"- Display name: {job.get('name') or 'not set'}",
                f"- Runner: `{job.get('runs_on') or 'not set'}`",
                f"- Needs: `{job.get('needs') or 'not set'}`",
                f"- Actions used: {', '.join(job.get('uses', [])) if job.get('uses') else 'none detected'}",
                f"- Step names: {', '.join(job.get('steps', [])) if job.get('steps') else 'not detected'}",
            ]
        )
    lines.extend(["", "## Run Commands"])
    lines.extend([f"- `{cmd}`" for cmd in commands] or ["- none detected"])
    lines.extend(["", "## Referenced Scripts"])
    if script_refs:
        for ref in script_refs:
            resolved = ref["resolved"]
            resolved_text = f"`{rel(Path(resolved))}`" if resolved else "not found in source repo"
            lines.append(f"- `{ref['raw']}` -> {resolved_text}")
    else:
        lines.append("- none detected")
    lines.append("")
    return "\n".join(lines)


def script_report(source: Path, copied_to: Path, consumers: list[Path]) -> str:
    text = read_text(source)
    first_lines = [line.strip() for line in text.splitlines()[:20]]
    shebang = first_lines[0] if first_lines and first_lines[0].startswith("#!") else ""
    ext = source.suffix.lower().lstrip(".")
    imports = []
    for pattern in [
        r"^\s*import\s+([A-Za-z0-9_., ]+)",
        r"^\s*from\s+([A-Za-z0-9_.]+)\s+import",
        r"^\s*require\(['\"]([^'\"]+)['\"]\)",
        r"^\s*import\s+.*?from\s+['\"]([^'\"]+)['\"]",
        r"^\s*use\s+([A-Za-z0-9_:]+)",
    ]:
        imports.extend(re.findall(pattern, text, re.M))
    commands = extract_commands([text]) if ext in {"sh", "bash", "ps1"} else []
    command_deps = sorted(set(filter(None, (classify_command(c) for c in commands))))
    purpose = "support script"
    haystack = (source.name + " " + text[:2000]).lower()
    if any(k in haystack for k in ["test", "pytest", "coverage"]):
        purpose = "test or coverage helper"
    elif any(k in haystack for k in ["build", "compile", "bundle"]):
        purpose = "build helper"
    elif any(k in haystack for k in ["publish", "release", "version"]):
        purpose = "release or publication helper"
    elif any(k in haystack for k in ["deploy", "pages"]):
        purpose = "deployment helper"
    elif any(k in haystack for k in ["license", "metadata", "audit", "sbom"]):
        purpose = "compliance or metadata helper"
    lines = [
        f"# {source.name}",
        "",
        f"- Source: `{rel(source)}`",
        f"- Copied script: `{rel(copied_to, TARGET)}`",
        f"- Purpose: {purpose}",
        f"- Runtime/type: `{ext or 'unknown'}`",
        f"- Shebang: `{shebang}`" if shebang else "- Shebang: not set",
        f"- Referenced by workflows: {', '.join(f'`{rel(c)}`' for c in consumers)}",
        f"- Import/module dependencies: {', '.join(sorted(set(imports))) if imports else 'none detected'}",
        f"- Command dependencies: {', '.join(command_deps) if command_deps else 'none detected'}",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    workflows_dir = TARGET / ".github" / "workflows"
    workflow_reports_dir = TARGET / "reports" / "workflows"
    script_reports_dir = TARGET / "reports" / "scripts"
    scripts_dir = TARGET / "scripts"
    for directory in [workflows_dir, workflow_reports_dir, script_reports_dir, scripts_dir, TARGET / "reports"]:
        directory.mkdir(parents=True, exist_ok=True)

    workflows = find_workflows()
    script_consumers: dict[Path, list[Path]] = defaultdict(list)
    workflow_rows = []
    all_jobs = []
    atom_counter: Counter[str] = Counter()
    domain_counter: Counter[str] = Counter()

    for workflow in workflows:
        repo_root = repo_root_for(workflow)
        repo_slug = slug(rel(repo_root))
        target_name = unique_name(workflow, f"{repo_slug}__{workflow.stem}", workflow.suffix)
        copied_workflow = workflows_dir / target_name
        copy_file(workflow, copied_workflow)
        text = read_text(workflow)
        jobs = extract_jobs(text)
        run_blocks = [run for job in jobs for run in job.get("runs", [])]
        commands = extract_commands(run_blocks)
        uses = [u for job in jobs for u in job.get("uses", [])]
        script_refs = extract_script_refs(repo_root, text)
        for use in uses:
            if use.startswith("./"):
                action_dir = (repo_root / use).resolve()
                for action_file in [action_dir / "action.yml", action_dir / "action.yaml"]:
                    if action_file.exists():
                        script_refs.extend(extract_script_refs(repo_root, read_text(action_file)))
        unique_refs = {}
        for ref in script_refs:
            unique_refs[(ref["raw"], ref["resolved"])] = ref
        script_refs = list(unique_refs.values())
        for ref in script_refs:
            if ref["resolved"]:
                script_consumers[Path(ref["resolved"])].append(workflow)
        purpose = infer_purpose(first_match(r"^name:\s*(.+?)\s*$", text), workflow.name, jobs, commands)
        domain_counter[purpose] += 1
        for job in jobs:
            job_id = str(job["id"])
            job_intent = infer_purpose(job.get("name", "") or job_id, job_id, [job], extract_commands(job.get("runs", [])))
            all_jobs.append((workflow, job, job_intent))
            for command in extract_commands(job.get("runs", [])):
                atom = classify_command(command) or command.split()[0]
                atom_counter[atom] += 1
        report = workflow_report(workflow, copied_workflow, repo_root, text, jobs, script_refs, commands, uses)
        report_path = workflow_reports_dir / unique_name(workflow, f"{repo_slug}__{workflow.stem}", ".md")
        report_path.write_text(report, encoding="utf-8")
        workflow_rows.append((workflow, copied_workflow, report_path, len(jobs), len(script_refs), purpose))

    copied_scripts: dict[Path, Path] = {}
    for source in sorted(script_consumers, key=lambda p: p.as_posix().lower()):
        repo_root = next((p for p in source.parents if (p / ".github").exists()), WORKSPACE)
        try:
            relative_source = source.relative_to(repo_root)
            repo_slug = slug(rel(repo_root))
        except ValueError:
            relative_source = source.relative_to(WORKSPACE)
            repo_slug = "workspace"
        copied_to = scripts_dir / repo_slug / unique_name(source, relative_source.as_posix(), source.suffix)
        copy_file(source, copied_to)
        copied_scripts[source] = copied_to
        report = script_report(source, copied_to, script_consumers[source])
        report_path = script_reports_dir / unique_name(source, f"{repo_slug}__{relative_source.as_posix()}", ".md")
        report_path.write_text(report, encoding="utf-8")

    inventory_lines = [
        "# GitHub Workflow Inventory",
        "",
        f"- Workspace scanned: `{WORKSPACE.as_posix()}`",
        f"- Workflows copied: {len(workflow_rows)}",
        f"- Referenced scripts copied: {len(copied_scripts)}",
        "",
        "| Source | Copied Workflow | Report | Jobs | Scripts | Purpose |",
        "| --- | --- | --- | ---: | ---: | --- |",
    ]
    for workflow, copied, report_path, job_count, script_count, purpose in workflow_rows:
        inventory_lines.append(
            f"| `{rel(workflow)}` | `{rel(copied, TARGET)}` | `{rel(report_path, TARGET)}` | {job_count} | {script_count} | {purpose} |"
        )
    (TARGET / "reports" / "workflow-inventory.md").write_text("\n".join(inventory_lines) + "\n", encoding="utf-8")

    unique_jobs = {}
    for workflow, job, job_intent in all_jobs:
        commands = extract_commands(job.get("runs", []))
        uses = tuple(sorted(job.get("uses", [])))
        command_atoms = tuple(sorted(set(classify_command(c) for c in commands if classify_command(c))))
        key_seed = "|".join([job_intent, ",".join(uses), ",".join(command_atoms)])
        key = hashlib.sha256(key_seed.encode()).hexdigest()[:12]
        unique_jobs.setdefault(key, {"intent": job_intent, "uses": uses, "atoms": command_atoms, "examples": []})
        unique_jobs[key]["examples"].append(f"{rel(workflow)}::{job['id']}")

    final_lines = [
        "# Final Workflow Component Analysis",
        "",
        "This report deduplicates workflow intent across the scanned workspace, then decomposes the remaining functionality to job-level components and atomic command/action surfaces.",
        "",
        "## Domain Coverage",
    ]
    for domain, count in domain_counter.most_common():
        final_lines.append(f"- {domain}: {count} workflow(s)")
    final_lines.extend(["", "## Deduplicated Job Components"])
    for key, item in sorted(unique_jobs.items(), key=lambda kv: (kv[1]["intent"], kv[0])):
        final_lines.extend(
            [
                f"### `{key}` {item['intent']}",
                f"- Job examples: {', '.join(f'`{example}`' for example in item['examples'][:12])}"
                + (" ..." if len(item["examples"]) > 12 else ""),
                f"- Action dependencies: {', '.join(item['uses']) if item['uses'] else 'none detected'}",
                f"- Atomic command surfaces: {', '.join(item['atoms']) if item['atoms'] else 'none detected'}",
            ]
        )
    final_lines.extend(["", "## Deduplicated Atomic Surfaces"])
    for atom, count in atom_counter.most_common():
        final_lines.append(f"- `{atom}`: {count} command occurrence(s)")
    final_lines.extend(
        [
            "",
            "## Copied Artifact Layout",
            "- `.github/workflows/`: uniquely named copies of every discovered workflow file.",
            "- `reports/workflows/`: one workflow research report per copied workflow.",
            "- `scripts/`: copies of existing script files referenced by workflow and local-action run commands.",
            "- `reports/scripts/`: one script research report per copied script.",
        ]
    )
    (TARGET / "reports" / "final-workflow-component-analysis.md").write_text(
        "\n".join(final_lines) + "\n", encoding="utf-8"
    )

    print(f"workflows={len(workflow_rows)}")
    print(f"scripts={len(copied_scripts)}")
    print(f"reports={(TARGET / 'reports').as_posix()}")


if __name__ == "__main__":
    main()
