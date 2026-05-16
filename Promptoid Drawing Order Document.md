# Promptoid Drawing Order and Visibility Reference
# Based on testnewperform.html — May 15, 2026

## render() — called every frame via requestAnimationFrame

### Step 1 — Automation (no drawing)
- Fire any pending APPOINTMENTS (jump, Y1pause, Y2resume)
- Fire any pending HL_APPOINTMENTS (word highlight cues)
- Sync audio UI state (play/pause button labels, emoji fill)

### Step 2 — Clear canvas
- Fill entire canvas with dark grey (#1e1e1e)
- This erases everything from the previous frame

### Step 3 — Overlay check (early return)
If overlayMode is set, draw overlay and return immediately.
Nothing else draws when an overlay is active.

| overlayMode | What draws | Notes |
|-------------|-----------|-------|
| 'lyrics'    | drawLyricsOverlay() + status balls | Music keeps playing |
| 'artwork'   | drawArtworkOverlay() + status balls | Music keeps playing |
| 'credits'   | drawCreditsOverlay() + status balls | Music keeps playing |

After drawing overlay + status balls, requestAnimationFrame(render) and return.
The normal render steps below DO NOT execute.

### Step 4 — Background image
- Drawn if backgroundImage is loaded and complete
- Fills entire canvas (covers the grey from Step 2)
- Song-specific: uses songFileMap[currentSongKey].background

### Step 5 — Magnetic tape strip
- Drawn at top of canvas, height = canvas.height / 8
- Drawn if magTapeImage is loaded and complete
- Covers top portion of background image

### Step 6 — Position indicator (on tape strip)
- Only drawn if NOT waitingForStart AND lyrics.length > 0
- Green rectangle + white circle showing current position
- Drawn on top of tape strip

### Step 7 — Controls image (tape recorder)
- Drawn at lower left: x=20, y=canvas.height - controlsHeight - 20
- Height = canvas.height / 3 + 72
- Drawn if controlsImage is loaded and complete

### Step 8 — Button outlines
- Drawn on top of controls image
- Colored polygons outlining each button region:
  - playback_mode: green/yellow/red depending on mode
  - forward (Play): green
  - pause: yellow
  - stop_eject: red
  - fast_forward, fast_rewind: blue
  - record: green (normal) or red (debug mode)

### Step 9 — Line number on controls
- Only drawn if NOT waitingForStart
- 3-digit line number in green, positioned at upper left of controls image

### Step 10 — Title and time signature
- Song title at y=120, green, left-aligned at x=5
- Time signature at y=150, green, left-aligned at x=5
- Always drawn if songData.title / songData.timeSignature exist

### Step 11 — "Press Play" message
- Drawn only if waitingForStart is true
- White text at canvas.width-1000, canvas.height-500
- Says "Press Play or spacebar" (index 0) or "Play or spacebar" (index > 0)

### Step 12 — Chord line
- Orange (#ff8800) at y=210, left-aligned at x=5
- Only drawn if lyrics and chords are loaded AND (playing OR currentIndex > 0)
- Section markers [..] stripped from display

### Step 13 — Lyric line
- White at y=240, left-aligned at x=5
- Supports ## split: splits into two lines at y=240 and y=285
- Only drawn under same conditions as chord line

### Step 14 — Syllable/chord highlighting (cyan)
- Only drawn if: currentIndex has beat data AND ball is rising (rising=true)
- Highlights current syllable in cyan at beat position
- Clears background rect before drawing highlight
- Highlights corresponding chord in cyan

### Step 15 — HL word highlighting
- Only drawn if currentHLWord is set and found in lyric text
- Cyan highlight on a specific word (from HL appointments file)
- Only active when highlightingActive is false (non-beat lines)

### Step 16 — Section label
- Blue (#0000ff) at y=180, left-aligned at x=5
- Only drawn if sections array is non-empty

### Step 17 — Debug info (DOM overlay, not canvas)
- Yellow bordered box at top-right of screen
- Only shown if debugMode is true
- Shows: line number, bounce count, beat numbers, playback mode, speed, duration

### Step 18 — Ball physics update (no drawing)
- Updates ballY based on gravity, dt, bounceDuration
- Advances currentIndex when bounceCount >= BOUNCES_PER_LINE
- Only runs if NOT songPaused AND NOT animationPaused AND NOT waitingForStart

### Step 19 — Ball
- Orange (#ee7621) normally
- Green (#00ff00) when highlighting is active (shouldHighlightBall)
- Drawn at ballCenterX (canvas center), ballY
- Radius = 25px
- Always drawn

### Step 20 — Music emojis
- 🎶🎸 positioned to right of controls image
- Filled (invisible) when audio paused, colored when playing
- DOM element (not canvas), updated each frame

### Step 21 — Settings overlay (canvas)
- Only drawn if settingsOpen is true (Ctrl+S)
- Dark semi-transparent panel in center of canvas
- Shows speed and delay values

### Step 22 — Asset status balls
- Always drawn, last canvas element
- 4 balls at bottom of canvas, offset 220px from left
- Spaced 100px apart
- Colors: grey=loading, orange=local, green=remote/pages, purple=other remote, black=failed
- White label text centered on each ball
- NOTE: uses local ctx = canvas.getContext('2d') which shadows global ctx

---

## Overlay Drawing Functions

### drawLyricsOverlay()
- Dark semi-transparent background (rgba 0,0,0,0.88)
- Line 0: title in bold green 32px
- Line 1: byline in italic grey 22px
- Empty lines: add 16px gap, skip
- All other lines: white 20px
- Text centered at canvas.width/2
- Starts at y=60, advances 28px per line
- "move mouse to dismiss" hint at bottom in dark grey
- Scrollable via overlayScrollY (Arrow keys)
- Dismissed by mouse movement (overlayMode = null)

### drawArtworkOverlay()
- If no artwork: dark background + "No artwork available" message
- If artwork: loads from songConfig.artwork via getAssetSource()
- Image drawn fullscreen (0,0,canvas.width,canvas.height)
- Loads lazily on first W keypress
- Dismissed by mouse movement

### drawCreditsOverlay()
- Dark semi-transparent background (rgba 0,0,0,0.92)
- Lines split on \n from songConfig.credits
- Line 0: bold green 28px
- All other lines: white 22px
- Vertically centered block
- "move mouse to dismiss" hint at bottom
- Dismissed by mouse movement

---

## DOM Elements (always visible, not canvas)

| Element | Position | Visibility |
|---------|----------|-----------|
| #songSelector | bottom-right | Always |
| #loadingStatus | below selector | Always |
| #controlRow (buttons) | bottom, left of emojis | Always |
| #musicEmojis | right of controls image | Always |
| #debugInfo | top-right | Only when debugMode=true |
| #speedControl | inside controlRow | Only when settingsOpen=true |
| #delayControl | inside controlRow | Only when settingsOpen=true |

---

## Known Issues

1. drawAssetStatusBallsOnCanvas() has `const ctx = canvas.getContext('2d')` 
   which creates a local ctx shadowing the global one. This causes the 
   ctx.save()/ctx.restore() to operate on a different context object than
   the rest of the render loop, potentially causing state bleed.
   FIX: Remove the local ctx declaration, use global ctx, remove save/restore.

2. Arrow key scrolling for lyrics overlay may not work if canvas doesn't
   have focus. Keys are on document so should be OK — needs testing.

3. beatPositionsCache is not reset in processSongData() — only 
   beatChordWordData is reset. If songs are switched, old beat positions
   may persist for matching indices.
   FIX: Add beatPositionsCache = {} alongside beatChordWordData = {} in processSongData().