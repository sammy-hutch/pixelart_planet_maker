from math import pi, sin, cos, radians, degrees
from PIL import Image
import random

### VARS

RADIUS = 16.0
CENTER_VECT = {
    "y": 0.0,
    "x": 0.0,
    "z": 0.0
}

FRAMES = 144

## Painting style parameters

# Landmass style parameters
LANDMASSES = True
LAND_PCT = 0.3

# Cracked style parameters
CRACKED = True
LAND_SIZE = 3

# Scattered style parameters
SCATTERED = True
PRIMARY_PCT = 0.5

# Band style parameters
BANDS = True
BAND_WIDTH = 3

# River style parameters
RIVERS = True
RIVER_PCT = 0.2

# Ice cap style parameters
ICE_PCT = 0.1
ICE_COLOR = (255, 255, 255, 255)  # White

# Cloud style parameters
CLOUD_PCT = 0.3
CLOUD_STYLE = "fluffy"  # Options: "fluffy", "wispy"
CLOUD_COLOR = (255, 255, 255, 204)  # Semi-transparent white

# Ring style parameters
RING_RADIUS_MIN = 5.0
RING_RADIUS_MAX = 5.0
RING_COLOR = (200, 200, 200, 124)  # Semi-transparent gray
RING_ANGLE = 45.0
RING_STYLE = "bands" # Options: "bands", "stacked"

# Coloring style parameters
PRIMARY_COLOR_1 = (0, 255, 0, 255)  # Green
PRIMARY_COLOR_2 = (255, 255, 0, 255)  # Yellow
PRIMARY_COLOR_3 = (255, 0, 0, 255)  # Red

SECONDARY_COLOR_1 = (0, 0, 255, 255)  # Blue
SECONDARY_COLOR_2 = (255, 0, 255, 255)  # Magenta
SECONDARY_COLOR_3 = (0, 255, 255, 255)  # Cyan





