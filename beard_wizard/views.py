from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

# def trimm(request):
    
#     return render(request, 'trimming_guide.html')

def virtual(request):
    return render(request, 'virtual_try_on.html')

def ai(request):
    return render(request, 'ai_analysis.html')

from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2
import mediapipe as mp
import time
import numpy as np

# --- BEARD STYLE DEFINITIONS ---
# All your landmark lists are now in a single dictionary.
BEARD_STYLES = {
    'low_boxed': [
        [93, 58, 172, 136, 150, 149, 176, 148, 152, 377, 400, 378, 379, 365, 367, 435, 454, 345, 280, 427, 432, 422, 424, 421, 200, 201, 204, 212, 187, 137],
        [61, 40, 37, 0, 267, 270, 291, 321, 405, 314, 17, 84, 181, 91, 146],
        [18, 85, 86, 16, 316, 315]
    ],
    'full_beard': [
        [127, 234, 93, 132, 58, 172, 136, 150, 149, 176, 148, 152, 377, 400, 378, 379, 365, 397, 288, 361, 323, 454, 356],
        [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 321, 405, 314, 17, 84, 181, 91, 146]
    ],
    'brett': [
        [215, 138, 135, 210, 211, 32, 208, 199, 428, 262, 431, 430, 366, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 215]
    ],
    'classic_full': [
        [93, 137, 215, 58, 172, 136, 150, 149, 176, 148, 152, 377, 400, 378, 379, 365, 397, 288, 366, 447, 352, 411, 427, 436, 322, 393, 164, 167, 165, 216, 187, 123, 93],
        [201, 83, 84, 17, 314, 313, 421, 418, 424, 422, 287, 321, 405, 314, 17, 84, 181, 91, 146, 57, 202, 204, 194, 201]
    ],
    # NEW STYLE ADDED HERE
    'goatee_mustach': [
        [216, 92, 165, 167, 164, 393, 391, 322, 432, 430, 394, 379, 378, 400, 377, 152, 148, 176, 149, 150, 169, 214, 216],
        [201, 83, 84, 17, 314, 313, 421, 418, 424, 422, 287, 267, 0, 37, 39, 40, 57, 202, 204, 194, 201]
    ]
}

