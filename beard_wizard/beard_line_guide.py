import cv2
import mediapipe as mp
import numpy as np
import math

# --- Global Variables for Interactive Editor ---
editor_mode = False
custom_shape_points = []
# Store the last detected landmarks to be accessible by the mouse callback
last_face_landmarks = None

# --- Mouse Callback Function ---
def mouse_callback(event, x, y, flags, param):
    """
    Handles mouse clicks to select landmarks in editor mode.
    """
    global custom_shape_points, last_face_landmarks

    if event == cv2.EVENT_LBUTTONDOWN and editor_mode:
        if last_face_landmarks:
            min_dist = float('inf')
            closest_landmark_idx = -1
            
            h, w, _ = param['frame_shape'] # Get frame shape from params

            # Find the landmark closest to the click
            for idx, lm in enumerate(last_face_landmarks.landmark):
                lx, ly = int(lm.x * w), int(lm.y * h)
                dist = math.hypot(x - lx, y - ly)
                if dist < min_dist:
                    min_dist = dist
                    closest_landmark_idx = idx
            
            # Add the landmark if the click was close enough
            if closest_landmark_idx != -1 and min_dist < 15: # 15 pixel threshold
                if closest_landmark_idx not in custom_shape_points:
                    custom_shape_points.append(closest_landmark_idx)
                    print(f"Added landmark: {closest_landmark_idx}")
                else:
                    print(f"Landmark {closest_landmark_idx} already in list.")
            else:
                print("No landmark close enough to the click.")


# --- Pre-defined Styles (You can replace these with your own) ---
# Using the lists you provided in the last prompt.
LOW_BOXED_BEARD_OUTLINE = [93, 58, 172, 136, 150, 149, 176, 148, 152, 377, 400, 378, 379, 365, 367, 435, 454, 345, 280, 427, 432, 422, 424, 421, 200, 201, 204, 212, 187, 137]
MUSTACHE_OUTLINE = [61, 40, 37, 0, 267, 270, 291, 321, 405, 314, 17, 84, 181, 91, 146]
# NOTE: Your last soul patch list created an unusual shape. I've used a more standard one.
# You can create your own with the editor!
SOUL_PATCH_OUTLINE = [18, 85, 86, 16, 316, 315]

# Start with the Low Boxed style as the default
ACTIVE_STYLE = [LOW_BOXED_BEARD_OUTLINE, MUSTACHE_OUTLINE, SOUL_PATCH_OUTLINE]


def main():
    global editor_mode, custom_shape_points, last_face_landmarks

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    window_name = "Beard Wizard"
    cv2.namedWindow(window_name)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: continue

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            
            # Set the mouse callback with frame shape as a parameter
            cv2.setMouseCallback(window_name, mouse_callback, param={'frame_shape': frame.shape})

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:
                last_face_landmarks = results.multi_face_landmarks[0] # Store for mouse callback
                num_landmarks = len(last_face_landmarks.landmark)

                # --- EDITOR MODE LOGIC (Unchanged) ---
                if editor_mode:
                    for idx, lm in enumerate(last_face_landmarks.landmark):
                        x, y = int(lm.x * w), int(lm.y * h)
                        cv2.putText(frame, str(idx), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255, 255, 0), 1)
                    
                    if len(custom_shape_points) > 1:
                        points_to_draw = []
                        for idx in custom_shape_points:
                            if idx < num_landmarks:
                                lm = last_face_landmarks.landmark[idx]
                                x, y = int(lm.x * w), int(lm.y * h)
                                points_to_draw.append([x, y])
                        
                        points_np = np.array(points_to_draw, np.int32)
                        cv2.polylines(frame, [points_np], isClosed=False, color=(0, 255, 0), thickness=2)

                # --- NORMAL MODE LOGIC (WITH OCCLUSION) ---
                else:
                    # Define a threshold for how far back a point can be to be visible.
                    # Positive 'z' values are further away. Adjust this if lines disappear too soon/late.
                    Z_THRESHOLD = 0.04 

                    for shape_indices in ACTIVE_STYLE:
                        # Loop through the indices to draw line segments one by one
                        for i in range(len(shape_indices)):
                            # Get the current point and the next point in the list.
                            # The modulo operator (%) makes the list wrap around, connecting the last point to the first.
                            p1_idx = shape_indices[i]
                            p2_idx = shape_indices[(i + 1) % len(shape_indices)]

                            # Safety check for index validity
                            if p1_idx < num_landmarks and p2_idx < num_landmarks:
                                p1 = last_face_landmarks.landmark[p1_idx]
                                p2 = last_face_landmarks.landmark[p2_idx]

                                # *** THE OCCLUSION CHECK ***
                                # Only draw the line if both points are in front of the Z threshold.
                                if p1.z < Z_THRESHOLD and p2.z < Z_THRESHOLD:
                                    # Get 2D coordinates for drawing
                                    p1_x, p1_y = int(p1.x * w), int(p1.y * h)
                                    p2_x, p2_y = int(p2.x * w), int(p2.y * h)
                                    
                                    # Draw the line segment
                                    cv2.line(frame, (p1_x, p1_y), (p2_x, p2_y), (0, 255, 255), 2)
            
            # --- DISPLAY INSTRUCTIONS ---
            y_offset = 30
            if editor_mode:
                cv2.putText(frame, "EDITOR MODE", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, "Click landmarks to add points", (10, y_offset + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(frame, "C: Clear | U: Undo | S: Save to Console", (10, y_offset + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            else:
                cv2.putText(frame, "Style: Custom", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.putText(frame, "E: Toggle Editor | Q: Quit", (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.imshow(window_name, frame)

            # --- KEYBOARD CONTROLS ---
            key = cv2.waitKey(5) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('e'):
                editor_mode = not editor_mode
                print(f"Editor mode {'ON' if editor_mode else 'OFF'}")
            elif key == ord('c') and editor_mode:
                custom_shape_points.clear()
                print("Cleared custom shape.")
            elif key == ord('u') and editor_mode:
                if custom_shape_points:
                    removed = custom_shape_points.pop()
                    print(f"Removed last landmark: {removed}")
            elif key == ord('s') and editor_mode:
                print("\n--- Your Custom Shape List ---")
                print(custom_shape_points)
                print("--- Copy the list above and paste it into the code ---\n")

    finally:
        print("Shutting down...")
        cap.release()
        cv2.destroyAllWindows()
        face_mesh.close()

if __name__ == '__main__':
    main()