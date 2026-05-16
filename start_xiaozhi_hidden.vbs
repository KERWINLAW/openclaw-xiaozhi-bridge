Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
root = fso.GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = root
Set env = shell.Environment("Process")
env("PYTHONIOENCODING") = "utf-8"
env("LOG_LEVEL") = "INFO"
env("PY_XIAOZHI_DATA_DIR") = root & "\.runtime\data"
env("PY_XIAOZHI_HEADLESS") = "1"
env("VIRTUAL_ENV") = root & "\.venv"
env("PATH") = root & "\.venv\Scripts;" & env("PATH")
env("PYTHONPATH") = root & "\.venv\Lib\site-packages"
python = root & "\.uv-python\cpython-3.12-windows-x86_64-none\pythonw.exe"
If Not fso.FileExists(python) Then
    python = root & "\.venv\Scripts\pythonw.exe"
End If
cmd = """" & python & """ """ & root & "\main.py"" --mode cli --protocol websocket --skip-activation"
shell.Run cmd, 0, False
