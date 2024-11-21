import cv2
import numpy as np
from pyzbar.pyzbar import decode, ZBarSymbol

def enhance_image(image):
    """
    Melhora o contraste e brilho da imagem para facilitar a leitura do QR Code.
    """
    # Conversão para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aumentar o brilho da imagem
    # Ajuste o fator de brilho conforme necessário
    brightness = 50
    gray = cv2.convertScaleAbs(gray, alpha=1, beta=brightness)

    # Aplicar equalização do histograma para melhorar contraste
    enhanced = cv2.equalizeHist(gray)

    # Aplicar um filtro de adaptação local para melhorar detalhes
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(enhanced)

    # Realçar bordas (opcional, útil em superfícies escuras)
    edges = cv2.Canny(enhanced, 50, 150)
    enhanced = cv2.addWeighted(enhanced, 0.8, edges, 0.2, 0)

    return enhanced

def read_qrcode_from_camera_pyzbar():
    """
    Lê QR Codes de uma câmera ao vivo com otimizações para superfícies escuras usando pyzbar.
    """
    cap = cv2.VideoCapture(0)  # Altere o índice se necessário para a câmera certa

    if not cap.isOpened():
        print("Erro ao acessar a câmera!")
        return

    print("Pressione 'q' para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha ao capturar quadro.")
            break

        # Melhorar a imagem
        enhanced_frame = enhance_image(frame)

        # Decodificar QR Code e outros tipos de código de barras com pyzbar
        decoded_objects = decode(enhanced_frame, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128, ZBarSymbol.CODE39])
        for obj in decoded_objects:
            # Desenhar retângulo ao redor do QR Code
            points = obj.polygon
            if len(points) == 4:
                pts = np.array(points, dtype=np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

            # Exibir os dados decodificados
            data = obj.data.decode('utf-8')
            print(f"QR Code detectado: {data}")
            cv2.putText(frame, data, (pts[0][0][0], pts[0][0][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Mostrar a imagem original com marcações
        cv2.imshow("QR Code Scanner", frame)

        # Sair ao pressionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def read_qrcode_from_camera_opencv():
    """
    Lê QR Codes usando OpenCV diretamente.
    """
    cap = cv2.VideoCapture(0)  # Altere o índice se necessário para a câmera certa

    if not cap.isOpened():
        print("Erro ao acessar a câmera!")
        return

    print("Pressione 'q' para sair.")

    detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha ao capturar quadro.")
            break

        # Detecta QR Code
        retval, decoded_info, points, straight_qrcode = detector(frame)

        if retval:
            for i in range(len(decoded_info)):
                # Desenhar retângulo ao redor do QR Code
                pts = np.int32(points[i]).reshape(-1, 1, 2)
                cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

                # Exibir os dados decodificados
                data = decoded_info[i]
                print(f"QR Code detectado: {data}")
                cv2.putText(frame, data, (pts[0][0][0], pts[0][0][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Mostrar a imagem original com marcações
        cv2.imshow("QR Code Scanner", frame)

        # Sair ao pressionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Use uma das duas funções para testar a leitura do QR Code
    read_qrcode_from_camera_pyzbar()
    # Ou
    # read_qrcode_from_camera_opencv()
