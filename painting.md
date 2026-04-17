
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
    - primary color 1:  **PRIMARY_COLOR_1** (RGB)
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
    - and what angle?   **RING_ANGLE

# painting flow

1. according to pattern inputs, assign each surface point as primary or secondary, to create basis pattern (values can be over-written/reassigned by logic of later pattern inputs).
2. according to color palettes, assign each surface point a color.
3. paint on ice caps (overwrite existing colors)
4. paint on clouds (opacity, so need to add colors together somehow)
5. paint on rings (need separate prior logic to create ring points, as separate entity from surface points, or at least flagged as different type)
6. dithering: small variations in each color for organic look
