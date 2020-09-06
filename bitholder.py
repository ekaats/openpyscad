
import openpyscad as ops


def get_cube_x(drill_holes):
    '''
    Given the drill holes, returns the X size of cube we need to create
    :param drill_holes:
    :return:
    '''
    max_x = 0
    for radius in drill_holes:
        max_x = max_x + (radius * 2)
    return max_x + (radius * 2)

def get_cube_y(drill_holes):
    '''
    Given the drill holes, returns the Y size of cube we need to create
    :param drill_holes:
    :return:
    '''
    max_y = 0
    for radius in drill_holes:
        max_y = radius + radius
    return max_y + radius


def build_maincube(drill_holes, spacing):

    maincube = ops.Cube([
        get_cube_x(drill_holes=drill_holes),
        get_cube_y(drill_holes=drill_holes), 50])

    # Add holes
    # for radius in range(4, 16):
    previous_x = 0


    for radius in drill_holes:
        x = previous_x + (radius * 2)
        y = radius + spacing
        z = 5

        previous_x = x # Add the Old One, please

        print(f"Adding a cylinder at {x}, {y}, {z}")
        cyl = ops.Cylinder(h=46, r=radius).translate([x, y, z])

        maincube = maincube - cyl

    # Add text
    text = ops.Text('"TreeCarcass"', font='"Noto Sans Display"')

    # Somehow need to 'overwrite' old objects. just calling text.operator() does not work
    text = text.rotate([0,0,8])
    text = text.linear_extrude(height=12)
    text = text.translate([10,15,40])

    maincube = maincube - text

    return maincube

if __name__ == '__main__':

    # Build a drillbit holder, based on the given parameters
    (build_maincube(
        drill_holes=[4,5,6,7,8,9,10,12,14,16,18,20],
        spacing=4
    )).write("sample.scad")

