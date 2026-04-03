from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(1)
port = 5000
host = '0.0.0.0'


def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    user_name = "Vistac"
    return render_template('index.html', user_name=user_name)
    # return "<h1>Webcam Stream</h1><img src='/video_feed' width='640'>"
    # return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def main() -> None:
    print('method webcam-app main.')
    app.run(host=host, port=port)


if __name__ == '__main__':
    print('webcam-app entry point.')
    main()
