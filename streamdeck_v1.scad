include <arduino.scad>

unoDimensions = boardDimensions( UNO );

// Upper PCB:
// hole-to-hole X: 65mm
// hole-to-hole Y: 45mm



//Board mockups
// arduino();

// Overwrite the enclosureLid to add a window for the keys to be put into.
module enclosureLid( boardType = UNO, wall = 3, offset = 3, cornerRadius = 3, ventHoles = false) {
	dimensions = boardDimensions(boardType);
	boardDim = boardDimensions(boardType);
	pcbDim = pcbDimensions(boardType);

	enclosureWidth = pcbDim[0] + (wall + offset) * 2;
	enclosureDepth = pcbDim[1] + (wall + offset) * 2;

	difference() {
		union() {
			boundingBox(boardType = boardType, height = wall, offset = wall + offset, include=PCB, cornerRadius = wall);

			translate([0, 0, -wall * 0.5])
				boundingBox(boardType = boardType, height = wall * 0.5, offset = offset - 0.5, include=PCB, cornerRadius = wall);
		
			//Lid clips
			translate([0, enclosureDepth * 0.75 - (offset + wall), 0]) {
				translate([-offset, 0, 0])
					rotate([0, 180, 90]) clip(clipHeight = 10);
				translate([offset + boardDim[0], 0, 0])
					rotate([0, 180, 270]) clip(clipHeight = 10);
			}
		
			translate([0, enclosureDepth * 0.25 - (offset + wall), 0]) {
				translate([-offset, 0, 0])
					rotate([0, 180, 90]) clip(clipHeight = 10);
				translate([offset + dimensions[0], 0, 0])
					rotate([0, 180, 270]) clip(clipHeight = 10);
			}
            
		}
       
            // Add the mounting holes and window
            translate([5,0,-2]) // moves all four mounting holes + window together
                union() {
                REL_X = 4;
                REL_Y = 1;
                    
                    
                translate([REL_X, REL_Y,0])    
                    cylinder(d=2, h=wall + 5, $fn=32);
                    
                translate([REL_X,REL_Y +  66,0])
                    cylinder(d=2, h=wall + 5, $fn=32);
                    
                translate([REL_X + 46,REL_Y + 66,0])
                    cylinder(d=2, h=wall + 5, $fn=32);
                    
                translate([REL_X + 46,REL_Y + 0,0])
                    cylinder(d=2, h=wall + 5, $fn=32);
                    
                // Create the window
                
                boundingBox(boardType = boardType, height = wall + 4, offset = wall -9, include=PCB, cornerRadius = wall);
                }
	}
}

//
//translate([0, 0, 0]) {
//	enclosure();
//}

rotate([180,180,0])
translate([75, -75, 0]) {
	enclosureLid(wall=2);
}
