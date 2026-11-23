"""Core data models shared by processing and export modules."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Particle:
    """One visual particle in normalized image coordinates."""

    x: float
    y: float
    red: int
    green: int
    blue: int
    brightness: float
    reveal_order: int


@dataclass(frozen=True, slots=True)
class ParticleFrame:
    """A collection of particles belonging to one animation frame."""

    timestamp: float
    visible_particle_count: int
