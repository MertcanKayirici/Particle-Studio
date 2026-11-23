# Particle Studio --- Data Models

## 1. Purpose

This document defines the core data structures used by Particle Studio's
Python-based image-processing and particle engine. Its goal is to make
image analysis, particle generation, animation, and export operate
through consistent data contracts.

This is an architectural design document. Exact field names and types
may be finalized during implementation, but the responsibilities
described here should remain stable.

## 2. Core design principles

-   **Single primitive:** A `Particle` is the only visual building
    block.
-   **Color flexibility:** Input images may be colored or grayscale.
    Output may be monochrome or colored.
-   **Shared animation model:** HTML and terminal exports use the same
    particle data and animation timeline.
-   **Portable output:** An exported file contains the data and playback
    logic it needs.
-   **Separated responsibilities:** Image, particle, animation, color,
    and export data remain distinct.

## 3. Core models

### 3.1 ImageSource

Represents the user-provided source image and the information required
for processing.

  Field                Description
  -------------------- --------------------------------------------
  `source_id`          Unique source identifier
  `width` / `height`   Image dimensions
  `mode`               Source color mode: RGB, RGBA, or grayscale
  `pixel_data`         Pixel data to be processed
  `metadata`           File type and optional source information

The original image may be preserved unchanged. Processing steps can
operate on a normalized representation when needed.

### 3.2 ProcessingConfig

Contains settings used to transform an image into particles.

Suggested fields:

-   `target_width`, `target_height`
-   `sampling_density`
-   `brightness_threshold`
-   `contrast`
-   `gamma`
-   `sharpen_amount`
-   `max_particles`
-   `background_color`
-   `output_color_mode`

Default parameter values should live in a profile/preset layer rather
than being scattered as hard-coded constants throughout the engine.

### 3.3 Particle

The system's single visual primitive. Each particle is rendered as a
tiny dot or an equivalent terminal character.

  Field            Description
  ---------------- --------------------------------------------------
  `id`             Unique particle identifier
  `x`, `y`         Normalized or output coordinates
  `size`           Particle size
  `color`          RGB/RGBA color information or grayscale value
  `brightness`     Visual brightness
  `opacity`        Visibility/alpha value
  `depth`          Optional drawing order or layer value
  `reveal_order`   Order/time at which the particle becomes visible

Particles should be small and dense. Visual quality should come from the
combined density and tonal variation of many small particles, rather
than a small number of oversized dots.

### 3.4 ParticleSet

A collection of particles representing one image.

-   References the source image identifier.
-   Stores particles in a deterministic order.
-   Carries the total particle count and output dimensions.
-   Provides common input to the HTML and terminal exporters.

### 3.5 ColorProfile

Defines color generation and conversion rules.

Supported output modes:

-   `monochrome`: White/gray particles on a black background.
-   `color`: Particles retain colors sampled from the source image, on a
    black background.

In color mode, particles may begin dark or with low opacity and
gradually approach their final colors during playback. In monochrome
mode, the same timing model is applied to brightness values.

### 3.6 AnimationConfig

Defines how particles transition from the initial state to the completed
image.

Suggested fields:

-   `duration_ms`
-   `fps`
-   `start_delay_ms`
-   `reveal_strategy`
-   `order_seed`
-   `fade_in`
-   `brightness_transition`
-   `color_transition`
-   `particle_motion`
-   `hold_final_frame`

The signature animation starts from an almost empty/dark screen,
progressively reveals particles, and eventually forms the complete
source image. Motion, jitter, or trail effects are optional parameters;
they do not replace the core progressive-reveal animation.

### 3.7 ExportConfig

Defines the export target and how the output file is generated.

  Field                              Description
  ---------------------------------- --------------------------------------------
  `format`                           `html` or `terminal`
  `output_path`                      Destination file path
  `canvas_width` / `canvas_height`   Visual output dimensions
  `include_controls`                 Whether playback controls are included
  `embed_assets`                     Whether required data is embedded
  `mobile_responsive`                Whether the HTML output is mobile-friendly

## 4. Data flow

1.  Create an `ImageSource`.
2.  Normalize and analyze the image using `ProcessingConfig`.
3.  Generate a `ParticleSet` using the sampling and density rules.
4.  Transform colors through `ColorProfile`.
5.  Determine particle reveal order and transitions through
    `AnimationConfig`.
6.  Pass `ExportConfig` to the selected exporter.
7.  Generate a standalone HTML or terminal output file.

## 5. Validation and consistency

-   Coordinates must remain within output bounds.
-   Particle count must not exceed `max_particles`.
-   Color channels must use valid ranges.
-   Animation order must be deterministic; identical seeds and settings
    should produce identical results.
-   HTML and terminal outputs must be based on the same `ParticleSet`
    and animation timeline.
-   Invalid or missing settings must be validated before export begins.

## 6. Versioning

An output schema version should be embedded in exported files. This will
make it possible to define compatibility strategies when model fields
change in future versions.

Example conceptual field: `schema_version`.

## 7. Out of scope

This document does not define a database schema, user account model, or
cloud synchronization. The first release focuses on local processing and
portable, self-contained output files.
