
# Calculating Coordinates on surface of sphere

## Vector positions relative to radius
For any given y (height), x (width) and z (depth), the radius must always be fixed.
From pythagorean theorem, the radius is the hypotenuse, and when working in 3 dimensions this gives 
r = (y^2 + x^2 + z^2)^0.5

so: 
**fixed relationship between radius and 3D vector position**

Thus, on any vertical layer of the sphere, where we know y will always be fixed:
x^2 + z^2 = r^2 - y^2
e.g. assuming a radius of 5 and y-value of 3:
x^2 + z^2 = 25 - 9
x^2 + z^2 = 16
So, for the layer of the sphere where y = 3, x^2 + z^2 = 16 for all possible permutations of x and z

## Traveling along the surface of the sphere
At its most stretched perspective, pixels on the surface of the sphere are 1-unit distance apart. Thus, distance traveled between calculated points on surface of sphere should be 1 unit on the circumference.

circumference (c) = 2 * pi * r
Thus, for a known radius, we can divide the full rotation of the circle by the circumference to get the degrees (or radians) of how far to travel in one step.

E.g. for a sphere of radius 5, 1 full revolution (in degrees) can be divided into 360 / (2 * pi * 5) per step, or ~11.5 degrees per step.
For radians the calculation is simpler: (2 * pi) / (2 * pi * 5) steps, or 1/5 radians per step

**step_distance (degrees) = 180 / (pi * radius)**
**step_distance (radians) = 1 / radius**

As we are traveling along the surface of the sphere in steps of unit 1, the number of steps is thus the circumference, 2 * pi * radius.

### Vertical Travel
For vertical, we only need to count half these (the "front", we don't need to count the same layers for the "back"). thus, we divide circumference by 2:
**number of vertical layers = pi * radius**

So, iterating over values of y to find each vertical layer of the sphere, starting from a max y, we create an angle between previous y and current y of 1/radius radians

we know the angle and the hypotenuse of the right-angled triangle, and we need to find the length of the opposite side.
sin(angle) = opposite/hypotenuse, thus opposite (y-value) = sin(angle) * radius

so, we can calculate y-value of each layer of the sphere with :
**y-value of vertical layer = sin(current_angle) * radius**

where current angle is calculated as previous_angle + step_distance

### Horizontal Travel
For each vertical layer, we can calculate the radius of that layer (r_layer) using
**r_layer = (r^2 - y^2)^0.5**

Then, given that radius, we can calculate step distance same as before.


# Plotting Rings

## distance from center
Points on a ring are always ring_radius distance away from center, same as points on surface of sphere. thus, for given ring_radius,
**ring_radius = (y^2 + x^2 + z^2)^0.5**

however, unlike sphere, rings only lie on one plane. the plane can be set by an angle: 0 degree ring lies flat, 90 degree ring sits vertically, 45 degree ring is halfway inbetween.

## y/x constant
For any angle, the relationship between y and x is constant, i.e. when viewed directly from the z-side, ring looks like a straight line (when viewed from x or y side, ring looks like an elipsis).

Using trigonometry, we can find the relationship. given ring_angle and ring_radius:

y = sin(ring_angle) * ring_radius
x = cos(ring_angle) * ring_radius

thus relationship constant between y and x is 
**yx_const = sin(ring_angle)/cos(ring_angle)**

in cases where angle is 0 or 90 degrees, instead of calculating this and getting mathematical error, we can either nudge the numbers slightly (0 -> 0.001 or similar) or accept a fixed value of 0 for y (when angle is 90) or a fixed value of 0 for x (when angle is 0)

This means that for any given point on the ring:
**x_value = y * yx_const**

and z_value is
**(ring_radius^2 - y^2 - (y * yx_const)^2) ^ 0.5**

# iterating steps on rings
step_distance and step_angle for iterating over the ring are calculated the same as for surface:
number of total steps = 2 * pi * r. we only need to calculate for 1 quarter (and then mirror the points), thus steps = pi * r / 2.

we start the iteration at max y, max x, min z.
then, for each step, we increase z by sin(step_angle) * radius:
**z += sin(step_angle) * radius**

and we can calculate y and x from the z and radius, given y and x are constant
