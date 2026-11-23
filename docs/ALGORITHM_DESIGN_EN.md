# Particle Studio — Algorithm Design

> This document describes the planned algorithms for image analysis,
> particle/ASCII generation, and progressive animation in Particle Studio.
>
> **Status:** Design phase. The workflow described here is the planned
> algorithm; it should not be considered implemented code or code that
> has already passed performance testing.
>
> Related document: [`PROJECT_ARCHITECTURE.md`](PROJECT_ARCHITECTURE.md)

---

## 1. Algorithm Objective

Recreate a source image using one of two visual representation modes:

1. **Particle mode:** The image is formed by positioning a large number
   of small, individual particles.
2. **ASCII mode:** The image is represented by text characters selected
   according to brightness and color information.

Both modes share the same behavior: instead of displaying the image
all at once, the animation starts on a black or nearly empty screen and
forms the image over time.

The output color mode is selected separately:

- **Monochrome:** Black and white / grayscale tones.
- **Color:** Colors derived from the source image.

Therefore, the visual representation mode and the color mode are
independent options. For example, Particle + Color and ASCII +
Monochrome are both valid combinations.

## 2. General Processing Pipeline

```text
Source image
    |
    v
Load and validate image
    |
    v
Resize / preserve aspect ratio
    |
    v
Analyze pixel colors and brightness
    |
    +------------------------------+
    |                              |
    v                              v
Particle generation           ASCII cell generation
    |                              |
    +---------------+--------------+
                    |
                    v
             Apply color mode
                    |
                    v
          Calculate reveal order
                    |
                    v
             Build timeline
                    |
          +---------+---------+
          |                   |
          v                   v
      HTML animation      Terminal frames
```

The purpose of this pipeline is to keep image analysis and animation
data generation independent of the output format. HTML and terminal
exporters should use the same underlying generation result.

## 3. Image Preprocessing

### 3.1 File Loading and Validation

When an input file is loaded:

- Check whether the file format is supported.
- Read the image width and height.
- Reject empty or corrupted files.
- Apply a safe processing limit for very large images.
- Convert the image into the standard pixel representation used by
  the algorithm.

The image formats supported in the first release will be finalized
during development. JPEG and PNG are suitable initial candidates.

### 3.2 Resizing

The image is processed according to the output width/height selected
by the user or the chosen quality profile.

- Preserve the aspect ratio.
- Do not stretch the image unnecessarily.
- Processing resolution directly affects the number of generated
  particles/characters.
- Fitting the image into the viewport for mobile and desktop HTML
  output is handled separately by the exporter.

### 3.3 Color and Brightness Analysis

RGB color information is obtained for each pixel. A perceptually
weighted brightness calculation can be used as an initial approach:

```text
L = 0.2126 * R + 0.7152 * G + 0.0722 * B
```

Here, R, G, and B are normalized color components in the range 0–1.

This value can be used especially in monochrome mode and when selecting
ASCII characters. The final brightness transformation will be tuned
through visual testing.

## 4. Particle Mode

### 4.1 Core Primitive

The core primitive in Particle mode is the **individual particle**.
Each particle is drawn as a small visual dot. A large number of small
particles work together to form the shape and details of the source
image.

Particles should not be grouped into large blobs or oversized cells.
Density should be achieved by increasing the number of small particles.

### 4.2 Determining Particle Positions

A practical initial approach is to generate candidate positions over
the processed image.

Possible strategies:

- **Uniform sampling:** Place candidate points at regular intervals
  across the image area.
- **Random sampling:** Select candidate points randomly from the
  image area.
- **Brightness/density sampling:** Generate more candidate points in
  selected regions according to brightness or contrast.

The algorithm should remain simple and measurable in the first
implementation. Uniform or controlled random sampling can be applied
first and evaluated; more advanced density distribution can be added
as a later improvement.

### 4.3 Particle Properties

A particle's data model should contain at least the following
information:

| Field | Description |
|---|---|
| `x` | Normalized horizontal position |
| `y` | Normalized vertical position |
| `r`, `g`, `b` | Color derived from the source image |
| `brightness` | Brightness value |
| `reveal_order` | Appearance order in the animation |

Drawing properties such as particle size and opacity may also be
required. Whether these belong in the data model or in render settings
will be clarified during implementation.

### 4.4 Color Mode

**Monochrome:**

- Particle color is converted to a grayscale tone derived from pixel
  brightness.
- Light-toned particles form the image against a black background.

**Color:**

- Each particle receives the color at its corresponding position in
  the source image.
- At the beginning of the animation, particle colors may appear at
  reduced intensity.
- Over time, colors can transition toward their final values.

Color emergence is part of the animation; it should not be treated as
a separate filter that changes the source image's color information.

## 5. ASCII Mode

### 5.1 Cell-Based Representation

In ASCII mode, the image is converted into a grid of character cells.
Each cell represents the corresponding area of the source image.

The average brightness of each cell is calculated, and a character
appropriate for that brightness level is selected.

### 5.2 Character Ramp

A character ramp consists of characters whose visual density increases
from dark areas to bright areas. An example starting ramp is:

```text
 .:-=+*#%@
```

The character ordering should be tested according to the font and
output environment. The same characters may appear to have different
visual densities in a terminal and in HTML.

