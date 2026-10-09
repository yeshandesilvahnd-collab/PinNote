# PinNote 📌

A minimalist, modern, floating sticky note widget for **Windows** and **macOS** featuring continuous reboot persistence, Always-on-Top pinning, rich text & table formatting, dark/light themes, and smart auto-transparency when idle.

---

## ✨ Features

1. **Title Bar Pin Control (📌)**:
   - Floating cluster: `[ 📌 Pin ]  [ — Minimize ]  [ □ Maximize ]  [ ✕ Close ]`.
   - One click toggles **Always-on-Top**. Active royal blue indicator ensures it floats above IDEs, browsers, and full-screen apps.
   - Shortcut: `Ctrl + P` (or `Cmd + P` on macOS).

2. **👻 Auto-Transparency When Idle (New in v1.1)**:
   - Automatically and smoothly fades the window to your chosen opacity (e.g. 50%) when inactive, keeping your workspace uncluttered while your notes remain visible.
   - Instantly snaps back to full 100% opacity the moment you move your mouse, click, scroll, or type.
   - Configurable timeout down to **5 seconds** (5s, 15s, 30s, 45s, 1m, 2m, 3m, 5m, 10m).
   - Adjustable idle opacity levels (20% – 80%).

3. **⚙️ Compact Settings Menu (New in v1.1)**:
   - Clean, modern context popup menu styled after Windows 11 / Edge design language.
   - One-click toggle for **Auto-transparency when idle**.
   - Submenu to choose **Runout time** (5 seconds to 10 minutes).
   - Submenu to select **Idle opacity** (20% to 80%).
   - One-click toggle for **Start on Windows / macOS boot**.

4. **Rich Text & Table Formatting**:
   - **Tables from Gemini, Word & Excel**: Copy tables from web pages, Gemini, Word, or Excel and paste (`Ctrl + V`) directly. Renders with crisp borders, header styling, and alternating rows.
   - **Markdown Table Support**: Automatically detects and converts raw markdown tables (`| Col 1 | Col 2 |`).
   - **Insert Table**: Right-click anywhere in the editor and choose **📊 Insert Table...** to specify custom rows and columns.
   - Standard shortcuts: `Ctrl + B` (Bold), `Ctrl + I` (Italic), `Ctrl + U` (Underline).

5. **📸 Screenshots, Images & Draggable Resizing (New)**:
   - **Interactive 4-Pointer Resize Handles**: Click any image or screenshot in your note to display MS Office-style corner pointers! Drag any pointer handle to smoothly resize the image with preserved aspect ratio and live pixel dimension feedback.
   - **Quick Resize Presets**: Right-click any image to quickly pick "Fit Note Width", "Reset to Standard", "75% Size", or "50% Size".
   - **Delete Image**: Press `Delete` or `Backspace` while an image is selected, or right-click and select "🗑️ Delete Image".
   - **Paste Screenshots (`Ctrl + V`)**: Copy any screenshot from Snipping Tool (`Win + Shift + S`), PrintScreen, web browser, or File Explorer and paste it directly into your note! Automatically rendered with responsive scaling and preserved across reboots.
   - **📸 Copy Note as Screenshot (`Ctrl + Shift + C` / `Cmd + Shift + C`)**: Right-click and choose "Copy Note as Screenshot" to capture your styled note as a clean image card to the clipboard — ready to paste into Discord, WhatsApp, Slack, or emails.
   - **Multi-Format Note Copy**: Clicking the Copy button (`📋`) copies formatted text, HTML, and attaches embedded screenshots to the clipboard.
   - **Save & Copy Specific Images**: Right-click any image in the note to copy it or save it to disk.
   - **Insert Image**: Right-click and select "🖼️ Insert Image..." to pick an image from your computer.

6. **Dark Mode & Light Mode (☀️ / 🌙)**:
   - Seamless one-click switch between Obsidian dark theme and crisp white light theme.
   - Preserves theme preference across reboots.

7. **Continuous Persistence & Autostart**:
   - Everything (rich HTML, tables, screenshots, window position, pin state, font size, theme, and idle preferences) auto-saves continuously to `~/.pinnote/data.json`.
   - Optional silent autostart on boot (Windows VBScript launcher / macOS LaunchAgent).

8. **Instant Actions & Undo**:
   - **📋 Copy**: One-click multi-format copy with toast feedback.
   - **🗑️ Clear with Undo**: Clears the note with a 6-second inline `↺ Undo` toast banner to restore your work with one click.
   - **A- / A+**: Real-time font size scaler with clean footer alignment.
   - **Live Counter**: Live word and character count in the footer.
   - **Resize Grip**: Smooth corner resizing.

---

## 🚀 Installation & Downloads

### Windows
1. Head to the **[Releases](https://github.com/yeshandesilvahnd-collab/PinNote/releases)** tab.
2. Download **`PinNote-Setup-v1.1.2.exe`** (or `PinNote-v1.1.2-Package.zip`).
3. Run the installer and choose whether to start PinNote automatically on boot.

### macOS
1. Download **`PinNote-macOS-Package.zip`** from Releases.
2. Unzip and double-click **`run_mac.command`**, or compile a native `.app` / `.dmg` using `./build_mac.sh`.

---

## ⌨️ Shortcuts Reference

| Windows | macOS | Description |
| :--- | :--- | :--- |
| `Ctrl + P` | `Cmd + P` | Toggle Always-on-Top |
| `Ctrl + S` | `Cmd + S` | Manual Save confirmation |
| `Ctrl + B` | `Cmd + B` | Bold text |
| `Ctrl + I` | `Cmd + I` | Italic text |
| `Ctrl + U` | `Cmd + U` | Underline text |
| `Ctrl + +` / `Ctrl + =` | `Cmd + +` | Increase font size |
| `Ctrl + -` | `Cmd + -` | Decrease font size |
| `Ctrl + Shift + C` | `Cmd + Shift + C` | Copy Note as Screenshot / Image |
| `Right Click` | `Right Click` | Context menu (Insert Table, Screenshot, Insert Image) |

---

## 🛠️ Running From Source

```bash
# Clone the repository
git clone https://github.com/<your-username>/PinNote.git
cd PinNote

# Install dependencies
pip install -r requirements.txt

# Run PinNote
python pin_note.py
```

---

## 📜 License
MIT License. See [LICENSE](LICENSE) for details.