def stream_generator(style_name='low_boxed'):
    """Video streaming generator function."""
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    cap = cv2.VideoCapture(0)
    
    # Select the active style based on the style_name parameter
    active_style = BEARD_STYLES.get(style_name, BEARD_STYLES['low_boxed']) # Default to low_boxed if name is invalid

    while True:
        success, frame = cap.read()
        if not success:
            placeholder = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(placeholder, "Camera Error", (180, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            ret, buffer = cv2.imencode('.jpg', placeholder)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(1)
            continue

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0]
            num_landmarks = len(landmarks.landmark)
            Z_THRESHOLD = 0.04

            for shape_indices in active_style:
                for i in range(len(shape_indices)):
                    p1_idx = shape_indices[i]
                    p2_idx = shape_indices[(i + 1) % len(shape_indices)]

                    if p1_idx < num_landmarks and p2_idx < num_landmarks:
                        p1 = landmarks.landmark[p1_idx]
                        p2 = landmarks.landmark[p2_idx]

                        if p1.z < Z_THRESHOLD and p2.z < Z_THRESHOLD:
                            p1_x, p1_y = int(p1.x * w), int(p1.y * h)
                            p2_x, p2_y = int(p2.x * w), int(p2.y * h)
                            cv2.line(frame, (p1_x, p1_y), (p2_x, p2_y), (0, 255, 255), 2)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

def video_feed_view(request, style_name):
    """Video streaming route that takes a style name."""
    return StreamingHttpResponse(stream_generator(style_name),
                                 content_type='multipart/x-mixed-replace; boundary=frame')



def trimm(request):
    context = {
        'style_names': BEARD_STYLES.keys()
    }
    return render(request, 'trimming_guide.html', context)


# import cv2
# import mediapipe as mp
# import numpy as np
# import math
# from django.shortcuts import render
# from django.http import StreamingHttpResponse

# # --- Helper Function for Overlaying an Image ---
# def overlay_transparent(background_img, foreground_img, x, y):
#     """Overlays a transparent PNG image on a background image."""
#     try:
#         bg_h, bg_w, _ = background_img.shape
#         fg_h, fg_w, _ = foreground_img.shape
#         if x >= bg_w or y >= bg_h or x + fg_w <= 0 or y + fg_h <= 0: return background_img
#         roi_x1, roi_y1 = max(x, 0), max(y, 0)
#         roi_x2, roi_y2 = min(x + fg_w, bg_w), min(y + fg_h, bg_h)
#         fg_crop = foreground_img[roi_y1-y:roi_y2-y, roi_x1-x:roi_x2-x]
#         alpha = fg_crop[:, :, 3] / 255.0
#         inverse_alpha = 1.0 - alpha
#         roi = background_img[roi_y1:roi_y2, roi_x1:roi_x2]
#         for c in range(3):
#             roi[:, :, c] = (alpha * fg_crop[:, :, c] + inverse_alpha * roi[:, :, c])
#         return background_img
#     except Exception:
#         return background_img

# # --- Pre-load all beard images into memory for efficiency ---
# # Make sure these images are in your 'static/assets/' folder
# BEARD_IMAGES = {
#     'balbo': cv2.imread('static/assets/balbo.png', cv2.IMREAD_UNCHANGED),
#     'van_dyke': cv2.imread('static/assets/van_dyke.png', cv2.IMREAD_UNCHANGED),
#     'goatee': cv2.imread('static/assets/goatee.png', cv2.IMREAD_UNCHANGED),
#     'none': None # Special case for no filter
# }

# def stream_generator(style_name='balbo'):
#     """Video streaming generator function with image overlay."""
#     mp_face_mesh = mp.solutions.face_mesh
#     face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
#     cap = cv2.VideoCapture(0)
    
#     # Get the selected pre-loaded image from the dictionary
#     filter_img = BEARD_IMAGES.get(style_name)

#     while True:
#         success, frame = cap.read()
#         if not success:
#             break

#         frame = cv2.flip(frame, 1) # Flip for a mirror effect
        
#         # If a valid filter is selected, process the frame
#         if filter_img is not None:
#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             results = face_mesh.process(rgb_frame)

#             if results.multi_face_landmarks:
#                 for face_landmarks in results.multi_face_landmarks:
#                     # --- Image Overlay Logic ---
#                     landmarks = face_landmarks.landmark
#                     chin_bottom, left_jaw, right_jaw, nose_bridge = landmarks[152], landmarks[288], landmarks[58], landmarks[168]
#                     h, w, _ = frame.shape
#                     chin_pt = (int(chin_bottom.x * w), int(chin_bottom.y * h))
#                     left_jaw_pt = (int(left_jaw.x * w), int(left_jaw.y * h))
#                     right_jaw_pt = (int(right_jaw.x * w), int(right_jaw.y * h))
#                     nose_pt = (int(nose_bridge.x * w), int(nose_bridge.y * h))

#                     filter_width = int(math.dist(left_jaw_pt, right_jaw_pt) * 1.4)
#                     filter_height = int(filter_width / (filter_img.shape[1] / filter_img.shape[0]))
#                     resized_filter = cv2.resize(filter_img, (filter_width, filter_height))
                    
#                     dx = chin_pt[0] - nose_pt[0]
#                     dy = chin_pt[1] - nose_pt[1]
#                     angle = math.degrees(math.atan2(dy, dx)) - 90
                    
#                     center = (filter_width // 2, filter_height // 2)
#                     rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
#                     rotated_filter = cv2.warpAffine(resized_filter, rotation_matrix, (filter_width, filter_height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
                    
#                     x_pos = chin_pt[0] - (filter_width // 2)
#                     y_pos = chin_pt[1] - (filter_height // 2) - 10
#                     frame = overlay_transparent(frame, rotated_filter, x_pos, y_pos)

#         # Encode the final frame (either processed or original) to JPEG
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()

#         # Yield the frame in the multipart format
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#     cap.release()

# def video_feed_view(request, style_name):
#     """This view streams the video feed by calling the generator."""
#     return StreamingHttpResponse(stream_generator(style_name),
#                                  content_type='multipart/x-mixed-replace; boundary=frame')

# def try_on_page(request):
#     """This view renders the main HTML page and passes the style names."""
#     context = {
#         'style_names': BEARD_IMAGES.keys()
#     }
#     return render(request, 'try_on.html', context)