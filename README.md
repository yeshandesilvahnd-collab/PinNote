# PinNote 📌

A minimalist, modern, floating sticky note widget for Windows featuring continuous reboot persistence, an Always-on-Top toggle, rich text & table formatting, and Dark/Light mode switching.

---

## ✨ What's New & Key Features

1. **Title Bar Pin Control (📌)**:
   - Positioned in the window controls cluster: **`[ 📌 Pin ]  [ — Minimize ]  [ □ Maximize ]  [ ✕ Close ]`**.
   - One click toggles **Always-on-Top**. When pinned, it glows with an active royal blue accent and stays floating above all other windows (browser, games, IDE, etc.).
   - Shortcut: `Ctrl + P`.

2. **Rich Text & Table Formatting**:
   - **Tables from Gemini / Word / Excel**: Copy any table from Gemini, Microsoft Word, Excel, or web pages and paste it directly (`Ctrl + V`). It automatically renders as a formatted table with crisp borders, header styling, and rows!
   - **Markdown Table Support**: If you copy a raw markdown table (`| Col 1 | Col 2 |`), PinNote detects and converts it into a visual table.
   - **Insert Table**: Right-click anywhere in the editor and choose **📊 Insert Table...** to insert custom rows and columns.
   - **Formatting Shortcuts**:
     - `Ctrl + B`: Bold
     - `Ctrl + I`: Italic
     - `Ctrl + U`: Underline

3. **Dark Mode & Light Mode Switch (☀️ / 🌙)**:
   - Click the theme toggle button in the top bar to instantly switch between:
     - **🌙 Dark Mode**: Obsidian/Zinc dark palette with high-contrast text and sleek borders.
     - **☀️ Light Mode**: Clean, crisp modern white/slate theme.
   - Your theme choice is preserved across reboots.

4. **Continuous Reboot Persistence**:
   - Everything (rich HTML, tables, plain text, window position, pin state, font size, and theme) is auto-saved on every change to `~/.pinnote/data.json`.
   - **Start on boot**: Toggle the checkbox in the bottom bar to have PinNote silently launch and reopen your note whenever your PC starts up.

5. **Instant Actions & Undo**:
   - **📋 Copy**: One-click copy with toast feedback.
   - **🗑️ Clear with Undo**: Clears the note and presents an inline `↺ Undo` banner for 6 seconds to restore your note with one click.
   - **A- / A+**: Font size scaler.
   - **Live Counter**: Live word and character count in the footer.
   - **Resize**: Resizable from the bottom-right corner grip.

---

## 🚀 How to Launch PinNote

- **Desktop Shortcut**: Double-click **PinNote** on your Desktop.
- **Silent Launcher**: Double-click [`PinNote.vbs`](file:///C:/Users/Yesha/.gemini/antigravity/scratch/pin_note/PinNote.vbs).
- **Batch Launcher**: Double-click [`PinNote.bat`](file:///C:/Users/Yesha/.gemini/antigravity/scratch/pin_note/PinNote.bat).
- **From Terminal**:
  ```powershell
  python C:\Users\Yesha\.gemini\antigravity\scratch\pin_note\pin_note.py
  ```

---

## ⌨️ Shortcuts Reference

| Shortcut | Description |
| :--- | :--- |
| `Ctrl + P` | Toggle Always-on-Top |
| `Ctrl + S` | Manual Save confirmation |
| `Ctrl + B` | Bold text |
| `Ctrl + I` | Italic text |
| `Ctrl + U` | Underline text |
| `Ctrl + +` / `Ctrl + =` | Increase font size |
| `Ctrl + -` | Decrease font size |
| `Right Click` | Context menu (Insert Table, Cut, Copy, Paste, Clear) |
