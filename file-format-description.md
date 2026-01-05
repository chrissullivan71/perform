# File Format for The Song Performance Program: Example with "The Visitor"

The Song Performance Program is used to animate synchronized lyrics, instrumentals, chords, and beats from structured `.txt` files. This document uses *"The Visitor" by Chris Sullivan* as a real-world example of the **Lyric/Instrumental Quad** format.

---

## Key Concept: The Lyric/Instrumental Quad

A **Lyric/Instrumental Quad** groups four lines that work together to represent a segment of performance timing. It consists of the following:

1. **Section Line**: Marks the section name, always surrounded by square brackets (`[]`).
2. **Lyric/Instrumental Line**:
   - For lyric sections: Contains the words or syllables, ending with `ZZZ`.
   - For instrumental sections: Contains **asterisks (`*`)**, spaced to align with beats, and ending in `I##` (instrument marker).
3. **Chord Line**: Specifies the chords from the `CHORDS` table.
4. **Beat Line**: Shows the explicit beats aligned with syllables, chords, or asterisks.

---

## Example Breakdown of "The Visitor"

Let’s examine portions of the file line-by-line.

---

### **1. Instrumental Section: Intro**

The **Intro** section contains instrumental music and does not include lyrics. Beats (`1 3 5 7`) align with the asterisks (`*`) and chords (`C D7 Bm Em`) played at specific points.

```
[Intro]
     C         D7       Bm    Em 
     *         *        *     *
     1         3        5     7                 I01         NB 02
```

- **Section Line**: `[Intro]` specifies the start of the Intro section.
- **Instrumental Line**: `* * * *` represents musical beats using asterisks spaced to match the beats.
  - `I01`: The instrument code corresponds to information in the program (e.g., acoustic guitar).
- **Chord Line**: Lists chords (`C, D7, Bm, Em`) played on the respective beats.
- **Beat Line**: Lists actual beat numbers (`1 3 5 7`) aligned with the asterisks and chords.

---

### **2. Lyric Section: Verse 1**

The **Verse 1** section introduces lyrical content. Each word or syllable aligns with a beat.

```
[Verse 1]
        G          D7       G       G7
Well he mightve arrived by courier
        1          3        5       7           ZZZ         LL 01
```

- **Section Line**: `[Verse 1]` marks the start of a new verse.
- **Lyric Line**: "Well he mightve arrived by courier" contains all lyric syllables for this line, ending with `ZZZ` to signal the end of lyrics.
  - **External Reference**: Each syllable (e.g., `Well`, `he`, `mightve`) maps to the `SYLLABLE_DICT`.
- **Chord Line**: Specifies the chords (`G`, `D7`, `G`, `G7`).
- **Beat Line**: Lists beats (`1 3 5 7`) aligned with the lyric syllables and chords.
- **Metadata Field**: `LL 01` indicates this is Lyric Line 1 in the song.

---

### **3. Other Sections: Crickets**

The **Crickets** sections provide recurring instrumental interludes. Each interlude is similar, consisting of three beats.

```
[Crickets]
    G         C         G     
    *         *         *    
    1         2         3                       I01         NB 03
```

- **Section Line**: `[Crickets]` identifies the section.
- **Instrumental Line**: `* * *` represents each beat of the recurring interlude.
  - Beats are short and grouped into three-note intervals.
  - **Instrument Marker**: `I01` indicates the instrument used (e.g., acoustic guitar).
- **Chord Line**: `G C G` chords repeat in this segment.
- **Beat Line**: `1 2 3` shows the individual beats.

---

### **4. Chorus**

The **Chorus** sections contain lyrics with repeated content and beat patterns that emphasize specific syllables.

```
[Chorus]
          G              D7        G       G7 
Theres a cricket on the twentieth floor 
          1              3         5       7    ZZZ         LL 05
```

- Same structure as **Verse 1**, but new lyrics ("Theres a cricket on the twentieth floor").
- **Metadata**: `LL 05` identifies this as Lyric Line 5.

---

### **5. Bridge**

The **Bridge** introduces unique rhythmic and lyrical elements. The beats align with intermittent syllables.

```
[Bridge]
       Bm               Em
Out of place and out of time 
       1         3      5                       ZZZ         LL 22
```

- **Lyric Line**: Phrases like "Out of place and out of time" map directly to the `SYLLABLE_DICT` table.
- **Chord Line**: `Bm Em` accompanies the lyrics with aligned chords.
- **Beat Line**: Lists beats (`1 3 5`) for this slower-paced bridge section.

---

## Explicit Rules

### 1. Section Lines

### 2. Chords
- Each chord in the Chord Line is associated with its respective beat and must exist in `CHORDS`.   A chord line's list of chords fills 40% of the charaters on that line.