### 5.3 Color ASCII

In Color mode, each character's color is derived from the corresponding
cell in the source image. In Monochrome mode, the cell brightness is
used as a grayscale tone.

Styling each colored character separately in HTML may increase file
size. Therefore, data size and rendering performance should be measured
during the export phase.

### 5.4 Terminal Compatibility

Terminal character cells are not square. Therefore, the aspect ratio
of ASCII output should be adjusted to account for the approximate
width-to-height ratio of terminal character cells.

If the terminal is small, the output width should be limited or an
appropriate resolution should be selected for the user.

## 6. Progressive Reveal

### 6.1 Core Behavior

The first animation frame should be black or nearly empty. Particles
or ASCII cells become visible in the specified order. The complete
image should be formed in the final frame.

### 6.2 Reveal Ordering

Each item receives a `reveal_order` value. This value determines when
the item appears in the animation.

Reveal-order strategies to evaluate:

- Random appearance order.
- Expansion from the center outward.
- Formation from the outer edges toward the center.
- Row/column or scan-line order.
- Controlled mixed ordering based on image regions.

The first version should implement one base ordering strategy.
Additional strategies can be added later as selectable effects. The
default strategy should be chosen after comparing visual examples.

### 6.3 Timeline

The reveal order is connected to the total animation duration.

A simple model:

```text
progress = elapsed_time / duration
visible_count = progress * total_item_count
```

`progress` is clamped to the range 0–1. `visible_count` represents
the number of items that should be visible by the current time.

Easing or different speed curves can be added later. For example, the
formation could start slowly, accelerate in the middle, and slow down
again near the end.

### 6.4 How Particles Appear

When an item reaches its reveal time, it may:

- Become visible.
- Perform a short opacity transition.
- Become more prominent through a small brightness increase.

These behaviors should be tested for visual quality and performance
cost. The first goal is smooth playback while a large number of items
appear.

### 6.5 Color Emergence

A two-stage appearance can be evaluated in Color mode:

1. The particle/character begins to appear.
2. Its color transitions from a low-intensity or faded appearance
   toward the source image's final color.

In Monochrome mode, a brightness/opacity transition is used instead
of a color transition.

## 7. Animation Data and Output Independence

Instead of generating HTML or terminal code directly, the generation
engine should prepare a shared animation data structure.

Conceptual data example:

```json
{
  "width": 1000,
  "height": 750,
  "mode": "particle",
  "color_mode": "color",
  "duration_ms": 6000,
  "background": "#000000",
  "items": [
    {
      "x": 0.42,
      "y": 0.31,
      "color": [230, 190, 210],
      "brightness": 0.78,
      "reveal_order": 120
    }
  ]
}
```

This example illustrates the concept of the data structure; it is not
the final schema. The actual field names and serialization format will
be finalized in `DATA_MODELS.md`.

Shared data provides the following benefits:

- The HTML exporter uses the same animation data.
- The terminal exporter uses the same reveal order.
- Image analysis does not need to run again for each output format.
- Adding new output formats becomes easier.

## 8. Differences Between HTML and Terminal Playback

### HTML

- The animation plays in a browser.
- The required styles, JavaScript, and animation data are embedded
  inside a single HTML file.
- The output adapts to mobile screen sizes.
- The goal is to avoid requiring an external server or Python
  installation.
- The animation is designed to start automatically when the file is
  opened. Browser restrictions may require user interaction for
  additional features such as audio.

### Terminal

- The animation is played frame by frame at timed intervals.
- A new frame is displayed by clearing the terminal screen or updating
  the cursor position.
- The supported terminal color mode and character width must be
  considered.
- Terminal output is not as platform-independent as a single HTML file.

## 9. Performance and Quality Metrics

The following metrics should be tracked during algorithm development:

- Number of particles/characters.
- Generation time.
- Animation data file size.
- HTML file opening time.
- Playback smoothness in desktop browsers.
- Playback smoothness in mobile browsers.
- Recognizability of the source image in the final frame.
- Ability of small particles to preserve image details.
- Visual quality of color transitions.

Low, medium, and high density profiles can be used in initial tests.
Exact particle-count and resolution limits should not be fixed before
measurements are taken.

## 10. Development Order

1. Image loading and validation.
2. Convert the image to a standard size.
3. Basic Particle generation.
4. Monochrome Particle preview.
5. Reveal ordering and progressive animation.
6. Color Particle mode and color emergence.
7. ASCII generation.
8. Monochrome and Color ASCII modes.
9. Finalize the shared animation data model.
10. Single-file HTML exporter.
11. Mobile browser testing.
12. Terminal exporter.
13. Performance and quality improvements.

This order validates the core visual-generation algorithm early and
builds export functionality on top of a stable data model.

---

## 11. Open Technical Decisions

The following topics have not yet been finalized and should be decided
based on prototypes and test results:

- Default sampling strategy for particle positions.
- Relationship between particle density and brightness.
- Default reveal-order strategy.
- Whether particle opacity/scale transitions should be used.
- Duration and easing curve for color emergence.
- Choice of drawing approach, such as Canvas or SVG, for HTML animation.
- Safe item-count and resolution limits for mobile devices.
- Scope of the ASCII character ramp and terminal color support.

These decisions should be made through small prototypes and real-device
testing.
