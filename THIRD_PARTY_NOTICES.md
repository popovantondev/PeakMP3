# Third-party components

PeakMP3 starts FFmpeg as a separate process; no FFmpeg library is linked into the application.

- Shared 2.6.0 installer: FFmpeg 5.1.6 minimal x86 and LAME 3.100, LGPL terms. Matching build configuration, licenses and corresponding sources are in the [shared release](https://github.com/popovantondev/YouTubeDownloader/releases/tag/v2.6.0), including `YouTubeDownloader-2.6.0-FFmpeg-Corresponding-Sources.zip`. See the [package notices](https://github.com/popovantondev/YouTubeDownloader/blob/main/THIRD_PARTY_NOTICES.md).
- Roboto Condensed website font: SIL Open Font License 1.1, [license](assets/site/fonts/OFL.txt).
- Three music excerpts by Kevin MacLeod (incompetech.com): CC BY 4.0. Trimming, PeakMP3 processing and MP3 encoding are disclosed in [music/CREDITS.md](music/CREDITS.md). The application’s source terms do not restrict these music files.
- Browser downloader dependencies belong to the separate YouTubeDownloader repository and shared package, not to the PeakMP3 native executable.
