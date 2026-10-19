from dataclasses import dataclass
from enum import StrEnum


class ShipmentStatus(StrEnum):
    PENDING = "pending"
    SHIPPED = "shipped"


@dataclass(frozen=True)
class Shipment:
    status: ShipmentStatus


def label(shipment: Shipment) -> str:
    return f"Shipment is {shipment.status.value}"
