$f = "e:\Repos\TheTuringTestHackathon2026\app\src\app\tokenize\page.tsx"
$raw = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8)
$start = $raw.IndexOf("{/* SFC Approval panel")
$endMarker = "Proceed to Deployment ..."
$endIdx = $raw.IndexOf($endMarker) + $endMarker.Length
$closeBtn = $raw.IndexOf("</button>", $endIdx)
$afterClose = $closeBtn + "</button>".Length
$closeDiv = $raw.IndexOf("</div>", $afterClose)
$cutEnd = $closeDiv + "</div>".Length
Write-Host "Start: $start, End: $cutEnd"
$raw.Substring($start, $cutEnd - $start)
