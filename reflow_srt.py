import re, os

RATE           = 500  # ms per word
SHORT_OVERHEAD = 800  # extra ms added when word count < 5
MIN_DUR        = 1500 # ms minimum per entry
MAX_WORDS      = 12   # flush buffer if accumulated words reach this
MAX_CHARS      = 85   # flush buffer if accumulated chars reach this
GAP            = 500  # ms gap between entries

def next_version(path):
    base = os.path.basename(path)
    m = re.match(r'^(.+?)(\d+)(\.srt)$', base, re.IGNORECASE)
    if m:
        return os.path.join(os.path.dirname(path),
                            f"{m.group(1)}{int(m.group(2))+1}{m.group(3)}")
    stem, ext = os.path.splitext(path)
    return stem + '_2' + ext

def parse_time(t):
    h, m, s = t.split(':')
    s, ms = s.split(',')
    return int(h)*3600000 + int(m)*60000 + int(s)*1000 + int(ms)

def fmt(ms):
    ms = max(0, int(ms))
    h = ms // 3600000; ms %= 3600000
    m = ms // 60000;   ms %= 60000
    s = ms // 1000;    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

# anchor source: active SRT
anchor_path = r'e:\Repos\TheTuringTestHackathon2026\document\harbour_subtitle13.srt'
out_path    = anchor_path

# ── 1. Build per-word timestamps from anchor SRT (linear interpolation) ───────
with open(anchor_path, encoding='utf-8') as f:
    content = f.read()

blocks = re.split(r'\n\n+', content.strip())
timed_words = []  # list of (word_str, timestamp_ms)
for block in blocks:
    lines = block.strip().split('\n')
    if len(lines) < 3:
        continue
    tm = re.match(r'\S+\s+-->\s+\S+', lines[1].strip())
    if not tm:
        continue
    start = parse_time(lines[1].split('-->')[0].strip())
    end   = parse_time(lines[1].split('-->')[1].strip())
    words = ' '.join(lines[2:]).split()
    for i, w in enumerate(words):
        t = start + int((end - start) * i / max(len(words), 1))
        timed_words.append((w, t))

# ── 2. Group words into sentences (flush at period or MAX_WORDS) ──────────────
# Sentence = accumulate tokens (comma/period segments) until period or MAX_WORDS
full_text = ' '.join(w for w, _ in timed_words)
tokens    = re.split(r'(?<=[,.])\s+', full_text)
tokens    = [t.strip() for t in tokens if t.strip()]

# Map each word back to its timestamp via index
word_index = 0
phrases = []   # list of (phrase_text, first_word_ts)

buffer_tokens = []
buffer_first_ts = None

for token in tokens:
    token_words = token.split()
    ts = timed_words[word_index][1]

    # Pre-flush: if adding this token would exceed char limit, flush buffer first
    prospective = ' '.join(buffer_tokens + [token])
    if buffer_tokens and len(prospective) > MAX_CHARS:
        phrases.append((' '.join(buffer_tokens), buffer_first_ts))
        buffer_tokens  = []
        buffer_first_ts = None

    if buffer_first_ts is None:
        buffer_first_ts = ts
    buffer_tokens.append(token)
    word_index += len(token_words)
    word_count = sum(len(t.split()) for t in buffer_tokens)
    if token.endswith('.') or word_count >= MAX_WORDS:
        phrases.append((' '.join(buffer_tokens), buffer_first_ts))
        buffer_tokens  = []
        buffer_first_ts = None

if buffer_tokens:
    phrases.append((' '.join(buffer_tokens), buffer_first_ts))

# ── 3. Assign timestamps: anchor to original video, no overlap ────────────────
out      = []
prev_end = 0
for i, (phrase, anchor_ts) in enumerate(phrases, 1):
    words    = phrase.split()
    overhead = SHORT_OVERHEAD if len(words) < 5 else 0
    dur      = max(len(words) * RATE + overhead, MIN_DUR)
    # start = prev_end + GAP (500ms breathing room between entries)
    start = max(anchor_ts, prev_end + GAP)
    end   = start + dur
    prev_end = end

    out.append(str(i))
    out.append(f"{fmt(start)} --> {fmt(end)}")
    out.append(phrase)
    out.append('')

# ── 4. Write output ───────────────────────────────────────────────────────────
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print(f"写入完成 → {os.path.basename(out_path)}，共 {len(phrases)} 条字幕。")
