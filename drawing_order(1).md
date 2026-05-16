# Promptoid Drawing Order and Visibility Reference
# Based on testnewperform.html — May 15, 2026

---

## Global States

These variables control what is drawn each frame. Many interact with each other.

| State | Type | Values | Notes |
|-------|------|--------|-------|
| running | bool | true/false | false = quit screen, render loop stops |
| waitingForStart | bool | true/false | true = song not yet started or just reset |
| songPaused | bool | true/false | true = user paused, ball frozen |
| animationPaused | bool | true/false | true = Y key or Y1pause fired |
| overlayMode | string/null | null, 'lyrics', 'artwork', 'credits' | null = normal display |
| settingsOpen | bool | true/false | true = speed/delay panel visible |
| debugMode | bool | true/false | true = debug info box visible |
| isAudioActuallyPlaying() | bool | true/false | derived from audioElement state |
| currentSongKey | string | '' or song key | empty = no song selected |
| Assets loaded | per-asset | grey/orange/green/purple/black | affects status ball colors |

---

## State: running = false (Quit)

Triggered by Q or Escape key. render() returns immediately - nothing draws.
Canvas shows a static quit message drawn directly to ctx before render() exits:
- Dark grey background
- Green text: "To close the program you must close this tab or window"
- Green text: folder path (if running locally)

DOM elements (buttons, selector, emojis) remain visible but non-functional.

---

## State: overlayMode != null

When any overlay is active, render() draws ONLY the overlay and status balls, then returns.
The normal teleprompter display does NOT draw.
Music continues playing. Ball animation is frozen (physics not updated).
Mouse movement sets overlayMode = null, returning to normal display.

### overlayMode = 'lyrics'
- Dark semi-transparent background (rgba 0,0,0,0.88)
- Line 0: song title, bold green 32px, centered
- Line 1: byline, italic grey 22px, centered
- Empty lines: 16px gap
- All other lines: white 20px, centered
- Scrollable via Arrow Up/Down keys (overlayScrollY)
- "move mouse to dismiss" hint at bottom in dark grey
- Asset status balls drawn on top

### overlayMode = 'artwork'
- If songConfig.artwork exists: image drawn fullscreen
- If not: dark background + "No artwork available" in white
- Asset status balls drawn on top

### overlayMode = 'credits'
- Dark semi-transparent background (rgba 0,0,0,0.92)
- Lines from songConfig.credits split on \n
- Line 0: bold green 28px, centered
- All other lines: white 22px, centered
- Block vertically centered on screen
- "move mouse to dismiss" hint at bottom
- Asset status balls drawn on top

---

## State: settingsOpen = true

Does NOT block normal drawing. Settings overlay draws ON TOP of everything else
(Step 21 in normal render order), before status balls.
Shows: dark panel, speed value, delay value.
DOM speed and delay sliders also become visible.

---

## State: debugMode = true

Does NOT block normal drawing.
DOM #debugInfo box appears top-right (yellow border).
Shows: line number, bounce count, beat numbers, playback mode, speed, duration.
Record button outline changes from green to red.

---

## State: waitingForStart = true

Ball is held at BALL_HIGH_POSITION (y=230), not animating.
Position indicator on tape strip does NOT draw.
Line number on controls does NOT draw.
Chord and lyric lines DO draw if currentIndex > 0.
Chord and lyric lines do NOT draw if currentIndex = 0.
"Press Play or spacebar" message draws.

---

## State: waitingForStart = false, songPaused = false, animationPaused = false

Normal playing state. Ball physics run. Lines advance automatically.
All normal display elements draw (see render order below).

---

## State: songPaused = true

Ball physics frozen at current position (ballY does not update).
Audio paused. Play button shows "PLAY".
All visual elements still draw normally - lyrics, chords, controls, etc.

---

## State: animationPaused = true

Same visual effect as songPaused - ball frozen, no line advance.
Typically set by Y key or Y1pause appointment.
Audio may still be playing (animationPaused does not pause audio).

---

## State: currentSongKey = '' (no song selected)

Lyrics and chords arrays are empty - chord/lyric lines do not draw.
Title and time signature do not draw (songData empty).
"Press Play or spacebar" message draws.
Status balls all grey.

---

## State: isAudioActuallyPlaying() = true

Music emoji colored (visible).
Play/Pause buttons show "PAUSE".

## State: isAudioActuallyPlaying() = false

Music emoji filled black (invisible).
Play/Pause buttons show "PLAY" or original label.

---

## Normal Render Order (overlayMode = null, running = true)

Steps execute in this order every frame:

| Step | What | Condition | Position |
|------|------|-----------|----------|
| 1 | Fire appointments, sync audio UI | always | no drawing |
| 2 | Clear canvas (dark grey) | always | entire canvas |
| 3 | Background image | image loaded | entire canvas |
| 4 | Magnetic tape strip | image loaded | top 1/8 of canvas |
| 5 | Position indicator on tape | !waitingForStart AND lyrics loaded | small rect + circle on tape |
| 6 | Controls image (tape recorder) | image loaded | lower left |
| 7 | Button outlines | controls loaded | on top of controls |
| 8 | Line number on controls | !waitingForStart | upper left of controls |
| 9 | Song title | songData.title exists | y=120, left |
| 10 | Time signature | songData.timeSignature exists | y=150, left |
| 11 | "Press Play" message | waitingForStart | lower right area |
| 12 | Chord line (orange) | lyrics+chords loaded, playing or index>0 | y=210, left |
| 13 | Lyric line (white) | same as above | y=240, left (or y=240+285 if ##) |
| 14 | Syllable highlight (cyan) | beat data exists AND rising=true | over lyric line |
| 15 | Chord highlight (cyan) | same as above | over chord line |
| 16 | HL word highlight (cyan) | currentHLWord set, not highlighting | over lyric line |
| 17 | Section label (blue) | sections array non-empty | y=180, left |
| 18 | Ball physics update | !songPaused AND !animationPaused AND !waitingForStart | no drawing |
| 19 | Ball | always | center of canvas, ballY |
| 20 | Music emojis | always | right of controls, DOM element |
| 21 | Settings overlay | settingsOpen=true | center panel, canvas |
| 22 | Asset status balls | always | bottom of canvas, 4 balls |

---

## Known Issues

### 1. drawAssetStatusBallsOnCanvas - local ctx shadows global
The function declares const ctx = canvas.getContext('2d') which creates a
local variable shadowing the global ctx. The ctx.save() and ctx.restore()
operate on this local reference. While functionally equivalent in this case,
it is inconsistent with the rest of the code and could cause subtle bugs.
FIX: Remove const ctx = canvas.getContext('2d'), remove ctx.save() and
ctx.restore(), use global ctx throughout.

### 2. beatPositionsCache not reset on song change
In processSongData(), beatChordWordData is reset to {} but beatPositionsCache
is not. If songs share line indices, old beat positions from a previous song
may persist.
FIX: Add beatPositionsCache = {}; alongside beatChordWordData = {};
in processSongData().

### 3. Arrow key scrolling for lyrics overlay - not yet confirmed working
Arrow Up/Down increment/decrement overlayScrollY when overlayMode is set.
Keys are on document listener so focus should not be an issue.
Needs testing.

### 4. Artwork overlay - image loads asynchronously
On first W keypress, artworkImage is created and src is set.
If image has not completed loading by the time drawArtworkOverlay() runs,
nothing draws (naturalWidth check fails). Second keypress or next frame
should show the image once loaded.
