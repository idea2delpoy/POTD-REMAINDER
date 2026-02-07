[Setup]
AppName=POTD Scheduler
AppVersion=1.0
AppPublisher=I2D
DefaultDirName={pf}\POTD Scheduler
DefaultGroupName=POTD Scheduler
DisableProgramGroupPage=yes
OutputDir=installer
OutputBaseFilename=POTD_Scheduler_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\app.exe

[Files]
Source: "dist\app.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\POTD Scheduler"; Filename: "{app}\app.exe"
Name: "{commondesktop}\POTD Scheduler"; Filename: "{app}\app.exe"

[Run]
Filename: "{app}\app.exe"; Description: "Launch POTD Scheduler"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\storage"
