[Setup]
AppName=Network Monitoring Tool
AppVersion=1.0
DefaultDirName={pf}\NetworkMonitoringTool
DefaultGroupName=Network Monitoring Tool
OutputDir=installer
OutputBaseFilename=NetworkMonitorSetup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\NetworkMonitor.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Network Monitoring Tool"; Filename: "{app}\NetworkMonitor.exe"
Name: "{commondesktop}\Network Monitoring Tool"; Filename: "{app}\NetworkMonitor.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a Desktop Icon"; GroupDescription: "Additional icons:"
