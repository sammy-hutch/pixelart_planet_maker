
# inputs

- pattern:              **PATTERN** (multiselect string)
    - **"landmasses"**: primary blobs against secondary sea. pct controls how much primary. blob locations randomly formed. Earth-style
        - if so, %?     **LAND_PCT**
    - **"cracked"**: primary plates divided by secondary cracks. land size determines average size of plates. secondary pct is minimal, just enough to fill gaps between plates
        - if so, size?  **LAND_SIZE**
    - **"scattered"**: primary and secondary in equal and random distribution.
        - if so, %?     **PRIMARY_PCT**
    - "bands": primary horizontal stripes against secondary horizontal stripes. Jupiter-style. could be applied on top of a "landmasses"-style base with low landmass pct to create spots that show through the stripes
        - if so, width? **BAND_WIDTH** 
    - **rivers**: primary base with secondary rivers overlaid
        - if so, %?     **RIVER_PCT**
    each pattern has different painting logic that gets applied.
    multiple patterns can be layered, so it should be possible to select multiple, and they should be ordered.

- primary palette: selection of colours for use in primary
    - primary color 1:  **PRIMARY_COLOR_1** (RGBA)
    - primary color 2:  **PRIMARY_COLOR_2**
    etc..

- secondary palette: selection of colours for use in secondary
    - secondary color 1:**SECONDARY_COLOR_1**
    etc..

- ice caps?
    - if so, %?         **ICE_PCT**
    - and what color?   **ICE_COLOR**

- clouds?
    - if so, %?         **CLOUD_PCT**
    - and what style?   **CLOUD_STYLE** e.g.
        - "blobby"
        - "wispy"
    - and what color?   **CLOUD_COLOR**
    - and opacity?      **CLOUD_OPACITY**

- rings?
    - if so, size?      **RING_SIZE**
    - and what color?   **RING_COLOR**
    - and what angle?   **RING_ANGLE**
    - and what style?   **RING_STYLE**
        - bands: rings sit on top of each other, extending out from surface of planet
        - stacked: rings sit side-by side , same distance from surface of planet

# painting flow

1. according to pattern inputs, assign each surface point as primary or secondary, to create basis pattern (values can be over-written/reassigned by logic of later pattern inputs).
2. according to color palettes, assign each surface point a color.
3. paint on ice caps (overwrite existing colors)
4. paint on clouds (opacity, so need to add colors together somehow)
5. paint on rings (need separate prior logic to create ring points, as separate entity from surface points, or at least flagged as different type)
6. dithering: small variations in each color for organic look. RGB is 0-255, so can adjust values by random amount in +- 5 for example

# image creation flow

given painted planet from painting flow step:
1. take z-most point for each y-x value, and assign that color (RGBA) to the y-x coord in NumPy array. (if z-most point is some % opaque, also include points behind etc)
2. Pillow PIL to map numpy array to png
3. create gif from pngs sequenced (PIL can also make gifs)
4. make spritesheet from pngs combined