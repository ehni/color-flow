# color-flow
Visualize the colors of a movie clip with a single picture

# Options
Tool for creating a color palette picture from a .mp4 video

positional arguments:

      pathIn                path to video
  
      pathOut               path to save the image

optional arguments:

      -h, --help            show this help message and exit
  
      --maxWidth MAXWIDTH   maximum width of the output image, default=2000

      --maxHeight MAXHEIGHT maximum height of the output image, default=4000

      --takeFrames TAKEFRAMES
                        Use every frame (True) or just take a frame every
                        second (False, Default)

# Example

* Video: http://download.blender.org/peach/bigbuckbunny_movies/BigBuckBunny_320x180.mp4

      #> python color-flow BugBuckBunny_320x180.mp4 .
      == Starting Color-Flow ==
      ==> Reading arguments
      ==> Reading video from BigBuckBunny_320x180.mp4
      Frames: 14315
      FPS: 24
      ==> Setting output picture dimension to 397 x 596
      ==> Reading 596 frames
      Progress: |XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX| 100.0% Complete
      ==> 596 frames read in 3.04 seconds
      ==> Generating new image
      Progress: |XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX| 100.0% Complete
      ==> Picture generated in  0.17 seconds
      ==> Saving new picture to .
      ==> Done!

    
* Output:
