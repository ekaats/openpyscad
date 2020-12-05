WALL_THICKNESS = 2;
MIDDLE_Z_LENGTH = 20;


// Vacuum side
ID_VAC=43;
VACUUM_Z_MAX=30;

difference() {
translate([0,0,0]) {
    linear_extrude(height=VACUUM_Z_MAX) {
        difference() {
            circle(d=ID_VAC + WALL_THICKNESS);
            circle(d=ID_VAC);
        }
    }
}
// plug thingies
translate([-ID_SANDER,-4,9.5])
                   cube([55,8,8]);
}


// Sander side
ID_SANDER = 27;
UD_SANDER = ID_SANDER + WALL_THICKNESS;
SANDER_Z_MAX = 30;
   
translate([0,0,MIDDLE_Z_LENGTH + VACUUM_Z_MAX]) 
    linear_extrude(height=SANDER_Z_MAX){
    difference() {
        circle(d=UD_SANDER);      
        circle(d=ID_SANDER);
        }
    }          
    

// middle part
translate([0,0,VACUUM_Z_MAX])
linear_extrude(height=MIDDLE_Z_LENGTH, scale = ID_SANDER / ID_VAC) {
    difference() {
            circle(d=ID_VAC + WALL_THICKNESS);
            circle(d=ID_VAC);
        }

}