$f = "e:\Repos\TheTuringTestHackathon2026\app\src\app\tokenize\page.tsx"
$raw = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8)
$nn = ([regex]::Matches($raw, '\n\n')).Count
$n = ([regex]::Matches($raw, '\n')).Count
Write-Host "Double NLs: $nn, Total NLs: $n"
