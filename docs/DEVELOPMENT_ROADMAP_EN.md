# Particle Studio --- Development Roadmap

## 1. Purpose

This roadmap defines the development sequence from the Particle Studio
concept to a working first release that generates shareable outputs.
Phases are ordered by dependency. The core acceptance criteria of the
current phase should be met before moving to the next one.

## 2. Fixed product decisions

-   Processing and particle engine: Python.
-   User interface: Web-based.
-   Visual primitive: A single particle (`Particle`).
-   Input: Color or black-and-white images.
-   Output color mode: Monochrome or color.
-   Background: Black by default.
-   Main animation: Start from an empty/dark screen and progressively
    form the image using particles.
-   Primary output: A single-file, mobile-friendly HTML document.
-   Secondary output: A single-file terminal output; the initial target
    is Windows `.cmd`.

## 3. Phases

### Phase 0 --- Project foundation and contracts

**Goal:** Define module boundaries and shared data contracts before
implementation.

Tasks: - Create the project directory structure. - Treat the
architecture and algorithm documents as references. - Define the data
models. - Document image-sampling, particle, and animation rules. -
Select the Python version and core dependencies.

Exit criteria: - Module responsibilities and data exchange must be
clear.

### Phase 1 --- Image Processing Core

**Goal:** Convert input images into normalized data suitable for
particle generation.

Tasks: - Image loading and validation. - RGB/RGBA and grayscale
support. - Resizing while preserving aspect ratio. - Brightness,
contrast, and gamma operations. - Controlled noise reduction/enhancement
steps. - Prepare a density map for sampling.

Exit criteria: - Images with different dimensions and color modes must
be processed consistently.

### Phase 2 --- Particle Engine

**Goal:** Generate many small particles from image data.

Tasks: - Implement the single `Particle` model. - Develop pixel/area
sampling strategies. - Calculate particle coordinates and
color/brightness values. - Add particle density and maximum-particle
limits. - Support deterministic generation through a seed. - Validate
particle data.

Exit criteria: - Generated particles must represent the main shapes and
tones of the source image recognizably.

### Phase 3 --- Animation Engine

**Goal:** Make particles progressively form the image, starting from an
empty screen.

Tasks: - Reveal-order algorithm. - Duration, FPS, and delay settings. -
Opacity and brightness transitions. - Transition from dark tones to
sampled source colors in color mode. - Optional motion/jitter/trail
effects. - Ensure the final frame displays the complete image.

Exit criteria: - Playback must progress smoothly from beginning to end
and produce the complete image at the final state.

### Phase 4 --- Rendering Layer

**Goal:** Make shared particle and animation data drawable on different
targets.

Tasks: - Define a shared rendering contract. - Black background and
scaling rules. - Particle size and drawing order. - Monochrome and color
rendering behavior. - Rendering correctness and performance tests.

Exit criteria: - The rendering layer must remain independent of
processing and export logic.

### Phase 5 --- Web Interface

**Goal:** Build a web interface where users can upload images and select
settings.

Tasks: - Image upload area. - Preview area. - Monochrome/color output
selection. - Particle density and animation settings. - HTML/terminal
format selection. - Processing status and error messages. - Responsive
mobile interface.

Exit criteria: - Users must be able to complete the main workflow
through the interface.

### Phase 6 --- Standalone HTML Export

**Goal:** Generate a single HTML file that requires no application
installation or server.

Tasks: - Embed particle data in the file. - Embed drawing and animation
code. - Enable autoplay. - Responsive canvas/drawing surface. - Offline
operation. - Mobile browser testing. - File-size and performance
optimization.

Exit criteria: - When the generated HTML is sent to another device, it
must open and play the animation without installing the application.

### Phase 7 --- Terminal Export

**Goal:** Generate a single-file terminal output from the same animation
data.

Tasks: - Terminal coordinate/character mapping. - Monochrome and, where
supported, colored character output. - Animation timing. - Windows
`.cmd` launch flow. - Terminal size and ANSI support checks.

Exit criteria: - Running a single `.cmd` file in a supported Windows
environment must start the animation.

### Phase 8 --- Quality, Optimization and Release

**Goal:** Make the first release reliable and shareable.

Tasks: - Unit and integration tests. - HTML/terminal data consistency
tests. - Visual quality tests at different resolutions. - Mobile and
desktop performance tests. - Error scenarios and large-file tests. -
Setup and usage documentation. - README and sample outputs.

Exit criteria: - Core use cases must be repeatable, tested, and
documented.

## 4. Prioritization

Priority order:

1.  Image-processing correctness
2.  Particle quality and density
3.  Progressive-reveal animation
4.  Single-file, mobile-friendly HTML
5.  Web interface experience
6.  Terminal output
7.  Additional effects and advanced optimization

HTML comes before terminal because it can be easily sent to and opened
by people who do not own a computer.

## 5. Testing strategy

-   Images with different aspect ratios.
-   Color and grayscale sources.
-   Bright, dark, and high-contrast images.
-   Low and high particle densities.
-   Small-screen phones and desktop browsers.
-   Offline HTML opening.
-   Repeatable output generation with identical settings.
-   Memory and frame-rate behavior at high particle counts.

## 6. Scope management

The first release's primary quality target is to progressively form the
source image using many small particles. Audio, user accounts, cloud
storage, social-platform integration, and advanced editing features are
not mandatory parts of the first release.

This roadmap is a living document. The phase order should only change
when justified by technical dependencies or test results.
