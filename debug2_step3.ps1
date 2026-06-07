$f = "e:\Repos\TheTuringTestHackathon2026\app\src\app\tokenize\page.tsx"
$raw = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8)
$start = $raw.IndexOf("{/* SFC Approval panel")
$cutEnd = 31743  # from debug_step3.ps1 output
$section = $raw.Substring($start, $cutEnd - $start)
$nn = ([regex]::Matches($section, '\n\n')).Count
$n = ([regex]::Matches($section, '\n')).Count
Write-Host "Section double NLs: $nn, total NLs: $n"
Write-Host "Section length: $($section.Length)"
# Show first 200 chars byte by byte
$section.Substring(0, 100).ToCharArray() | ForEach-Object { $c = [int]$_; if ($c -lt 32) { "[$c]" } else { [char]$c } } | Write-Output
