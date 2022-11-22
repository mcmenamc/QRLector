import cv2
import pyzbar.pyzbar as pyzbar
import http3
import asyncio
from playsound import playsound
import os.path

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
dirname = os.path.dirname(os.path.abspath(__file__))
uri = 'https://cool-rain-6866.fly.dev/api/acceso'
cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)


async def send_to_server(matricula):
    client = http3.AsyncClient()
    myobj = {
        'matricula': matricula,
        # 'acceso': '6371b3c5469a0fa86517eac0'
        'acceso': '6371b3cc469a0fa86517eac3'
    }
    response = await client.post(uri, json=myobj, timeout=5, verify=False)
    return response


async def main():

    while True:
        _, frame = cap.read()
        decodedObjects = pyzbar.decode(frame)
        for obj in decodedObjects:
            TextString = obj.data.decode('utf-8')
            response = await send_to_server(TextString)
            try:
                if response.status_code == 201:
                    print(response.json())
                    cv2.putText(frame, 'Bienvenido', (50, 50),
                                font, 2, (255, 0, 0), 3)
                    playsound(dirname + "\check.wav")
                    await asyncio.sleep(0.3)
                else:
                    error = response.json().get('message')
                    print(error)
                    cv2.putText(frame, error, (50, 50),
                                font, 2, (255, 0, 0), 3)
                    playsound(dirname + "\error.wav")
                    await asyncio.sleep(0.3)
            except:
                print('Error')

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

asyncio.run(main())
