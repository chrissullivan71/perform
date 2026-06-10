# Adding a New Song to Promptoid

## Files You Will Need
- `songname.txt` — lyrics, chords, beats
- `songname.mp3` — audio recording
- `songnameChords_v1.jpg` — chord chart for baritone uke
- `songname.lyric` — generated from txt file

---

## Step 1: Create the txt File

Format: `songname.txt` in the perform folder.

```
Song Title  by Songwriter
4/4

[Section Name]
C        Am7      Dm7      G7
Lyric line goes here
1        3        5        7        ZZZ    LL 01

[Section Name]
C        Am7      Dm7      G7
Next lyric line
1        3        5        7        ZZZ    LL 02
```

Rules:
- Line 1: title (use two spaces before "by" for byline extraction)
- Line 2: time signature
- Each lyric group: section header, chord line, lyric line, beat line (with ZZZ)
- Instrumental lines use `*` as the lyric
- LL numbers should be sequential with no gaps or duplicates
- `##` in a lyric line splits it for display across two lines

---

## Step 2: Add the mp3

Copy `songname.mp3` to the perform folder.

---

## Step 3: Add to the Song Selector

In `testnewperform.html`, find the `<select id="songSelector">` block near the top of the file:

```html
<select id="songSelector">
    <option value="">Select Song...</option>
    <option value="Four Strong Winds">Four Strong Winds</option>
    ...
    <option value="lastWaltz">The Last Great Waltz</option>
    <!-- ADD YOUR NEW SONG HERE: -->
    <option value="songKey">Song Title</option>
</select>
```

The `value` must exactly match the key you use in `songFileMap`.

---

## Step 4: Add to songFileMap

In `testnewperform.html`, find `const songFileMap = {` and add your entry
**before** `"lastWaltz"` (or any existing entry). Example:

```javascript
const songFileMap = {
    "songKey": {
        base: "songname",
        display: "Song Title",
        bouncesPerLine: 8,
        bounceDuration: 1.0,
        background: "background.jpg",
        fontSize: 36,
        font: "Consolas",
        lyricsFile: "songname.lyric",
        chords: "songnameChords_v1.jpg",
        credits: `Song Title\nWritten by Songwriter\nPerformer — instrument\nVenue, Year`,
        appointments: [
            { time: 0.00,   type: "jump", nextIndex: 99, reference: "beginning", fired: false },
            { time: 5.00,   type: "jump", nextIndex: 0,  reference: "Intro", fired: false },
            { time: 12.50,  type: "jump", nextIndex: 1,  reference: "First lyric line", fired: false },
            // ... one appointment per lyric line ...
            { time: 200.00, type: "Y1pause", nextIndex: 26, reference: "song ended", fired: false }
        ]
    },
    "lastWaltz": {
```

### Appointment rules:
- `nextIndex` is zero-based — first lyric line = 0
- `nextIndex: 99` at time 0.00 is a safe "do nothing" start
- `time` is seconds from start of mp3
- Last appointment is always `Y1pause` with `nextIndex` = total number of lyric lines
- One appointment per lyric line — the time is when that line starts in the audio
- `bounceDuration` × `bouncesPerLine` should roughly equal the average seconds per line

### Estimating bounceDuration:
Divide total song duration by number of lyric lines to get average seconds per line.
With `bouncesPerLine: 8`, divide that by 8 to get `bounceDuration`.

---

## Step 5: Create the Chord Chart JPG

Generate `songnameChords_v1.jpg` with the chord shapes for baritone
ukulele (DGBE tuning). Provide the list of chords used in the song.

Download the JPG and copy it to the perform folder.

---

## Step 6: Update the Syllable Dictionary

In `testnewperform.html`, find `const SYLLABLE_DICT = {` and add entries for
multi-syllable words in the new song's lyrics. Add them in a labelled section:

```javascript
// Song Title
"traveling": ["trav", "el", "ing"],
"foreign": ["for", "eign"],
"affair": ["af", "fair"],
// ... etc
```

Rules:
- Key is the word in lowercase, with apostrophes stripped
  (e.g. `obsession's` → key is `obsessions`)
- Value is array of syllables
- Single-syllable words don't need entries
- Contractions count as one syllable and don't need entries
- If a word highlights too wide, it's missing from the dictionary

---

## Step 7: Generate the Lyric File

Open `make_lyric_files_v3.py` and add the song base name to the `songs` list:

```python
songs = [
    "theLastGreatWaltz",
    ...
    "songname",   # ADD HERE
]
```

Run it:
```
py make_lyric_files_v3.py
```

This generates `songname.lyric` in the perform folder.

---

## Step 8: Commit Everything

```
git add testnewperform.html
git add songname.txt
git add songname.mp3
git add songnameChords_v1.jpg
git add songname.lyric
git add make_lyric_files_v3.py
git commit -m "Added Song Title"
git push origin main
```

---

## Step 9: Upload to Server

FTP these files to `sullivanweb.me/mystuff/performances/`:
- `testnewperform.html`
- `songname.txt`
- `songname.mp3`
- `songnameChords_v1.jpg`
- `songname.lyric`

---

## Troubleshooting

**Song doesn't appear in dropdown** — `songFileMap` key doesn't match the
`<option value="">` in the selector, or the entry is missing.

**"Song could not be loaded"** — `songname.txt` is missing from the folder.

**Audio 404 error** — `songname.mp3` is missing or filename doesn't match `base`
field in songFileMap.

**K key doesn't work** — chord chart JPG is missing or filename doesn't match
`chords` field in songFileMap. On Linux servers, filename is case-sensitive.

**Highlighting too wide** — word is missing from SYLLABLE_DICT. Add it.

**Counter gets stuck** — an appointment's `nextIndex` points to a line that
doesn't exist, or `nextAppointmentPending` is blocking natural advance.
Check that `nextIndex` values match actual lyric line indices (zero-based).

**Lines display in wrong order** — appointment times are wrong or out of order.

