from math import pi, sin, cos

RADIUS = 5.0
CENTER_VECT = {
    "y": 0.0,
    "x": 0.0,
    "z": 0.0
}


def planet_maker():
    surface_points = [
        {"name": str(RADIUS)+"_"+str(0.0)+"_"+str(0.0), 
         "y": RADIUS, "x": 0.0, "z": 0.0,
         "neighbors": []}
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
                                   "neighbors": []})
            current_h_layer_angle += h_layer_step_distance

    # for surface_point in surface_points:
    #     print(surface_point)
    print(len(surface_points))

    
    # 2. Identify neighbouring points
    for u in surface_points:
        for v in surface_points:
            if u["name"] != v["name"]:
                distance = ((u["y"] - v["y"])**2 + (u["x"] - v["x"])**2 + (u["z"] - v["z"])**2)**0.5
                if distance <= 1.45:
                    u["neighbors"].append(v["name"])
    
    for surface_point in surface_points:
        print(surface_point)
    


if __name__ == "__main__":
    planet_maker()