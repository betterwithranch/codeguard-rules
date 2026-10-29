"""Print the judge rules a diff can change the verdicts of, one per line: the runs its
eval needs, then the rule's id.

A judge rule's verdicts change with its skill, its binding (which names its model), its
eval, and the gates its binding triggers on; such a rule runs 20 times. A change to the
package config, the CI workflow (which pins the codeguard version) or this script can
change every rule's, so every other rule runs 3 times. CI passes each id to
`codeguard eval --rule` with its `--repeat`, and skips the eval when none is printed.

Usage: affected_judge_rules.py <base>
"""

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CHANGED_RULE_RUNS = 20
EVERY_RULE_RUNS = 3
EVERY_RULE = {"codeguard-package.yaml", ".github/workflows/ci.yaml", "scripts/affected_judge_rules.py"}


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


def changed(ruleset: str, rules: dict[str, set[str]], paths: set[str]) -> set[str]:
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


def main(base: str) -> None:
    rulesets = yaml.safe_load((ROOT / "codeguard-package.yaml").read_text())["rulesets"]
    paths = changed_paths(base)
    for name in rulesets:
        rules = judge_triggers(ROOT / name)
        kept = changed(name, rules, paths)
        for rule in sorted(rules):
            if rule in kept:
                print(CHANGED_RULE_RUNS, rule)
            elif paths & EVERY_RULE:
                print(EVERY_RULE_RUNS, rule)


if __name__ == "__main__":
    main(sys.argv[1])