### 3. Lyrics and Syllables
- Lyric lines' lyriic content ends with `ZZZ`.
- Each syllable is validated against `SYLLABLE_DICT`.

### 4. Instrumentals
- Asterisks (`*`) denote beats, and the line's content is ended with `I##` instead of ZZZ which a normal lyric line's lyric content ends with.

---

## External Tables

### CHORDS Table
        const CHORDS = [
            "C", "D", "E", "F", "G", "A", "B",
            "Cm", "Dm", "Em", "Fm", "Gm", "Am", "Bm",
            "C7", "D7", "E7", "F7", "G7", "A7", "B7",
            "Cm7", "Dm7", "Em7", "Fm7", "Gm7", "Am7", "Bm7",
            "Cmaj7", "Dmaj7", "Emaj7", "Fmaj7", "Gmaj7", "Amaj7", "Bmaj7",
            "C♭", "D♭", "E♭", "F♭", "G♭", "A♭", "B♭",
            "C♯", "D♯", "E♯", "F♯", "G♯", "A♯", "B♯"
        ];

### SYLLABLE_DICT Table
		// ---------------------------
		// SYLLABLE DICTIONARY
		// ---------------------------

		const SYLLABLE_DICT = {
 			// ---------------------------
			// Don't Think Twice, It's All Right
			// ---------------------------
			"baby": ["baby"],
			"before": ["be", "fore"],
			"better": ["bet", "ter"],
			"could": ["could"],
			"done": ["done"],
			"farewell": ["fare", "well"],
			"goodbye": ["good", "bye"],
			"honey": ["hon", "ey"],
			"kind": ["kind"],
			"mind": ["mind"],
			"never": ["nev", "er"],
			"precious": ["pre", "cious"],
			"reason": ["rea", "son"],
			"rooster": ["roos", "ter"],
			"saying": ["say", "ing"],
			"talking": ["talk", "ing"],
			"think": ["think"],
			"travelin": ["trav", "el", "in"],
			"wasted": ["wast", "ed"],
			"window": ["win", "dow"],
			"woman": ["wom", "an"],
			"wonder": ["won", "der"],
			"wondrin": ["wond", "rin"],
			"anymore": ["an", "y", "more"],
			"anyway": ["an", "y", "way"],

			// ---------------------------
			// Rainbow Connection
			// ---------------------------
			"amazing": ["a", "maz", "ing"],
			"answered": ["an", "swered"],
			"asleep": ["a", "sleep"],
			"believe": ["be", "lieve"],
			"believed": ["be", "lieved"],
			"connection": ["con", "nec", "tion"],
			"dreamers": ["dream", "ers"],
			"illusion": ["il", "lu", "sion"],
			"illusions": ["il", "lu", "sions"],
			"laughter": ["laugh", "ter"],
			"lovers": ["lov", "ers"],
			"magic": ["mag", "ic"],
			"morning": ["morn", "ing"],
			"probably": ["prob", "ab", "ly"],
			"rainbow": ["rain", "bow"],
			"rainbows": ["rain", "bows"],
			"sailors": ["sail", "ors"],
			"somebody": ["some", "bod", "y"],
			"something": ["some", "thing"],
			"someday": ["some", "day"],
			"stargazing": ["star", "gaz", "ing"],
			"supposed": ["sup", "posed"],
			"visions": ["vi", "sions"],
			"voices": ["voic", "es"],
			"wonder": ["won", "der"],

			// ---------------------------
			// High Flight
			// ---------------------------
			"climbed": ["climbed"],
			"delirious": ["de", "lir", "i", "ous"],
			"danced": ["danced"],
			"footless": ["foot", "less"],
			"joined": ["joined"],
			"laugh": ["laugh"],
			"mirth": ["mirth"],
			"silvered": ["sil", "verd"],
			"skies": ["skies"],
			"slipped": ["slipped"],
			"surly": ["sur", "ly"],
			"tumblin": ["tum", "blin"],
			"wings": ["wings"],

			// ---------------------------
			// The Visitor
			// ---------------------------
			"*": ["*"],
			"arrived": ["ar", "rived"],
			"courier": ["cour", "i", "er"],
			"cricket": ["crick", "et"],
			"elevator": ["el", "e", "va", "tor"],
			"figured": ["fig", "ured"],
			"hoppin": ["hop", "pin"],
			"mate": ["mate"],
			"miss": ["miss"],
			"people": ["peo", "ple"],
			"playin": ["play", "in"],
			"probly": ["prob", "ly"],
			"scrape": ["scrape"],
			"singin": ["sing", "in"],
			"twentieth": ["twen", "ti", "eth"],
            "unlikely": ["un", "like", "ly"],

			// ---------------------------
			// CONTRACTIONS: Don't Think Twice, It's All Right
			// ---------------------------
			"ain't": ["ain't"],
			"can't": ["can't"],
			"could've": ["could've"],
			"couldn't": ["couldn't"],
			"didn't": ["didn't"],
			"doesn't": ["doesn't"],
			"don't": ["don't"],
			"hadn't": ["hadn't"],
			"hasn't": ["hasn't"],
			"haven't": ["haven't"],
			"he's": ["he's"],
			"i'd": ["i'd"],
			"i'll": ["i'll"],
			"i'm": ["i'm"],
			"i've": ["i've"],
			"isn't": ["isn't"],
			"it's": ["it's"],
			"let's": ["let's"],
			"she's": ["she's"],
			"shouldn't": ["shouldn't"],
			"that's": ["that's"],
			"there's": ["there's"],
			"they'll": ["they'll"],
			"they're": ["they're"],
			"they've": ["they've"],
			"wasn't": ["wasn't"],
			"we're": ["we're"],
			"weren't": ["weren't"],
			"what's": ["what's"],
			"where's": ["where's"],
			"who's": ["who's"],
			"won't": ["won't"],
			"wouldn't": ["wouldn't"],
			"you'd": ["you'd"],
			"you'll": ["you'll"],
			"you're": ["you're"],
			"you've": ["you've"],

			// ---------------------------
			// CONTRACTIONS: Rainbow Connection
			// ---------------------------
			"what's": ["what's"],
			"it's": ["it's"],
			"didn't": ["didn't"],
			"doesn't": ["doesn't"],
			"there's": ["there's"],
			"we've": ["we've"],
			"he's": ["he's"],
			"you're": ["you're"],

			// ---------------------------
			// CONTRACTIONS: High Flight
			// ---------------------------
			// (None commonly found; add if needed)

			// ---------------------------
			// CONTRACTIONS: The Visitor
			// ---------------------------
			"he'd": ["he'd"],
			"he's": ["he's"],
			"she's": ["she's"],
			"it's": ["it's"],
			"didn't": ["didn't"],
			"can't": ["can't"],
			"doesn't": ["doesn't"],
			"there's": ["there's"],
			"we're": ["we're"],
			"you're": ["you're"]
		};



