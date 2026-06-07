b = open(r'e:\Repos\TheTuringTestHackathon2026\app\src\app\compliance\page.tsx', 'rb').read()
line_num = 1
line_start = 0
for i in range(len(b)-1):
    if b[i] == 0x0d and b[i+1] == 0x0a:
        if line_num == 214:
            line = b[line_start:i]
            print(f'Line 214 ({len(line)} bytes): {line.hex()}')
            decoded = line.decode('utf-8', errors='replace')
            print(f'Line 214: {decoded!r}')
            if len(line) >= 39:
                print(f'Col 38 (0-idx): 0x{line[38]:02X}')
            break
        line_num += 1
        line_start = i + 2
        
# Also check if this error is from old log or new
import os, datetime
log_path = r'e:\Repos\TheTuringTestHackathon2026\app\.next\dev\logs\next-development.log'
mtime = os.path.getmtime(log_path)
print(f'\nLog last modified: {datetime.datetime.fromtimestamp(mtime)}')
