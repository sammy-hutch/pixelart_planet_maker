from math import pi, sin, cos

RADIUS = 5.0
CENTER_VECT = {
    "y": 0.0,
    "x": 0.0,
    "z": 0.0
}
INIT_ANGLE = pi/2.0
FINAL_ANGLE = -pi/2.0


def plotter():
    current_v_angle = INIT_ANGLE
    v_step_distance = 1.0 / RADIUS
    surface_points = [
        {"name": str(RADIUS)+"_"+str(0.0)+"_"+str(0.0), "y": RADIUS, "x": 0.0, "z": 0.0}
    ]

    while current_v_angle > FINAL_ANGLE:
        current_v_angle -= v_step_distance
        y_value = round(RADIUS * sin(current_v_angle), 2)

        current_h_layer_angle = 0
        max_h_layer_angle = 2 * pi
        h_layer_radius = (RADIUS**2 - y_value**2)**0.5
        h_layer_step_distance = 1.0 / h_layer_radius if h_layer_radius != 0 else 2 * pi

        while current_h_layer_angle < max_h_layer_angle:
            x_value = round(h_layer_radius * sin(current_h_layer_angle), 2)
            z_value = round(h_layer_radius * cos(current_h_layer_angle), 2)
            surface_points.append({"name": str(y_value)+"_"+str(x_value)+"_"+str(z_value), 
                                   "y": y_value, "x": x_value, "z": z_value})
            current_h_layer_angle += h_layer_step_distance

    # for surface_point in surface_points:
    #     print(surface_point)

    return surface_points
    


if __name__ == "__main__":
    plotter()