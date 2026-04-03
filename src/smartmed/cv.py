import cv2


def openCamera() -> None:
  cap = cv2.VideoCapture(1)
  if not cap.isOpened():
    print("錯誤：無法開啟攝影機")
    exit()
  print("按下 'q' 鍵退出程式")

  while True:
    # 逐幀擷取畫面
    ret, frame = cap.read()

    if not ret:
      print("無法接收畫面，正在退出...")
      break

    # 在視窗中顯示畫面
    cv2.imshow("UV Webcam Test", frame)

    # 偵測鍵盤輸入，按下 'q' 停止
    if cv2.waitKey(1) & 0xFF == ord("q"):
      break

  # 釋放資源並關閉視窗
  cap.release()
  cv2.destroyAllWindows()
