# Advanced Video Downloader 🚀

**Advanced Video Downloader** is a powerful Python-based toolkit designed to simplify downloading videos from various platforms, including YouTube and direct links. With a user-friendly GUI, batch download support, and real-time progress tracking, this tool is perfect for anyone who needs to save videos for offline use.

---

## Features ✨

- **Single Video Downloads**:
  - Download videos from YouTube or direct links.
  - Choose between video (with audio) or audio-only formats.
  - Select video quality (highest or lowest resolution for YouTube).

- **Batch Downloads**:
  - Download multiple videos at once from a list of URLs.
  - Track progress with a real-time progress bar.

- **User-Friendly GUI**:
  - Intuitive interface with tabs for single and batch downloads.
  - Real-time status updates and progress bars.

- **Platform Support**:
  - YouTube videos and playlists.
  - Direct video links (e.g., `.mp4`, `.mkv` files).

- **Error Handling**:
  - Handles invalid URLs, network errors, and unsupported platforms gracefully.

- **Threaded Downloads**:
  - Downloads run in the background, keeping the GUI responsive.

---

## Installation 🛠️

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/advanced-video-downloader.git
   cd advanced-video-downloader
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python video_downloader.py
   ```

---

## Usage 🖥️

1. **Single Download**:
   - Enter a video URL in the "Single Download" tab.
   - Select download options (video/audio, quality).
   - Click "Download" and choose a save location.

2. **Batch Download**:
   - Enter multiple video URLs (one per line) in the "Batch Download" tab.
   - Click "Download All" to start the batch download.

---

## Acknowledgments 🙏

- Powered by the [pytube](https://pytube.io) library for YouTube downloads.
- Built with Python and `tkinter`.
