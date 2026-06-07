import re, os

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
    h = ms // 3600000; ms %= 3600000
    m = ms // 60000;   ms %= 60000
    s = ms // 1000;    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

RATE = 450  # ms per word
path = r'e:\Repos\TheTuringTestHackathon2026\document\harbour_subtitle3.srt'
out_path = next_version(path)

with open(path, encoding='utf-8') as f:
    content = f.read()

blocks = re.split(r'\n\n+', content.strip())
entries = []
for block in blocks:
    lines = block.strip().split('\n')
    if len(lines) < 3:
        continue
    m = re.match(r'(\S+)\s+-->\s+(\S+)', lines[1].strip())
    if not m:
        continue
    entries.append({
        'idx':   lines[0].strip(),
        'start': parse_time(m.group(1)),
        'end':   parse_time(m.group(2)),
        'text':  '\n'.join(lines[2:])
    })

new_entries = []
for i, e in enumerate(entries):
    words    = e['text'].split()
    needed   = len(words) * RATE
    duration = e['end'] - e['start']
    next_start = entries[i + 1]['start'] if i + 1 < len(entries) else e['end'] + 10000

    if needed <= duration:
        new_entries.append(e)
        continue

    # --- need to split ---
    orig_lines = e['text'].split('\n')
    if len(orig_lines) >= 2:
        # Split at the natural line break (first line vs rest)
        text1 = orig_lines[0]
        text2 = '\n'.join(orig_lines[1:])
    else:
        # No line break: split at word midpoint
        mid   = len(words) // 2
        text1 = ' '.join(words[:mid])
        text2 = ' '.join(words[mid:])

    w1 = len(text1.split())
    w2 = len(text2.split())
    total_w = w1 + w2

    # Mid time: proportional share within the original window
    mid_time = e['start'] + int(duration * w1 / total_w)

    # End of part 2: use any gap after the original end, capped at next_start
    end2 = min(e['start'] + needed, next_start)

    new_entries.append({'idx': e['idx'], 'start': e['start'], 'end': mid_time, 'text': text1})
    new_entries.append({'idx': e['idx'], 'start': mid_time,   'end': end2,     'text': text2})

    print(f"[{e['idx']:>2}] split {len(words)}词/{duration/1000:.1f}s  "
          f"→ [{w1}词/{( mid_time - e['start'])/1000:.1f}s] + [{w2}词/{(end2 - mid_time)/1000:.1f}s]  "
          f"(gap used: {max(0, end2 - e['end'])/1000:.1f}s)")

# Renumber
out = []
for i, e in enumerate(new_entries, 1):
    out.append(str(i))
    out.append(f"{fmt(e['start'])} --> {fmt(e['end'])}")
    out.append(e['text'])
    out.append('')

with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print(f"\n写入完成 → {os.path.basename(out_path)}，共 {len(new_entries)} 条字幕。")
