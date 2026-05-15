Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
root = fso.GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = root
cmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File """ & root & "\scripts\run_xiaozhi_cli.ps1"" -Mode cli -SkipActivation"
shell.Run cmd, 0, False
