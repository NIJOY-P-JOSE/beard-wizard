import cv2
import mediapipe as mp
import numpy as np
import math
import base64
import json
from channels.generic.websocket import WebsocketConsumer

# --- Helper Function for Overlaying ---
def overlay_transparent(background_img, foreground_img, x, y):
    try:
        bg_h, bg_w, _ = background_img.shape
        fg_h, fg_w, _ = foreground_img.shape
        if x >= bg_w or y >= bg_h or x + fg_w <= 0 or y + fg_h <= 0: return background_img
        roi_x1, roi_y1 = max(x, 0), max(y, 0)
        roi_x2, roi_y2 = min(x + fg_w, bg_w), min(y + fg_h, bg_h)
        fg_crop = foreground_img[roi_y1-y:roi_y2-y, roi_x1-x:roi_x2-x]
        alpha = fg_crop[:, :, 3] / 255.0
        inverse_alpha = 1.0 - alpha
        roi = background_img[roi_y1:roi_y2, roi_x1:roi_x2]
        for c in range(0, 3):
            roi[:, :, c] = (alpha * fg_crop[:, :, c] + inverse_alpha * roi[:, :, c])
        return background_img
    except Exception:
        return background_img

# --- Main WebSocket Consumer Class ---
class FilterConsumer(WebsocketConsumer):
    def connect(self):
        # Initialize MediaPipe and load filter images when a user connects
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.filter_images = {
            'balbo': cv2.imread('static/assets/balbo.png', cv2.IMREAD_UNCHANGED),
            'van_dyke': cv2.imread('static/assets/van_dyke.png', cv2.IMREAD_UNCHANGED),
            'goatee': cv2.imread('static/assets/goatee.png', cv2.IMREAD_UNCHANGED),
        }
        self.accept()
        print("WebSocket Connected")

    def disconnect(self, close_code):
        self.face_mesh.close()
        print("WebSocket Disconnected")

    def receive(self, text_data):
        # This method is called whenever a message is received from the client
        data = json.loads(text_data)
        image_data = data['image']
        style_name = data.get('style', 'balbo') # Default to 'balbo' if no style is sent

        # Decode the base64 image
        img_bytes = base64.b64decode(image_data.split(',')[1])
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # --- MediaPipe and OpenCV Processing Logic ---
        filter_img = self.filter_images.get(style_name)
        if filter_img is None:
            # If style is 'none' or invalid, send the original frame back
            _, buffer = cv2.imencode('.jpg', frame)
            self.send(text_data=base64.b64encode(buffer).decode('utf-8'))
            return

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmarks = face_landmarks.landmark
                chin_bottom, left_jaw, right_jaw, nose_bridge = landmarks[152], landmarks[288], landmarks[58], landmarks[168]
                h, w, _ = frame.shape
                chin_pt = (int(chin_bottom.x * w), int(chin_bottom.y * h))
                left_jaw_pt = (int(left_jaw.x * w), int(left_jaw.y * h))
                right_jaw_pt = (int(right_jaw.x * w), int(right_jaw.y * h))
                nose_pt = (int(nose_bridge.x * w), int(nose_bridge.y * h))

                filter_width = int(math.dist(left_jaw_pt, right_jaw_pt) * 1.4)
                filter_height = int(filter_width / (filter_img.shape[1] / filter_img.shape[0]))
                resized_filter = cv2.resize(filter_img, (filter_width, filter_height))
                
                dx = chin_pt[0] - nose_pt[0]
                dy = chin_pt[1] - nose_pt[1]
                angle = math.degrees(math.atan2(dy, dx)) - 90
                
                center = (filter_width // 2, filter_height // 2)
                rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
                rotated_filter = cv2.warpAffine(resized_filter, rotation_matrix, (filter_width, filter_height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
                
                x_pos = chin_pt[0] - (filter_width // 2)
                y_pos = chin_pt[1] - (filter_height // 2) - 10
                frame = overlay_transparent(frame, rotated_filter, x_pos, y_pos)

        # Encode the processed frame back to base64
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        # Send the processed frame back to the client
        self.send(text_data=jpg_as_text)