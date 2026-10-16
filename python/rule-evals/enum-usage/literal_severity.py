from dataclasses import dataclass
from typing import Literal

type Severity = Literal["error", "warning"]


@dataclass(frozen=True)
class Override:
    severity: Severity = "error"


def relaxed() -> Override:
    return Override(severity="warning")
