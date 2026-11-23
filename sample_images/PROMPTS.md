Prompt 1: Reference image (good board)

Use this in ChatGPT or Gemini to create the image:

A realistic top-down photo of a green printed circuit board, taken straight from
above by a fixed industrial inspection camera. Flat, even, bright lighting. Plain
dark grey background, the full board visible with some margin around it. No
perspective tilt, no shadows, no hands, no text labels, sharp focus.

The board has a small number of large, clearly separated components:
- one large black square microcontroller chip in the center
- two smaller black rectangular ICs
- three blue cylindrical electrolytic capacitors
- four small beige resistors
- one white 4-pin connector on the left edge
- one red LED
- one silver oval crystal oscillator
- one black square push button

Components are spaced apart and do not overlap. 4:3 aspect ratio.

Save the result as reference.png.




Prompt 2: Edit template (missing part)

Upload reference.png with this prompt, and change only the part inside [ ]:

Edit this exact image. Remove only the [blue capacitor in the top right], so that
spot shows the bare green board with its empty solder pads. Do not change
anything else: same camera angle, same zoom, same framing, same lighting, same
colors, and every other component stays in exactly the same position and size.
Keep the same image resolution.




Prompt 3: Edit template (complete board, different condition)
Edit this exact image. Do not add or remove any component. Only make the overall
lighting about 10 percent [brighter / warmer]. Everything else must stay
exactly the same: framing, zoom, angle, and every component's position.
Make these 7 test images
File name	What to do
test_01_ok.png	Prompt 3, brighter
test_02_ok.png	Prompt 3, warmer
test_03_missing_chip.png	Prompt 2: remove the large center chip
test_04_missing_cap.png	Prompt 2: remove one blue capacitor
test_05_missing_led.png	Prompt 2: remove the red LED
test_06_missing_2.png	Prompt 2: remove the white connector and one resistor
test_07_missing_3.png	Prompt 2: remove the crystal, the push button and one small IC