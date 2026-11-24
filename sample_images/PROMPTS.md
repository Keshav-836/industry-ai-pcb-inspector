# How I made the practice images

The task didn't come with any data, and I couldn't find a public dataset with
the same board photographed again and again with parts removed. So I made my
own practice images with ChatGPT.

AI was only used to make these images. Nothing inside the app calls any AI.

I drafted the prompts with Claude and then tweaked them while generating.

## The rule I followed

Generate the reference board only once. For every test image, upload that same
reference to ChatGPT and ask it to edit it. If you write a fresh prompt each
time, you get a different board and the comparison is useless.

I also checked every result against the reference before keeping it (side by
side, and with a small OpenCV diff script) because ChatGPT sometimes changed
more than I asked for.

---

## Board 1 (simple board)

### Reference

```
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
```

### Removing a part (I changed only the bit in brackets)

```
Edit this exact image. Remove only the [blue capacitor in the top right], so that
spot shows the bare green board with its empty solder pads. Do not change
anything else: same camera angle, same zoom, same framing, same lighting, same
colors, and every other component stays in exactly the same position and size.
Keep the same image resolution.
```

### Complete board, different lighting

```
Edit this exact image. Do not add or remove any component. Only make the overall
lighting about 10 percent [brighter / warmer]. Everything else must stay
exactly the same: framing, zoom, angle, and every component's position.
```

### What I got

| File | What I asked for | What is actually missing |
|---|---|---|
| test_01_ok.png | brighter lighting | nothing |
| test_02_ok.png | warmer lighting | nothing |
| test_03_missing_chip.png | remove the center chip | Main chip |
| test_04_missing_cap.png | remove one blue capacitor | Capacitor top-left |
| test_05_missing_led.png | remove the red LED | LED |
| test_06_missing_2.png | remove the connector and one resistor | Connector, Resistor bottom-left |
| test_07_missing_3.png | remove the crystal, the button and one small IC | IC bottom-left, Crystal, Push button |
| test_08_missing_cap_right.png | remove the top-right capacitor (my first try) | Capacitor top-right |

Things that happened:
- test_07: I asked for "one small IC" and it removed the bottom-left one. Fine,
  I just wrote down the real answer.
- test_05 came out shifted by about 7 px compared to the reference. I kept it on
  purpose because it's a good test for the alignment step.
- Three images came back 1 px smaller than the reference. The app resizes, so
  that's fine too.

---

## Board 2 (dense board)

I wanted to see if the app works on a much busier board with small parts,
without changing any setting.

### Reference

```
A realistic top-down photo of a dense, crowded printed circuit board, taken
straight from above by a fixed industrial inspection camera. Flat, even, bright
lighting. Plain dark grey background, the full board visible with some margin.
No perspective tilt, no shadows, no hands, no text labels, sharp focus.

Dark green board packed with many components close together:
- one large black square processor chip in the center
- four smaller black ICs of different sizes around it
- about twenty tiny surface-mount resistors and capacitors (small black and
  brown rectangles) spread across the board
- four blue electrolytic capacitors of different sizes
- one USB connector on the right edge
- one black 6-pin header on the left edge
- three small surface-mount LEDs (red, green, yellow) in a row
- one silver crystal
- one small black push button
- one black 3-pin voltage regulator

Components are close together but do not overlap. 4:3 aspect ratio.
```

Edits used the same "remove only [...]" prompt as board 1.

### What I got

| File | What is missing |
|---|---|
| test_01_missing_led.png | Green LED |
| test_02_missing_small.png | Beige capacitor (right of the yellow LED) |
| test_03_missing_2.png | USB connector, Voltage regulator |

Things that happened:
- My first try at test_02 removed the green LED again instead of the small
  capacitor. My diff script caught it. I rewrote the prompt to describe the
  exact spot ("the beige capacitor to the right of the yellow LED, keep all
  three LEDs") and the second try worked.
- ChatGPT also redrew the tiny printed text on a lot of small parts (like "200"
  turning into "D02"). I left it, since it's a nice check that the app doesn't
  raise false alarms over small noise like that.

---

## Results

With the same settings for both boards, the app got all of them right:
board 1 was 8 out of 8, and board 2 was 3 out of 3.