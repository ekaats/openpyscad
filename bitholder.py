import re
import openpyscad as ops

class BitsCube:

    def __init__(self, drill_holes, height, spacing, z_clearance=None, debug=False, text=None, top_connector=None, bottom_connector=None):

        self.drill_holes = drill_holes

        # Set the X and Y of the cube
        self.x = self._get_cube_x()
        self.y = self._get_cube_y()
        self.height = height

        # Set the type of connector on either side of the cube.
        # todo: only expect 0, 1 or None
        self.top_connector = top_connector
        self.bottom_connector = bottom_connector

        self.spacing = spacing
        self.text = text

        self.debug = debug

        if z_clearance is None:
            # Set z_clearance (the amount of material under the drill bit holes) to 5 by default
            self.z_clearance = 5
        else:
            self.z_clearance = z_clearance

    def getcube(self):

        maincube = ops.Cube([self.x, self.y, self.height])
        if self.debug is True:
            maincube.transparent()

        previous_x = 0


        for radius in self.drill_holes:
            x = previous_x + (radius * 2)
            y = radius + self.spacing
            z = self.z_clearance

            previous_x = x  # Add the new x to previous

            print(f"Adding a cylinder at {x}, {y}, {z}")
            cyl = ops.Cylinder(h=self.height - self.z_clearance, r=radius).translate([x, y, z])

            maincube = maincube - cyl

        # Add text, if available
        if self.text:
            maincube = maincube + self._add_text(maincube)


        if self.top_connector == 0:
            # needs to be taken out of the cube

            maincube = self._get_connector(
                maincube=maincube,
                position='top',
                type=0)

        elif self.top_connector == 1:
            print("Positive top connector is not supported")
            # # needs to be added next to the cube
            # maincube = self._get_connector(
            #     maincube=maincube,
            #     position='top',
            #     type=1)


        if self.bottom_connector == 0:
            print("Negative bottom connector is not supported")
            # # needs to be taken out of the cube
            #
            # maincube = self._get_connector(
            #     maincube=maincube,
            #     position='bottom',
            #     type=0)

        elif self.bottom_connector == 1:
            # needs to be added next to the cube
            maincube = self._get_connector(
                maincube=maincube,
                position='bottom',
                type=1)

        # todo: add connecting points
        return maincube

    @property
    def simple_name(self):
        """

        :return: text without special characters
        """
        return re.sub('\W+', '', self.text)

    def _get_cube_x(self):
        '''
        Given the drill holes, returns the X size of cube we need to create
        :param drill_holes:
        :return:
        '''
        max_x = 0
        for radius in self.drill_holes:
            max_x = max_x + (radius * 2)
        return max_x + (radius * 2)

    def _get_connector(self, maincube, position, type):
        '''
        Add a connector of the given type to the cube
        '''

        middle_of_cube = self.x / 2

        connector_length = 5
        connector_shape = ops.Cube([5, connector_length, self.height]) # Start out with a small cube

        slopped_part = ops.Cylinder(h=connector_length,r1=20, r2=20, _fn=3) # Add a slopped part
        slopped_part = slopped_part.rotate([0,90,270])
        slopped_part = slopped_part.translate([connector_length / 2,0, (self.height / 2)]) # todo: not sure if x is correct but it seems to work


        connector_shape = connector_shape + slopped_part # add connector and slope together

        connector_shape = connector_shape.rotate([180,0, 0]) # rotate the whole thing
        connector_shape = connector_shape.translate([0,connector_length, self.height])


        if type == 0:
            # todo: scale negative slightly bigger

            if position == 'top':
                connector_shape = connector_shape.rotate([0,0,180]) # rotate the shape around

                connector_shape = connector_shape.translate([middle_of_cube, self.y, 0])
                maincube = maincube - connector_shape

            # elif position == 'bottom':
            #     #todo: does not work with the current thickness of the lower part of the cube
            #     connector_shape = connector_shape.rotate([0,0,180])
            #     connector_shape = connector_shape.translate([middle_of_cube, -1, 0])
            #     maincube = maincube - connector_shape


        elif type == 1:

            # if position == 'top':
            #     connector_shape = connector_shape.translate([middle_of_cube, self.y, 0])
            #     maincube = maincube + connector_shape

            if position == 'bottom':
                connector_shape = connector_shape.rotate([0,0,180]) # Rotate the shape around

                # place the shape in the middle of the cube.
                # because it is rotated it also needs to be repositioned on the Z axis
                connector_shape = connector_shape.translate([middle_of_cube, 0, 0])
                maincube = maincube + connector_shape

        return maincube

    def _add_text(self, maincube):
        '''
        If text is given, add this to the cube.

        :return:
        '''
        text = ops.Text(f'"{self.text}"', font='"Noto Sans Display"')

        # Somehow need to 'overwrite' old objects. just calling text.operator() does not work
        text = text.rotate([0, 0, 8])
        text = text.linear_extrude(height=self.height / 2) # Make the text half the block in depth

        # Needs to be placed above the holes. Second is used as guide
        y_of_text = (self.drill_holes[1] * 2) + self.spacing

        # put the text Y relative to hole, Z depending on height
        text = text.translate([10, y_of_text, self.height / 2])

        return maincube - text

    def _get_cube_y(self):
        '''
        Given the drill holes, returns the Y size of cube we need to create
        :param drill_holes:
        :return:
        '''
        max_y = 0
        for radius in self.drill_holes:
            max_y = radius + radius
        return max_y + radius


def build_cubes():

    '''
    Create several different drillbit modules, based on parameters

    '''

    cubes = [
        BitsCube(
            drill_holes=[4,5,6,7,8,9,10,12,14,16,18],
            spacing=5,
            text="Treecarcasses",
            height=50,
            top_connector=0,
            bottom_connector=1
        ),
        BitsCube(
            drill_holes=[6,8,10,12,14,16,18],
            spacing=5,
            height=40,
            text="speedTree",
            bottom_connector=1
        ),
        BitsCube(
            drill_holes=[4, 5, 6, 7, 8, 9, 10, 12, 14],
            spacing=5,
            text="Stein",
            height=30,
            top_connector = 0,
            bottom_connector = 1,
            debug=False
        ),
    ]
    return cubes



if __name__ == '__main__':

    # Build a drillbit holder, based on the given parameters
    for cube in build_cubes():

        (cube.getcube()).write(f"{cube.simple_name}.scad")

