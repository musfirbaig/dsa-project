$items = Get-ChildItem -path "C:\Users\Admin\Downloads\dsa-project\Inverted_Index" -recurse

if ($items.Count -eq 0) {
    Write-Warning "No files found in the specified directory."
    continue
}

$sizeSum = 0
$devSum = 0

foreach ($item in $items) {
    $sizeSum += $item.Length
    $devSum += ($item.Length - $avrg) * ($item.Length - $avrg)
}

$avrg = ($sizeSum / $items.Count)/1MB
$variance = ($devSum / $items.Count)/1MB

Write-Output "Average file size: $avrg"
Write-Output "Variance of file sizes: $variance"