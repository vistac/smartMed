from flask import Flask, render_template, Response, jsonify
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(1)
port = 5000
host = "0.0.0.0"
DEBUG = True


def gen_frames():
  while True:
    success, frame = camera.read()
    if not success:
      break
    else:
      ret, buffer = cv2.imencode(".jpg", frame)
      frame = buffer.tobytes()
      yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


def get_available_cameras():
  """掃描系統中可用的攝影機索引"""
  available = []
  # 掃描前 5 個索引 (通常電腦不會超過 5 個攝影機)
  for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
      available.append(i)
      cap.release()
  return available


@app.route("/")
def index():
  user_name = "Vistac"
  return render_template("index.html", user_name=user_name)
  # return "<h1>Webcam Stream</h1><img src='/video_feed' width='640'>"
  # return render_template('index.html')


@app.route("/start")
def start_camera():
  global camera
  if camera is None:
    camera = cv2.VideoCapture(0)  # 打開預設攝影機
    return jsonify({"status": "Camera started"})
  return jsonify({"status": "Camera already running"})


@app.route("/stop")
def stop_camera():
  global camera
  if camera is not None:
    camera.release()  # 釋放攝影機資源
    camera = None
    return jsonify({"status": "Camera stopped"})
  return jsonify({"status": "Camera not running"})


@app.route("/video_feed")
def video_feed():
  return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


def main() -> None:
  print("method webcam-app main.")
  app.run(host=host, port=port, debug=DEBUG)


if __name__ == "__main__":
  print("webcam-app entry point.")
  main()
