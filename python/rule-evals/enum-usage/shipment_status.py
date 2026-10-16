from dataclasses import dataclass
from enum import StrEnum


class ShipmentStatus(StrEnum):
    PENDING = "pending"
    SHIPPED = "shipped"


@dataclass(frozen=True)
class Shipment:
    status: ShipmentStatus


def shipped() -> Shipment:
    return Shipment(status="shipped")
