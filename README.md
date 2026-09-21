# PixelShelf

**A 2D game asset catalog and web-based sprite previewer for creators.**

PixelShelf is a dedicated web platform for indie game developers and pixel artists to organize, tag, and preview 2D game assets. Whether you are assembling tilesets for a museum-themed 2D platformer or keeping track of complex character animations, PixelShelf centralizes your collections with clear metadata so project files stay organized. 

Users can upload spritesheets, document their grid dimensions, and run a simple in-browser animation preview before importing files into a game engine.

## The Problem

Student game developers and 2D artists often lose track of sprite files across scattered local folders. Furthermore, they lack a quick way to test animation loops without booting up heavy game engines. Standard art portfolio websites display only static images, making it difficult to verify how a spritesheet moves in motion. PixelShelf provides a lightweight web organizer with an integrated animation viewer built specifically for 2D sprites.

## Features

* **Asset Manager & Uploader:** Upload 2D image files (PNG/GIF) up to 10MB. Tag your assets with metadata such as frame size, author, category (characters, tilesets, UI), and license type.
* **Interactive Sprite Animator:** A custom HTML5 Canvas widget where users can enter frame width/height to view a looping animation preview with play/pause controls.
* **Background Contrast Tester:** Switch the canvas backdrop between light, dark, and transparent checkerboards to test sprite edge clarity and readability.
* **Dashboard & Collections:** View recent uploads, total asset counts, and organize private asset libraries and project collections.
* **User Profiles:** Showcase a portfolio of public assets and quick stats on uploaded spritesheets.
* **Secure Authentication:** Full register, login, and logout functionality to keep private assets secure.

## Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite 
* **Frontend:** HTML, CSS, JavaScript (HTML5 Canvas API for the Sprite Animator)

## Project Limitations

To keep the application lightweight and focused on its core objective, PixelShelf adheres to the following constraints:
* **No Built-in Drawing Editor:** The app is purely for organizing and previewing assets; users cannot draw or edit pixel art within the browser.
* **2D Raster Files Only:** Support is restricted to standard PNG and GIF formats. 3D models and audio files are not supported.
* **No Engine Auto-Export:** The system does not generate engine-specific scripts (e.g., Unity ScriptableObjects or Godot scene files). It provides direct file downloads.
* **File Upload Size Limit:** Individual asset uploads are capped at a maximum of 10MB to maintain efficient server storage.
