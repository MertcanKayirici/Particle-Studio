"""Shared application configuration and defaults."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RenderConfig:
    width: int = 1000
    height: int = 750
    max_particles: int = 100_000
    particle_size: float = 1.0
    background: str = "#000000"
    color_mode: str = "color"  # "color" or "grayscale"
    visual_mode: str = "particles"  # "particles" or "ascii"
    reveal_duration: float = 8.0
