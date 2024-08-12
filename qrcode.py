import cv2
import numpy as np
import pyperclip

def generate_ascii_qr(image_path, scale_factor, ascii_char='#'):
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"Error: Cannot load image at {image_path}")
        return

    detector = cv2.QRCodeDetector()
    retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(img)

    if not retval or points is None or len(points) < 1 or len(points[0]) < 4:
        print("QR code not detected or insufficient points detected.")
        return
    
    straight_qrcode = straight_qrcode[0]  # 読み取ったQRコードの画像を取得
    qr_height, qr_width = straight_qrcode.shape  # QRコードのサイズを取得

    # スケーリングのために、新しいサイズを設定
    scaled_height = qr_height * scale_factor
    scaled_width = qr_width * scale_factor

    # スケーリング後のQRコード画像を初期化
    scaled_qr = np.zeros((scaled_height, scaled_width), dtype=np.uint8)

    # スケーリングの処理
    for y in range(qr_height):
        for x in range(qr_width):
            if straight_qrcode[y, x] < 128:
                # スケーリングファクターに基づいてアスキー文字を表示
                scaled_qr[y*scale_factor:(y+1)*scale_factor, x*scale_factor:(x+1)*scale_factor] = 0
            else:
                scaled_qr[y*scale_factor:(y+1)*scale_factor, x*scale_factor:(x+1)*scale_factor] = 255

    # QRコードをアスキーアートに変換
    qr_ascii_art = ''
    for y in range(scaled_height):
        for x in range(scaled_width):
            qr_ascii_art += ascii_char if scaled_qr[y, x] == 0 else ' '
        qr_ascii_art += '\n'

    # クリップボードにコピー
    pyperclip.copy(qr_ascii_art)

    print("QR code ASCII art copied to clipboard:")
    print(qr_ascii_art)

# プロンプトからファイル名と倍率を取得
image_path = input("Enter the QR code image file name (default: qrcode.png): ") or 'qrcode.png'
scale_factor = int(input("Enter the scale factor (default: 1): ") or 1)

generate_ascii_qr(image_path, scale_factor, ascii_char='@')
