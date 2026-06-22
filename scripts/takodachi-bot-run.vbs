Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

vbsFullName = WScript.ScriptFullName

vbsDirectory = fso.GetParentFolderName(vbsFullName)

projectRoot = fso.GetParentFolderName(vbsDirectory)
WshShell.CurrentDirectory = projectRoot

pythonwPath = fso.BuildPath(projectRoot, ".venv\Scripts\pythonw.exe")
scriptPath = fso.BuildPath(projectRoot, "src\takodachi-bot\takodachi.pyw")

WshShell.Run """" & pythonwPath & """ """ & scriptPath & """", 0, False