## Summary of the File Format: quads of lines, one section line, one lytric line, one chord line, and one beat line in each quad.
- Sections are named with brackets (`[]`).
- Lyrics and syllables reference `SYLLABLE_DICT`.
- Chords reference `CHORDS`.
- Beats align precisely with syllables, asterisks, and chords.

- Square brackets (`[]`) enclose section names (e.g., `[Intro]`, `[Chorus]`).

# Documenting the Crickets Section in "The Visitor"

The **Crickets** section is an instrumental interlude consisting of **3 bars in 4/4 time**. The section relies on precise vertical alignment of chords, chirps, and beats within a **fixed-width font**. This ensures the timing between beats, chords, and chirps is clear and consistent.

---

## Why Fixed-Width Fonts Are Required

Using a fixed-width font (e.g., **Courier**, **Consolas**, **Monaco**, or **Lucida Console**) ensures every character occupies the same horizontal width. This is critical for:
1. Maintaining vertical alignment between chords, chirps (`*`), and beats.
2. Reflecting the correct spacing for the **passage of time** between beats.

Without a fixed-width font, visual alignment becomes distorted, and timing information appears incorrect.

---

## The Crickets Section Representation

The Crickets section is represented as follows:

```
[Crickets]
    G     G     C     C     G     G     C     C     G     C     G     C
          *                       *                 *
          2                       6                 9                       I01         NB 03

## How to View or Edit This `.txt` File

### Fixed-Width Font Requirement

To maintain proper alignment when viewing or editing this `.txt` file, remember,
character placcement from left to right (and therefore word placement chord placement and beat placement) represents the passage
of time from the beginning to the end of each line of the song.  To this end, fixed-width fonts are required.

1. Open the file in a text editor that supports fixed-width (monospaced) fonts.
   - Examples: Notepad, VS Code, Sublime Text, Atom, Courier
2. Set the font to a monospaced font:
   - Courier, Consolas, Monaco, Lucida Console.

### Ensure Spacing Consistency
- Do NOT modify the spacing between characters unless explicitly editing timing.
- Misaligned spaces result in incorrect timing visualization.

3. **Vertical Alignment**:
   - Chords, lyrics, and beats are verically aligned to indicate simultaniety.

Metadata:
While an Instrumental (lyricless, music-only) line is indicated by the I in I?? which takws the place of ZZZ on sung lyric lines, 
the two numerric digis followjng it, the ?? in "I??" indicate the instrument to be played.  01 is used to indicate Classical Guitar.