"""Copy this rule package with only the judge rules a diff can change the verdicts of.

A judge rule's verdicts change with its skill, its binding (which names its model), its
eval, and the gates its binding triggers on. A change to the package config, the CI
workflow or this script can change every rule's. `codeguard eval` on the copy judges
only the rules kept.

Usage: judge_eval_package.py <base> <out>. Prints the rules kept, and writes nothing
when there are none.
"""

import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
EVERY_RULE = {"codeguard-package.yaml", ".github/workflows/ci.yaml", "scripts/judge_eval_package.py"}


def changed_paths(base: str) -> set[str]:
    diff = subprocess.run(
        ["git", "diff", "--name-only", base, "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return set(diff.stdout.split())


def judge_triggers(ruleset: Path) -> dict[str, set[str]]:
    rules: dict[str, set[str]] = {}
    for binding in sorted((ruleset / "bindings").glob("*.yaml")):
        config = yaml.safe_load(binding.read_text())
        if "skill" in config:
            rules[binding.stem] = set(config.get("triggers", []))
    return rules


def affected(ruleset: str, rules: dict[str, set[str]], paths: set[str]) -> set[str]:
    if paths & EVERY_RULE:
        return set(rules)
    kept: set[str] = set()
    for path in paths:
        parts = Path(path).parts
        if len(parts) < 3 or parts[0] != ruleset:
            continue
        kind, name = parts[1], Path(parts[2]).stem
        if kind in {"skills", "bindings", "rule-evals"} and name in rules:
            kept.add(name)
        elif kind == "gates":
            kept |= {rule for rule, triggers in rules.items() if name in triggers}
    return kept


def main(base: str, out: Path) -> None:
    rulesets = yaml.safe_load((ROOT / "codeguard-package.yaml").read_text())["rulesets"]
    paths = changed_paths(base)
    plans = {name: judge_triggers(ROOT / name) for name in rulesets}
    kept = {name: affected(name, rules, paths) for name, rules in plans.items()}
    if not any(kept.values()):
        return
    shutil.copytree(ROOT, out, ignore=shutil.ignore_patterns(".git", "drafts"))
    subprocess.run(["git", "init", "--quiet"], cwd=out, check=True)
    for name, rules in plans.items():
        for rule in rules.keys() - kept[name]:
            shutil.rmtree(out / name / "skills" / rule)
            (out / name / "bindings" / f"{rule}.yaml").unlink()
            (out / name / "rule-evals" / f"{rule}.yaml").unlink()
        for rule in sorted(kept[name]):
            print(f"{name}/{rule}")


if __name__ == "__main__":
    main(sys.argv[1], Path(sys.argv[2]))
