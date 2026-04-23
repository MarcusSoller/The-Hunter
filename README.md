# The-Hunter
A Python-based 2D survival game featuring character selection, asset path optimization for standalone distribution, and milestone-triggered boss encounters.

Key Technical Features
1. Robust Path Handling (resource_path)
One of the most critical engineering choices in this project is the resource_path function. It ensures that all assets (images/sounds) are correctly located whether the game is running as a script or as a packaged standalone .exe using PyInstaller.

2. State-Based Game Flow
The game utilizes a state machine (SELECT and GAME states) to manage transitions.

SELECT: A character selection screen with collision-detecting buttons.

GAME: The core survival loop with dynamic enemy spawning and score-based boss triggers.

3. Dynamic Enemy & Boss Logic
Ostrich Mob AI: Enemies automatically track the player's coordinates and rotate their sprites to face the player using math.atan2 for precise directional visuals.

Lion Boss System: Features a custom HP bar and milestone-based spawning (every 20 points), adding a layer of progression to the arcade gameplay.

4. Animation & Audio Systems
Frame Toggling: Implemented a frame-switching timer for character and enemy animations to create visual movement.

Multi-Channel Audio: Managed background music and sound effects (footsteps, shooting, and enemy growls) across different Pygame mixer channels to prevent audio clipping.

Tech Stack
Language: Python

Graphics: Pygame (Sprite rotation, alpha-blending overlays)

Assets: Custom images (MediBang Paint) and localized sound effects.

Controls
WASD: Move and Aim (Snaps to 4-way direction)

Space: Shoot Arrow

R: Restart (Resetting all game variables and timers)
