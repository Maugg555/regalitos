import cv2
from playsound import playsound

bd = cv2.barcode_BarcodeDetector()
cap = cv2.VideoCapture(0)

detecciones = {}

while True:
    ret, frame = cap.read()
    if ret:
        ret_bc, decode, puntos = bd.detectAndDecode(frame)
        if ret_bc and puntos is not None:
            frame = cv2.polylines(frame,
                                  [puntos.astype(int)],
                                  True,
                                  (0, 255, 0),
                                  3)
            for codigo, punto in zip(decode, puntos):
                if codigo in detecciones:
                    detecciones[codigo] += 1
                    if detecciones[codigo] >= 30:
                        print("Detección exitosa", codigo)
                        playsound('beep.mp3')
                        cv2.waitKey(250)
                        detecciones.clear()
                else:
                    detecciones[codigo] = 1

                frame = cv2.putText(frame,
                                    codigo,
                                    tuple(punto[1].astype(int)),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    2,
                                    (0, 0, 255),
                                    2,
                                    cv2.LINE_AA)
        cv2.imshow('Escaner de barras', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

# import cv2
# from playsound import playsound

# bd = cv2.barcode_BarcodeDetector()
# cap = cv2.VideoCapture(0)

# detecciones = {}

# while True:
#     ret, frame = cap.read()
#     if ret:
#         ret_bc, decode, puntos = bd.detectAndDecode(frame)
#         if ret_bc:
#             frame = cv2.polylines(frame, puntos.astype(int), True, (0, 255, 0), 3)
#             for codigo, punto in zip(decode, puntos):
#                 if codigo in detecciones:
#                     detecciones[codigo] += 1
#                     if detecciones[codigo] >= 30:
#                         print("Detección exitosa:", codigo)
#                         playsound('beep.mp3')
#                         cv2.waitKey(250)
#                         detecciones.clear()
#                 else:
#                     detecciones[codigo] = 1

#                 frame = cv2.putText(frame, codigo, punto[1].astype(int), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
#         cv2.imshow('Escaner de barras', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cv2.destroyAllWindows()



# import cv2
# from playsound import playsound

# bd = cv2.barcode.BarcodeDetector()
# cap = cv2.VideoCapture(0)

# detecciones = {}

# while True:
#     ret, frame = cap.read()
#     if ret:
#         (ret_bc,
#         decode, 
#         puntos) = bd.detectAndDecode(frame)
#         if ret_bc:
#             frame = cv2.polylines(frame,
#                                   puntos.astype(int),
#                                   True,
#                                   (0,255,0),
#                                   3)
#             for codigo, punto in zip(decode, puntos):
#                 if codigo in detecciones:
#                     detecciones[codigo] +=1
#                     if detecciones[codigo] >= 30:
#                         print("Detección exitosa", codigo)
#                         playsound('beep.mp3')
#                         cv2.waitKey(250)
#                         detecciones.clear()
#                 else:
#                     detecciones[codigo] = 1 

#                 frame = cv2.putText(frame,
#                                     codigo,
#                                     punto[1].astype(int),
#                                     cv2.FONT_HERSHEY_SIMPLEX,
#                                     2,
#                                     (0,0,255),
#                                     2,
#                                     cv2.LINE_AA)
#         cv2.imshow('Escaner de barras', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
        
# cv2.destroyAllWindows()