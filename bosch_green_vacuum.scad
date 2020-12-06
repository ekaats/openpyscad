WALL_THICKNESS = 3;
MIDDLE_Z_LENGTH = 20;


// Vacuum side
ID_VAC=44;
UD_VAC=ID_VAC + WALL_THICKNESS;
VACUUM_Z_MAX=30;

difference() {
translate([0,0,0]) {
    linear_extrude(height=VACUUM_Z_MAX) {
        difference() {
            circle(d=UD_VAC, $fn=100);
            circle(d=ID_VAC, $fn=100);
        }
    }
}
// plug thingies
translate([-ID_SANDER, -4, 10])
                   cube([55,9,9]);
}


// Sander side
//ID_SANDER = 28; //Sander
ID_SANDER = 38;

UD_SANDER = ID_SANDER + WALL_THICKNESS;
SANDER_Z_MAX = 30;
   
translate([0,0,MIDDLE_Z_LENGTH + VACUUM_Z_MAX]) 
    linear_extrude(height=SANDER_Z_MAX){
    difference() {
        circle(d=UD_SANDER, $fn=100);      
        circle(d=ID_SANDER, $fn=100);
        }
    }          
    

// middle part
SLOPE_SCALE=UD_SANDER/UD_VAC;
translate([0,0,VACUUM_Z_MAX])
linear_extrude(height=MIDDLE_Z_LENGTH, scale = SLOPE_SCALE) {
    difference() {
            circle(d=UD_VAC, $fn=100);
            circle(d=ID_VAC, $fn=100);
        }

}