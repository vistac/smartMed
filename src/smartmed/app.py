from flask import Flask, render_template, Response, jsonify, request
from pygrabber.dshow_graph import FilterGraph
import cv2
import threading

app = Flask(__name__)
camera = cv2.VideoCapture(1)
port = 5000
host = "0.0.0.0"
DEBUG = True
camera = None
camera_lock = threading.Lock()


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
  """使用 pygrabber 獲取 Windows 攝影機名稱"""
  try:
    devices = FilterGraph().get_input_devices()
    return [{"id": i, "name": name} for i, name in enumerate(devices)]
  except Exception:
    return []


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/list")
def list_cameras():
  return jsonify({"cameras": get_available_cameras()})


@app.route("/start")
def start_camera():
  global camera
  device_id = request.args.get("device_id", default=0, type=int)

  with camera_lock:
    if camera is not None:
      # 如果已經有開啟的攝影機，先釋放舊的
      camera.release()
      camera = None

    try:
      # 建立新的攝影機實例
      new_cam = cv2.VideoCapture(device_id, cv2.CAP_DSHOW)  # 使用 DSHOW 在 Windows 更快
      if not new_cam.isOpened():
        return jsonify({"status": "error", "message": "無法開啟攝影機"}), 500

      camera = new_cam
      return jsonify({"status": "started", "device_id": device_id})
    except Exception as e:
      return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/stop")
def stop_camera():
  global camera
  with camera_lock:
    if camera is not None:
      camera.release()
      camera = None
      return jsonify({"status": "stopped"})
    return jsonify({"status": "already stopped"})


@app.route("/video_feed")
def video_feed():
  def generate_frames():
    global camera
    while True:
      with camera_lock:
        if camera is None or not camera.isOpened():
          break
        success, frame = camera.read()

      if not success:
        break

      ret, buffer = cv2.imencode(".jpg", frame)
      if not ret:
        continue

      yield (
        b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
      )

  return Response(
    generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
  )


def main() -> None:
  print("method webcam-app main.")
  app.run(host=host, port=port, debug=DEBUG)


if __name__ == "__main__":
  print("webcam-app entry point.")
  main()
