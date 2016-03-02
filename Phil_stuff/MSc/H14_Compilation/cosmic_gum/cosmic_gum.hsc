#THIS SCRIPT GENERATES COSMIC GUM

	#switch to OBJ Level
	opcf /obj
	#remove any previous versions of the cosmic_gum
	oprm -f cosmic_gum

	#add the cosmic_gum geometry object
	opadd geo cosmic_gum
	#go into the cosmic_gum object
	opcf cosmic_gum
	#remove the default file sop
	oprm file1
	#add a sphere sop
	opadd sphere my_sphere
	#set its parameters
	opparm my_sphere type (poly) freq (10)

	#add a Mountain SOP
	opadd mountain my_mountain

	#activate its channels and values
	chblockbegin
		chadd my_mountain offset3
		chkey -f 1 -F '$T' my_mountain/offset3
	chblockend

	#set its parameters
	opparm my_mountain offset (0 0 offset3) frac_depth (1)

	#wire the Sphere and Mountain SOPs together
	opwire my_sphere -0 my_mountain

	#activate the Display and Render Flags on the Mountain SOP
	opset -d on -r on my_mountain

	#layout the created nodes
	oplayout -d 0
