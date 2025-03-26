[Setup]
AppName=YouTube Playlist Downloader
AppVersion=1.0
DefaultDirName={pf}\YouTubeDownloader
DefaultGroupName=YouTube Downloader
OutputDir=.
OutputBaseFilename=YouTubeDownloaderSetup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\Youtube_Playlist_Downloader.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\YouTube Downloader"; Filename: "{app}\Youtube_Playlist_Downloader.exe"
Name: "{commondesktop}\YouTube Downloader"; Filename: "{app}\Youtube_Playlist_Downloader.exe"

[Run]
Filename: "{app}\Youtube_Playlist_Downloader.exe"; Description: "Launch YouTube Downloader"; Flags: nowait postinstall
