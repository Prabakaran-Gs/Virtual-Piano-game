<body>

<h1>Hand Tracking Piano with OpenCV, Mediapipe, and Pygame</h1>

<h2>Overview</h2>

<p>This Python script utilizes OpenCV, Mediapipe, and Pygame to create a simple hand-tracking piano application. The program captures video from the default camera, detects hand landmarks using the Mediapipe library, and triggers piano sounds through Pygame based on hand positions.</p>

<h2>Dependencies</h2>

<ul>
    <li>OpenCV: Used for capturing and processing video frames.</li>
    <li>Mediapipe: Employs the hands module for hand landmark detection.</li>
    <li>Pygame: Enables the playback of piano sounds.</li>
</ul>

<p>Install the required libraries using the following commands:</p>

<pre>
<code>pip install opencv-python
pip install mediapipe
pip install pygame
</code></pre>

<h2>Usage</h2>

<ol>
    <li>Make sure you have a working camera connected to your system.</li>
    <li>Run the script by executing the following command:</li>
</ol>

<pre>
<code>python virtual_keyboard.py
</code></pre>

<p>A window will appear displaying the live camera feed with hand tracking and piano keys drawn on it.</p>

<p>Play the piano by hovering your hand over the corresponding virtual keys. The keys are mapped to the C4 to B4 notes.</p>

<p>Press 'q' to exit the application.</p>

<h2>Configuration</h2>

<ul>
    <li>You can uncomment the lines that set the frame width and height if needed:</li>
</ul>

<pre>
<code># cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
</code></pre>

<p>Customize the sound files (<code>sound_files</code>) to use your preferred piano notes in MP3 format.</p>

<h2>Piano Key Positions</h2>

<p>The script defines the positions of the virtual piano keys on the video frame. You can adjust these positions in the <code>piano_keys</code> list based on your preferences or the dimensions of your video feed.</p>

<h2>Acknowledgments</h2>

<ul>
    <li>The script uses the Mediapipe library for hand tracking. More information about Mediapipe can be found <a
            href="https://google.github.io/mediapipe/solutions/hands">here</a>.</li>
    <li>Pygame is utilized for playing piano sounds. You can find Pygame documentation <a
            href="https://www.pygame.org/">here</a>.</li>
</ul>

<h2>License</h2>

<p>This project is licensed under the <a href="LICENSE">MIT License</a>. Feel free to modify and distribute it according to the terms of the license.</p>

<p>Feel free to contact the author for any questions or improvements.</p>

</body>
