import re, glob, os

BASE = r"e:\Repos\TheTuringTestHackathon2026\app\src\app"

def fix(txt):
    # 1. Step-indicator checkmarks inside double-quoted strings
    #    e.g.  done ? "\ufffd" : n   or  "\ufffd"
    txt = re.sub(r'"(\ufffd)"', '"\u2713"', txt)
    # 2. Standalone FFFD inside JSX element text  >\ufffd<  or  >\ufffd{
    txt = re.sub(r'>(\ufffd)([<{])', lambda m: '>\u2713' + m.group(2), txt)
    # 3. Em-dash context: letter SPACE FFFD SPACE letter  (e.g. blockchain \ufffd it)
    txt = re.sub(r'([A-Za-z\u4e00-\u9fff]) (\ufffd) ([A-Za-z])',
                 lambda m: m.group(1) + ' \u2014 ' + m.group(3), txt)
    # 4. Curly-quote pair around hex addr: \ufffd 0x  or  \ufffd x...addr...\ufffd
    txt = re.sub(r"(\ufffd)(0x[0-9a-fA-F]*)", lambda m: "'" + m.group(2), txt)
    txt = re.sub(r"(0x[0-9a-fA-F]+)(\ufffd)", lambda m: m.group(1) + "'", txt)
    # 5. >= sign context: "is \ufffd 70" or "score is \ufffd"
    txt = re.sub(r'\bis (\ufffd)([= ]?\d)', lambda m: 'is >= ' + m.group(2), txt)
    txt = re.sub(r'\bis (\ufffd)([^"])', lambda m: 'is >= ' + m.group(2), txt)
    # 6. Icon strings in data objects: icon: "\ufffd" -> icon: "ok"
    txt = re.sub(r'(icon\s*:\s*")(\ufffd)(")', lambda m: m.group(1) + '\u2713' + m.group(3), txt)
    # 7. Remaining FFFD inside any string literal -> checkmark
    txt = re.sub(r'"([^"\n]*)\ufffd([^"\n]*)"',
                 lambda m: '"' + m.group(1) + '\u2713' + m.group(2) + '"', txt)
    # 8. Any remaining FFFD -> checkmark
    txt = txt.replace('\ufffd', '\u2713')
    return txt

files = glob.glob(BASE + r'\**\*.tsx', recursive=True)
fixed = []
for f in files:
    with open(f, encoding='utf-8') as fh:
        txt = fh.read()
    if '\ufffd' not in txt:
        continue
    before_count = txt.count('\ufffd')
    new_txt = fix(txt)
    after_count = new_txt.count('\ufffd')
    with open(f, 'w', encoding='utf-8', newline='') as fh:
        fh.write(new_txt)
    fixed.append(f'{os.path.basename(os.path.dirname(f))}/{os.path.basename(f)}: fixed {before_count} (remaining {after_count})')

if fixed:
    print('FIXED:')
    for s in fixed:
        print(' ', s)
else:
    print('No files needed fixing.')
