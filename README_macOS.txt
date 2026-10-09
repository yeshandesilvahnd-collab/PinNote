PinNote for macOS
==================

Option 1: Run Directly (No compiling needed)
--------------------------------------------
1. Double-click "run_mac.command".
2. If macOS blocks it on first run, Right-click -> Open.
3. It will set up the environment and launch PinNote.


Option 2: Build Native macOS App & DMG Installer
------------------------------------------------
1. Open Terminal in this folder.
2. Run:
     chmod +x build_mac.sh
     ./build_mac.sh
3. Once completed:
   - "dist/PinNote.app" is created.
   - "dist/PinNote-v1.0.dmg" is created (ready to drag into Applications).


Features on macOS:
------------------
- Native Apple typography (San Francisco font)
- Cmd+S, Cmd+B, Cmd+I, Cmd+U, Cmd++, Cmd+- shortcuts
- Always-on-top pinning
- LaunchAgent reboot persistence (~/Library/LaunchAgents/com.pinnote.app.plist)
- Dark and Light mode
- HTML and Markdown table support
