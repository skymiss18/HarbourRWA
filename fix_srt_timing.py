import re, os, glob

def next_version(path):
    """Given foo_N.srt, return foo_(N+1).srt in the same dir."""
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

path = r'e:\Repos\TheTuringTestHackathon2026\document\harbour_subtitle3.srt'
out_path = next_version(path)
with open(path, encoding='utf-8') as f:
    content = f.read()

blocks = re.split(r'\n\n+', content.strip())
entries = []
for block in blocks:
    lines = block.strip().split('\n')
    if len(lines) < 3: continue
    m = re.match(r'(\S+)\s+-->\s+(\S+)', lines[1].strip())
    if not m: continue
    entries.append({
        'idx': lines[0].strip(),
        'start': parse_time(m.group(1)),
        'end':   parse_time(m.group(2)),
        'text':  '\n'.join(lines[2:])
    })

RATE = 450  # ms per word
MIN  = 1500

for e in entries:
    e['needed'] = max(len(e['text'].split()) * RATE, MIN)

for i, e in enumerate(entries):
    new_end = e['start'] + e['needed']
    if i + 1 < len(entries):
        new_end = min(new_end, entries[i+1]['start'])
    old_dur = e['end'] - e['start']
    new_dur = new_end - e['start']
    if new_dur != old_dur:
        print(f"[{e['idx']:>2}] {len(e['text'].split()):>2}词  {old_dur/1000:.1f}s -> {new_dur/1000:.1f}s  (需{e['needed']/1000:.1f}s)")
    e['new_end'] = new_end

out = []
for e in entries:
    out.append(e['idx'])
    out.append(f"{fmt(e['start'])} --> {fmt(e['new_end'])}")
    out.append(e['text'])
    out.append('')

with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print(f"\n写入完成 → {os.path.basename(out_path)}")
