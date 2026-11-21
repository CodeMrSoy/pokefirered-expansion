Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[Windows.Forms.Application]::EnableVisualStyles()

$root = (Get-Location).Path
$profile = Join-Path ([Environment]::GetFolderPath('LocalApplicationData')) 'LivingQuantumWorldPhase11'
$python = Join-Path $root 'python\python.exe'
$form = New-Object Windows.Forms.Form
$form.Text = 'Pokemon Quantum - Living World'
$form.StartPosition = 'CenterScreen'
$form.ClientSize = New-Object Drawing.Size(940, 570)
$form.MinimumSize = New-Object Drawing.Size(850, 480)
$form.Font = New-Object Drawing.Font('Segoe UI', 10)

$panel = New-Object Windows.Forms.FlowLayoutPanel
$panel.Dock = 'Left'
$panel.Width = 250
$panel.Padding = New-Object Windows.Forms.Padding(14)
$panel.FlowDirection = 'TopDown'
$panel.WrapContents = $false

$view = New-Object Windows.Forms.TextBox
$view.Dock = 'Fill'
$view.Multiline = $true
$view.ReadOnly = $true
$view.ScrollBars = 'Both'
$view.WordWrap = $false
$view.Font = New-Object Drawing.Font('Consolas', 10)
$form.Controls.Add($view)
$form.Controls.Add($panel)

function Add-MenuButton($label, $action) {
    $button = New-Object Windows.Forms.Button
    $button.Text = $label
    $button.Width = 218
    $button.Height = 38
    $button.Add_Click($action)
    $panel.Controls.Add($button)
}

function Start-Host($flag) {
    try {
        $arguments = @('-B', 'play.py')
        if ($flag) { $arguments += $flag }
        Start-Process -FilePath $python -WorkingDirectory $root -ArgumentList $arguments
    } catch {
        [Windows.Forms.MessageBox]::Show($_.Exception.Message, 'Pokemon Quantum') | Out-Null
    }
}

function Read-SharedText($path) {
    $share = [IO.FileShare]::ReadWrite -bor [IO.FileShare]::Delete
    $stream = [IO.File]::Open($path, [IO.FileMode]::Open, [IO.FileAccess]::Read, $share)
    try {
        $reader = New-Object IO.StreamReader($stream)
        try { return $reader.ReadToEnd() } finally { $reader.Dispose() }
    } finally { $stream.Dispose() }
}

$script:monitor = $false
$script:lastSnapshot = ''
$intro = "Choose Play Pokemon Quantum for your main save, or Living World Demo for the Pewter scenario.`r`n`r`nUse Settings and controls to change keyboard bindings. Diagnostics runs the sandbox and local model checks."

Add-MenuButton 'Play Pokemon Quantum' { Start-Host }
Add-MenuButton 'Living World Demo' { Start-Host '--phase11-demo' }
Add-MenuButton 'Living World Monitor' {
    $script:monitor = $true
    $script:lastSnapshot = ''
    $view.Text = 'Waiting for a game session to publish its first snapshot.'
}
Add-MenuButton 'Settings and controls' { Start-Host '--controls' }
Add-MenuButton 'Diagnostics' {
    $script:monitor = $false
    $view.Text = Read-SharedText (Join-Path $root 'release.json')
    Start-Process -FilePath (Join-Path $root 'Validate Offline Runtime.cmd') -WorkingDirectory $root
}
Add-MenuButton 'Save management' {
    $script:monitor = $false
    $view.Text = "Saves, input settings and the Living World database are stored at:`r`n$profile`r`n`r`nClose the game before making a backup. Backups include battery saves and their matching Living World database."
    $choice = [Windows.Forms.MessageBox]::Show('Create a backup now? Choose No to open the save folder.', 'Save management', 'YesNoCancel')
    if ($choice -eq 'Yes') {
        $result = & $python -B play.py --profile-backup 2>&1 | Out-String
        $view.AppendText("`r`n`r`n" + $result)
    } elseif ($choice -eq 'No') {
        [IO.Directory]::CreateDirectory($profile) | Out-Null
        Invoke-Item -LiteralPath $profile
    }
}

$timer = New-Object Windows.Forms.Timer
$timer.Interval = 1200
$timer.Add_Tick({
    if (!$script:monitor) { return }
    try { $snapshot = Read-SharedText (Join-Path $profile 'monitor.json') } catch { return }
    try { $state = ConvertFrom-Json $snapshot } catch { return }
    $age = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds() - $state.updated
    $status = if ($state.running -and $age -lt 8) { 'Live' } else { 'Last recorded session' }
    $position = $view.SelectionStart
    $rendered = "$status`r`nHost-only residents have no ROM sprites. ROM actor projections are intended locations; the nearby hint is confirmed by the ROM.`r`n`r`n" + $snapshot
    if ($rendered -eq $script:lastSnapshot) { return }
    $script:lastSnapshot = $rendered
    $view.Text = $rendered
    $view.SelectionStart = [Math]::Min($position, $view.TextLength)
    if ($position -gt 0) { $view.ScrollToCaret() }
})
$view.Text = $intro
$timer.Start()
try { [void]$form.ShowDialog() } finally { $timer.Dispose(); $form.Dispose() }