def planet_maker():
    surface_points = [
        {"name": str(RADIUS)+"_"+str(0.0)+"_"+str(0.0), 
         "y": RADIUS, "x": 0.0, "z": 0.0,
         "h_angle": 0.0,
         "h_layer_radius": 0.0,
         "neighbors": [],
         "point_type": "surface",
         "land_type": "None",
         "color": (0, 0, 0, 1)}
    ]

    # 1. Plot the points on the surface of the sphere
    init_v_angle = pi/2.0   # start from the top of the sphere
    final_v_angle = -pi/2.0  # end at the bottom of the sphere, don't need to go further as horizontal layers cover full 360 degrees

    current_v_angle = init_v_angle
    v_step_distance = 1.0 / RADIUS

    # iterate over vertical steps to create horizontal layers
    while current_v_angle > final_v_angle:
        current_v_angle -= v_step_distance
        y_value = round(RADIUS * sin(current_v_angle), 2)

        current_h_layer_angle = 0
        max_h_layer_angle = 2 * pi
        h_layer_radius = (RADIUS**2 - y_value**2)**0.5
        h_layer_step_distance = 1.0 / h_layer_radius if h_layer_radius != 0 else 2 * pi

        # iterate over horizontal steps to plot points on the current horizontal layer
        while current_h_layer_angle < max_h_layer_angle:
            x_value = round(h_layer_radius * sin(current_h_layer_angle), 2)
            z_value = round(h_layer_radius * cos(current_h_layer_angle), 2)
            surface_points.append({"name": str(y_value)+"_"+str(x_value)+"_"+str(z_value), 
                                   "y": y_value, "x": x_value, "z": z_value,
                                   "h_angle": round(current_h_layer_angle, 3),
                                   "h_layer_radius": round(h_layer_radius, 2),
                                   "neighbors": [],
                                   "point_type": "surface",
                                   "land_type": "None",
                                   "color": (0, 0, 0, 1)})
            current_h_layer_angle += h_layer_step_distance

    
    # 2. Identify neighbouring points
    for u in surface_points:
        for v in surface_points:
            if u["name"] != v["name"]:
                distance = ((u["y"] - v["y"])**2 + (u["x"] - v["x"])**2 + (u["z"] - v["z"])**2)**0.5
                if distance <= 1.45:
                    u["neighbors"].append(v["name"])
    
    
    # 3. Pattern planet (assign each point to primary or secondary color group)
    points_to_pattern = len(surface_points)
    points_to_check = surface_points.copy()

    while points_to_pattern > 0:
        point = random.choice(points_to_check)
        point_index = surface_points.index(point)
        primary_chance = 0.5

        # Landmass logic: similarity to direct neighbours
        if LANDMASSES:
            primary_chance = LAND_PCT

            # calculate modifiers: the more neighbors that are similar, 
            # the more likely that way, but always non zero chance to go the opposite way
            positive_modifier = (1 - primary_chance) / (len(point["neighbors"]) + 1) * 1.0
            negative_modifier = primary_chance / (len(point["neighbors"]) + 1) * 1.0
            for neighbor in surface_points[point_index]["neighbors"]:
                neighbor_index = next(i for i, p in enumerate(surface_points) if p["name"] == neighbor)
                if surface_points[neighbor_index]["land_type"] == "primary":
                    primary_chance += positive_modifier
                elif surface_points[neighbor_index]["land_type"] == "secondary":
                    primary_chance -= negative_modifier

        if primary_chance > random.random():
            point["land_type"] = "primary"
        else:
            point["land_type"] = "secondary"
        
        points_to_pattern -= 1
        points_to_check.remove(point)


    # 4. Paint planet
    for point in surface_points:
        if point["land_type"] == "primary":
            point["color"] = PRIMARY_COLOR_1
        else:
            point["color"] = SECONDARY_COLOR_1
    

    # 5. Map planet to image, gif and spritesheet
    
    # Identify limits of image size
    y_mod = max(RADIUS, RING_RADIUS_MAX * sin(radians(RING_ANGLE)))
    x_mod = max(RADIUS, RING_RADIUS_MAX * cos(radians(RING_ANGLE)))
    y_size = int(2 * y_mod) + 1
    x_size = int(2 * x_mod) + 1

    rotate_step = (2.0 * pi) / FRAMES
    rotation = 0.0
    img_counter = 1
    images = []

    while rotation < 2.0 * pi:
        # create "empty" image depth map template
        image_depth_map = [[{"color": (255, 255, 255, 0), "z": float(x_mod + 1)} for _ in range(x_size)] for _ in range(y_size)]

        # Map z-least points to y-x pixel coords
        for point in surface_points:
            y_pixel = int(round(point["y"]) + y_mod)
            x_pixel = int(round(point["x"]) + x_mod)

            if point["z"] < image_depth_map[y_pixel][x_pixel]["z"]:
                image_depth_map[y_pixel][x_pixel]["color"] = point["color"]
                image_depth_map[y_pixel][x_pixel]["z"] = point["z"]
        
        # Paint the image
        img_name = "planet_" + str(img_counter) + ".png"
        image_array = [[image_depth_map[y][x]["color"] for x in range(x_size)] for y in range(y_size)]
        img = Image.new('RGBA', (x_size, y_size))
        img.putdata([pixel for row in image_array for pixel in row])
        img.save(f"images/{img_name}")
        images.append(img)

        # Rotate points for next frame
        for point in surface_points:
            new_angle = (point["h_angle"] + rotate_step) % (2.0 * pi)
            point["x"] = round(point["h_layer_radius"] * sin(new_angle), 2)
            point["z"] = round(point["h_layer_radius"] * cos(new_angle), 2)
            point["h_angle"] = round(new_angle, 3)
        
        img_counter += 1
        rotation += rotate_step
    
    images[0].save('images/planet.gif', save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)


if __name__ == "__main__":
    planet_maker()