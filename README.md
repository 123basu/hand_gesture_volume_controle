Hand Gesture Volume Control 

This project allows you to *control system volume using hand gestures* through your webcam.  
It uses *OpenCV, **MediaPipe, and **PyCaw* to detect hand landmarks and adjust volume levels in real time.

How It Works
- *OpenCV* captures video frames from your webcam.  
- *MediaPipe* detects hand landmarks and tracks finger positions.  
- The *distance between thumb and index finger* determines the volume level.  
- *PyCaw* controls the system’s audio endpoint based on that distance.

Requirements

To run this project, you need:
- *Python 3.8 – 3.12* ✅  
  (⚠ MediaPipe does not yet support Python 3.13 or newer.)
