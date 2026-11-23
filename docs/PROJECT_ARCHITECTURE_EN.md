# Particle Studio — Project Overview and Architecture

> This document describes the project's purpose, core product decisions,
> architectural layers, module responsibilities, and data flow.
> **This is not the main `README.md`.** The main README will be prepared
> as the project features are completed and actual usage becomes clear.

## 1. Project Purpose

Particle Studio is an application that recreates a user-selected image
using particles or ASCII characters and can export the resulting
formation as an animation.

The application's defining feature is not simply converting a photo
into particles. The image starts on a completely black or nearly empty
screen and gradually emerges over time. When the animation finishes,
the source image should be recognizable and as detailed as possible
within the selected visual style.

Easy sharing of the generated animation is one of the main product
goals. Therefore, the primary output is a standalone HTML file. This
file can be sent to another person through messaging applications and
can play the animation when opened in a modern browser.

## 2. Core Product Decisions

| Area | Decision |
|---|---|
| Image processing engine | Python |
| User interface | Web-based |
| Core visual primitive | Single particle |
| Input images | Color or black and white |
| Output color mode | Color or monochrome |
| Visual representation | Particles or ASCII |
| Main animation | Full progressive reveal |
| Default background | Black |
| Primary output | Single-file standalone HTML |
| Secondary output | Terminal/CMD animation |
| Target devices | Mobile and desktop browsers; supported desktop terminals for terminal output |

These decisions define the initial architecture. Additional effects and
output formats may be introduced later, but the core particle model and
standalone HTML output should remain fundamental parts of the project.

## 3. User Experience

The expected basic user flow is:

1. The user opens the application.
2. The user uploads an image.
3. The user selects a visual representation: particles or ASCII.
4. The user selects an output color mode: color or monochrome.
5. The user adjusts settings such as visual density, particle size,
   animation duration, and other available options.
6. The user generates a preview and reviews the result.
7. The user selects an output format.
8. The application exports the animation.

The primary output intended for sharing with a friend is a single HTML
file. The recipient should not need to install Python, Particle Studio,
or any other development tool.

## 4. Visual Generation Behavior

### 4.1 Particle Mode

In Particle mode, the image is formed by a large number of small
particles.

- Particles should be small; image detail should come from using many
  particles.
- Particle positions and visual properties should be derived from the
  source image.
- Particle colors should be determined from the source image's colors
  or brightness values, according to the selected output mode.
- The order in which particles appear is part of the animation.
- Density and particle size should be configurable.

### 4.2 ASCII Mode

In ASCII mode, the image is represented by characters selected
according to brightness and, when applicable, color values.

- Character density affects the level of image detail.
- Dark and bright areas are represented by different characters.
- Terminal output should account for the aspect ratio of terminal
  character cells.
- HTML output should scale to mobile screens without causing horizontal
  overflow.

### 4.3 Progressive Reveal Animation

The main effect is the gradual formation of the image from beginning
to end.

1. The animation starts with a black or nearly empty screen.
2. The first particles/characters appear.
3. Additional particles emerge and begin forming the main shape.
4. Image details become increasingly visible.
5. When the animation finishes, the complete image is visible.

In color mode, not only the particles but also their colors may become
more pronounced over time. For example, the main subject can initially
appear faint or with low brightness against a black background, then
gradually transition toward its actual colors.

## 5. High-Level Architecture

The architecture consists of layers with separated responsibilities:

```text
                         USER
                           |
                           v
                  WEB USER INTERFACE
                  - Image upload
                  - Setting selection
                  - Preview
                  - Export request
                           |
                           v
                    PYTHON ENGINE
                  - Image loading
                  - Image analysis
                  - Particle generation
                  - Reveal ordering
                  - Animation data
                           |
                  +--------+--------+
                  |                 |
                  v                 v
            HTML EXPORTER     TERMINAL EXPORTER
            - CSS             - ASCII frames
            - JavaScript      - Timing
            - Animation data  - Terminal playback
                  |                 |
                  v                 v
          SINGLE HTML FILE    TERMINAL OUTPUT
```

### 5.1 Web Interface

The web interface manages interaction with the user. It provides image
upload, setting selection, preview, and export operations.

The interface should not reimplement particle generation algorithms.
Image processing and animation-data generation remain responsibilities
of the Python engine.

### 5.2 Python Engine

The Python engine is the application's processing center. It analyzes
the source image, generates particles, determines the order in which
particles appear, and prepares animation data for the exporters.

The engine should remain independent of the web interface and output
formats. This allows the same generation logic to be used for both HTML
and terminal output.

### 5.3 Export Layer

The export layer converts the shared animation data prepared by the
engine into the selected output format.

**HTML exporter:**

- Produces a single `.html` file.
- Embeds the required CSS and JavaScript inside the file.
- Includes the animation data inside the file.
- Aims to work without external libraries, a server, or an internet
  connection.
- Supports mobile and desktop screens.

**Terminal exporter:**

- Plays ASCII frames in chronological order.
- Updates the terminal screen to show the progressive formation effect.
- Should account for terminal dimensions and character-cell proportions.

## 6. Python Package and Module Responsibilities

Planned source-code structure:

```text
src/
└── particle_studio/
    ├── core/
    │   └── models.py
    ├── imaging/
    │   ├── loader.py
    │   └── analysis.py
    ├── particles/
    │   └── generator.py
    ├── animation/
    │   └── reveal.py
    ├── rendering/
    │   ├── ascii_renderer.py
    │   └── particle_renderer.py
    ├── exporters/
    │   ├── html_exporter.py
    │   └── terminal_exporter.py
    ├── config.py
    └── __main__.py
```

