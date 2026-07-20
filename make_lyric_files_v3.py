import re
import os

PERFORM_DIR = r"C:\Users\Owner\Documents\GitHub\perform_jan5"

songs = [
    "theLastGreatWaltz",
    "misterTut",
    "twentiethCentury",
    "accurateDontThinkTwice",
    "maryEllenCarterJoelChris",
    "fourStrongWinds",
    "rainbowConnection",
    "the-visitor",
    "aForeignAffair",
    "yourNumberOne",
    "callingUsAway",
    "yourNameHere",
    "livingInThePast",
    "upOnCrippleCreek",
    "arthurMcBride",
    "scarboroughLament"
]

CHORDS = {
    "C", "D", "E", "F", "G", "A", "B",
    "Cm", "Dm", "Em", "Fm", "Gm", "Am", "Bm",
    "C7", "D7", "E7", "F7", "G7", "A7", "B7",
    "Cmaj7", "Dmaj7", "Fmaj7", "Gmaj7", "Amaj7",
    "Dm7", "Em7", "Gm7", "Am7", "Bm7",
    "Bb", "Eb", "Ab", "Db", "Gb",
    "Bb7", "F#7",
    "F#", "C#",
    "F#m", "C#m",
    "Ab+", "A+", "Bb+", "C+", "C#+", "D+", "Eb+", "E+", "F+", "Gb+", "G+"
}

def is_chord_line(line):
    words = line.split()
    if not words:
        return False
    matches = sum(1 for w in words if w in CHORDS)
    return matches / len(words) >= 0.5

def is_beat_line(line):
    return 'ZZZ' in line or 'I01' in line or 'NB ' in line

def is_section_line(line):
    s = line.strip()
    return s.startswith('[') and ']' in s

def clean_lyric_line(line):
    line = re.sub(r'##', ' ', line)
    line = re.sub(r'\s*\$\$\s*', '\n', line)
    line = re.sub(r'\s*LL\s*\d+.*$', '', line)
    line = re.sub(r'  +', ' ', line)
    line = line.strip()
    return line

def make_lyric_file(base_name):
    txt_path = os.path.join(PERFORM_DIR, base_name + ".txt")
    if not os.path.exists(txt_path):
        print(f"NOT FOUND: {txt_path}")
        return
    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if len(lines) < 2:
        return
    title = lines[0].strip()
    byline = ""
    if ' by ' in title:
        idx = title.index(' by ')
        byline = title[idx + 1:].strip()
        title = title[:idx].strip()
    elif '  ' in title:
        parts = title.split('  ', 1)
        title = parts[0].strip()
        byline = parts[1].strip()
    output = [title]
    if byline:
        output.append(byline)
    output.append("")
    last_section = ""
    in_section = False
    for line in lines[2:]:
        stripped = line.rstrip()
        if not stripped:
            continue
        if is_section_line(stripped):
            section = re.sub(r'[\[\]{}]', '', stripped).strip()
            section = re.sub(r'\s+\d+\s*$', '', section).strip()
            if section != last_section:
                if in_section:
                    output.append("")
                last_section = section
                in_section = True
        elif is_beat_line(stripped) or is_chord_line(stripped):
            continue
        else:
            cleaned = clean_lyric_line(stripped)
            if (cleaned
                    and cleaned not in ('*', '**')
                    and not all(c in '* ' for c in cleaned)
                    and 'pedal steel' not in cleaned.lower()):
                output.append(cleaned)
    out_path = os.path.join(PERFORM_DIR, base_name + ".lyric")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    print(f"Done: {out_path}")

for base in songs:
    make_lyric_file(base)
print("All done.")