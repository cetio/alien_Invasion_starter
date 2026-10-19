"""Interface for game entities."""
from abc import ABC, abstractmethod


class Entity(ABC):
    """Base class for all game entities for tick and draw cycles."""

    layer: int
    priority: int

    @abstractmethod
    def update(self) -> None:
        """Update the entity's state for this frame."""

    @abstractmethod
    def draw(self) -> None:
        """Draw the entity to the screen."""