| Module | Responsibility |
|---|---|
| `core/` | Core data models shared between modules |
| `imaging/` | Loading, validating, and analyzing image files |
| `particles/` | Generating individual particles from image data |
| `animation/` | Preparing the appearance order and timeline for particles/characters |
| `rendering/` | Particle and ASCII preview/rendering operations |
| `exporters/` | Converting shared animation data into HTML or terminal output |
| `config.py` | Application and generation defaults |
| `__main__.py` | Starting the application from the command line |

### 6.1 Shared Data Model

A particle is the engine's core visual primitive. A particle may contain
at least the following information:

- Normalized X and Y position
- Red, green, and blue color components
- Brightness value
- Appearance order in the animation

Animation data should be organized in a format that exporters can use.
This prevents the HTML and terminal exporters from having to repeat
image analysis and particle generation.

The final data-model fields may evolve as performance and animation
requirements are tested.

## 7. Technology Selection

| Technology | Purpose |
|---|---|
| Python 3.11+ | Image processing and generation engine |
| Pillow | Opening image files and basic image operations |
| NumPy | Pixel, color, brightness, and sampling calculations |
| HTML | Shareable output and web interface |
| CSS | Interface and output presentation |
| JavaScript | Playback of animations in HTML output |
| Canvas | Target approach for efficiently drawing many particles in the browser |
| Pytest | Automated testing |
| Ruff | Python code quality and formatting checks |

The standalone HTML output should not load external JavaScript/CSS
libraries at runtime. This makes it easier for the file to work offline
and independently after it has been shared.

## 8. Data Flow

Example flow for Particle mode:

1. The image loader opens the source file and converts it to a supported
   common color representation.
2. The image analysis module extracts pixel, brightness, color, and,
   where necessary, edge information.
3. The particle generator creates particle positions and visual
   properties from the analysis data.
4. The animation module determines the appearance order and timing of
   the particles.
5. The preview engine displays the result inside the application.
6. If the user selects HTML export, the HTML exporter combines the
   animation data, CSS, and JavaScript player into one file.
7. When the file is opened in a browser, the animation plays using the
   embedded data.

ASCII mode follows the same general flow, but represents the image
using characters instead of particles.

## 9. Requirements for Standalone HTML Output

The HTML file is the project's most important deliverable. Therefore,
the following requirements should be considered from the beginning:

- It must be shareable as a single file.
- CSS, JavaScript, and animation data must be embedded in the file.
- It must not require Python or a local server.
- It should work without an internet connection.
- It should be usable in Android and iOS browsers.
- It should work in Windows and Linux desktop browsers.
- It must adapt to different screen sizes.
- Animation start and playback behavior must respect browser
  restrictions.
- File size and memory usage must remain controlled for large
  animation datasets.

Mobile browser performance must be validated through real-device
testing, especially regarding particle count and animation-frame
encoding.

## 10. Performance and Quality Goals

- Create detailed images using many small particles.
- Keep memory consumption under control as particle count increases.
- Display the beginning, middle, and final stages of the animation
  consistently.
- Support color and monochrome modes through the same generation
  infrastructure.
- Avoid unnecessarily large HTML files.
- Provide acceptable playback smoothness on mobile devices.
- Allow modules to be tested independently.

Exact particle limits, resolutions, and target frame rates will be
determined after performance measurements.

## 11. Development Phases

1. **Project foundation:** Package structure, configuration, and shared
   data models.
2. **Image loading:** File validation and conversion to a standard
   image representation.
3. **Image analysis:** Extraction of brightness, color, and sampling
   data.
4. **Particle generation:** Creation of individual particles with
   position, color, and brightness values.
5. **Progressive animation:** Preparation of the reveal sequence from
   an empty screen to the complete image.
6. **ASCII generation:** Character-based visual representation.
7. **Preview:** Displaying the generated animation inside the
   application.
8. **HTML export:** Independent, single-file animation output.
9. **Compatibility and optimization:** Mobile/desktop browser testing
   and performance improvements.
10. **Terminal output:** Playing the ASCII animation in a terminal.
11. **Interface integration:** Connecting the user interface to the
    Python engine.

## 12. Technical Topics Not Yet Finalized

The following topics will be decided according to requirements and
test results:

- How the web interface communicates with the Python engine: a local
  API, another local communication layer, or a packaged execution
  approach.
- The exact drawing and data-transfer method used for previews.
- The detailed algorithm used to determine particle appearance order.
- How animation data is stored and compressed inside the HTML file.
- Whether terminal output is delivered as a single file or in a format
  that requires a supporting runtime.
- Resolution, particle limits, and quality profiles for large images.

These topics will be decided as the core modules are developed and
prototypes are tested.

## 13. Architectural Principles

1. **Single responsibility:** Each module performs a specific task.
2. **Independent engine:** Image-processing code is not coupled to
   interface code.
3. **Shared animation data:** Different exporters use the same
   generation output.
4. **Independent output:** A recipient of the HTML file does not need
   the development environment.
5. **Measure before optimizing:** Particle counts and frame rates are
   determined through tests, not guesses.
6. **Incremental development:** First validate the generation
   algorithm, then complete interface and export integration.

---

**Document status:** Architecture draft. It will be updated as the
application develops and actual behavior and technical decisions become
clear.
