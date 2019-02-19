import sys

from sty import fg, bg, ef, rs, RgbFg

from textblob import TextBlob

MIN_INTENSITY = 60

def get_heatmap(text_file):
    text = TextBlob(text_file.read())
    max_polarity = max(text.sentences, key=lambda x: x.polarity).polarity
    min_polarity = min(text.sentences, key=lambda x: x.polarity).polarity
    max_polarity_deviation = max(abs(max_polarity), abs(min_polarity))
    max_subjectivity = max(text.sentences, key=lambda x: x.subjectivity).subjectivity
    scaled = [(s, s.polarity/max_polarity_deviation, s.subjectivity/max_subjectivity) for s in text.sentences]
    return scaled

def colorize(text, heat1, heat2):
    remainder_intensity = 255 - MIN_INTENSITY
    r, g, b = [MIN_INTENSITY] * 3
    if heat1 < 0:
        r += int(remainder_intensity * (-heat1))
    elif heat1 > 0:
        g += int(remainder_intensity * heat1)
    b += int(remainder_intensity * heat2)
    return fg(*(r, g, b)) + text + fg.rs

if __name__ == "__main__":
    with open(sys.argv[1], encoding='utf-8', errors='ignore') as infile:
        phmap = get_heatmap(infile)
        colorized = [colorize(str(s[0]), s[1], s[2]) for s in phmap]
        print(*colorized)
