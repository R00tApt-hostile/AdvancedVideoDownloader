import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from pytube import YouTube, Playlist
import requests
from tqdm import tqdm
from threading import Thread

class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Video Downloader")
        self.root.geometry("700x500")

        # Notebook for tabs
        self.notebook = ttk.Notebook(root)
        
        # Single Download Tab
        self.single_tab = ttk.Frame(self.notebook)
        self.create_single_tab()
        
        # Batch Download Tab
        self.batch_tab = ttk.Frame(self.notebook)
        self.create_batch_tab()
        
        self.notebook.add(self.single_tab, text="Single Download")
        self.notebook.add(self.batch_tab, text="Batch Download")
        self.notebook.pack(expand=True, fill='both')

    def create_single_tab(self):
        # URL Entry
        self.url_label = ttk.Label(self.single_tab, text="Enter Video URL:")
        self.url_label.pack(pady=10)

        self.url_entry = ttk.Entry(self.single_tab, width=70)
        self.url_entry.pack(pady=5)

        # Download Options
        self.options_label = ttk.Label(self.single_tab, text="Select Download Option:")
        self.options_label.pack(pady=10)

        self.download_option = tk.StringVar(value="video")
        ttk.Radiobutton(self.single_tab, text="Video (MP4)", variable=self.download_option, value="video").pack()
        ttk.Radiobutton(self.single_tab, text="Audio Only (MP4)", variable=self.download_option, value="audio").pack()

        # Quality Selection
        self.quality_label = ttk.Label(self.single_tab, text="Select Quality (YouTube only):")
        self.quality_label.pack(pady=10)

        self.quality_var = tk.StringVar(value="highest")
        ttk.Combobox(self.single_tab, textvariable=self.quality_var, values=["highest", "lowest"]).pack()

        # Download Button
        self.download_button = ttk.Button(self.single_tab, text="Download", command=self.start_single_download)
        self.download_button.pack(pady=20)

        # Progress Bar
        self.progress = ttk.Progressbar(self.single_tab, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        # Status Label
        self.status_label = ttk.Label(self.single_tab, text="")
        self.status_label.pack(pady=5)

    def create_batch_tab(self):
        # URL List Entry
        self.batch_label = ttk.Label(self.batch_tab, text="Enter Video URLs (one per line):")
        self.batch_label.pack(pady=10)

        self.batch_text = scrolledtext.ScrolledText(self.batch_tab, width=80, height=10)
        self.batch_text.pack(pady=5)

        # Download Button
        self.batch_download_button = ttk.Button(self.batch_tab, text="Download All", command=self.start_batch_download)
        self.batch_download_button.pack(pady=20)

        # Progress Bar
        self.batch_progress = ttk.Progressbar(self.batch_tab, orient="horizontal", length=400, mode="determinate")
        self.batch_progress.pack(pady=10)

        # Status Label
        self.batch_status_label = ttk.Label(self.batch_tab, text="")
        self.batch_status_label.pack(pady=5)

    def start_single_download(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        Thread(target=self.download_video, args=(url,)).start()

    def start_batch_download(self):
        urls = self.batch_text.get("1.0", tk.END).strip().split("\n")
        if not urls:
            messagebox.showerror("Error", "Please enter at least one URL.")
            return

        Thread(target=self.download_batch, args=(urls,)).start()

    def download_video(self, url):
        try:
            if "youtube.com" in url or "youtu.be" in url:
                self.download_youtube_video(url)
            else:
                self.download_general_video(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download video: {str(e)}")

    def download_youtube_video(self, url):
        try:
            yt = YouTube(url, on_progress_callback=self.update_progress)
            if self.download_option.get() == "video":
                if self.quality_var.get() == "highest":
                    stream = yt.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution()
                else:
                    stream = yt.streams.filter(progressive=True, file_extension="mp4").get_lowest_resolution()
            else:
                stream = yt.streams.filter(only_audio=True).first()

            # Ask user for save location
            save_path = filedialog.asksaveasfilename(
                defaultextension=".mp4",
                filetypes=[("MP4 files", "*.mp4")],
                title="Save Video As"
            )
            if not save_path:
                return  # User canceled

            self.status_label.config(text=f"Downloading: {yt.title}")
            stream.download(output_path=os.path.dirname(save_path), filename=os.path.basename(save_path))
            self.status_label.config(text="Download complete!")
            messagebox.showinfo("Success", "Video downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download YouTube video: {str(e)}")

    def download_general_video(self, url):
        try:
            # Ask user for save location
            save_path = filedialog.asksaveasfilename(
                defaultextension=".mp4",
                filetypes=[("Video files", "*.mp4 *.mkv *.webm")],
                title="Save Video As"
            )
            if not save_path:
                return  # User canceled

            self.status_label.config(text=f"Downloading: {os.path.basename(url)}")
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                total_size = int(response.headers.get("content-length", 0))
                self.progress["maximum"] = total_size
                with open(save_path, "wb") as file:
                    for chunk in tqdm(response.iter_content(chunk_size=1024), total=total_size // 1024, unit="KB"):
                        file.write(chunk)
                        self.progress["value"] += len(chunk)
                self.status_label.config(text="Download complete!")
                messagebox.showinfo("Success", "Video downloaded successfully!")
            else:
                messagebox.showerror("Error", f"Failed to download video. Status code: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download video: {str(e)}")

    def download_batch(self, urls):
        self.batch_progress["maximum"] = len(urls)
        self.batch_progress["value"] = 0

        for i, url in enumerate(urls):
            self.batch_status_label.config(text=f"Downloading {i + 1}/{len(urls)}: {url}")
            self.download_video(url)
            self.batch_progress["value"] += 1

        self.batch_status_label.config(text="Batch download complete!")
        messagebox.showinfo("Success", "All videos downloaded successfully!")

    def update_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        self.progress["value"] = bytes_downloaded

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()
