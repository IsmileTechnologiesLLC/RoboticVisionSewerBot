#!copyright by utkarshcrazy@gitlab

import time
import os
import sys
import asyncio
from azure.iot.device.aio import IoTHubModuleClient
import cv2
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

#Azure storage connection string
m_str_Connect_str ="DefaultEndpointsProtocol=https;AccountName=storageaccounteventhub1;AccountKey=3WOTa4vl26KCFnW2DQ2HrAczu3d2Mtzt1t47ZBjZIj4kxmTyVtL3j37IFZ5TA9bkvpKhEcndXT2a2u+zXFCE6g==;EndpointSuffix=core.windows.net"
print ("Open camera")
cap = cv2.VideoCapture(0)
print ("Opened")

print ("Init")
ret, frame = cap.read()
print ("Done init")
#is this working? @aniket

async def main():
    try:
        if not sys.version >= "3.5.3":
            raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
        print ( "IoT Hub Client for Python" )


        # define behavior for halting the application
        def stdin_listener():
            while True:
                try:
                    print("TakePicture")
                    (grabbed, frame) = cap.read()
                    print("Took")
                    current_time= datetime.now()
                    strFilename = str(current_time.strftime("%m%d%Y_%H%M%S")) + ".png";
                    print("write: " + strFilename)
                    file_dir="//home//pi//robotlivestream//videos//"
                    cv2.imwrite(file_dir+strFilename, frame)
                    print("wrote")

                    print("Upload: " + strFilename)                    
                    blob_service_client = BlobServiceClient.from_connection_string(m_str_Connect_str)
                    container_name = "videosforroboticvision"
                    blob_client = blob_service_client.get_blob_client(container=container_name, blob=strFilename)
    
                    with open(file_dir+strFilename, "rb") as data:
                        blob_client.upload_blob(data, overwrite=True)

                    print("Uploaded")
                    
                except Exception as ex:
                    print('Exception:')
                    print(ex)
                    time.sleep(10)
        print ( "The sample is now waiting for messages. ")

        # Run the stdin listener in the event loop
        loop = asyncio.get_event_loop()
        user_finished = loop.run_in_executor(None, stdin_listener)

        # Wait for user to indicate they are done listening for messages
        await user_finished
                
#         def TakePicture():
#             print ( "TakePicture")
#             (grabbed, frame) = cap.read()
#             showimg = frame
#             image = 'capture.png'
# 
#             print ( "write")
# 
#             cv2.imwrite(image, frame)
#             cap.release()
# 
#             #This is the connection string to azure
#             connect_str = m_str_Connect_str
#         
#             blob_service_client = BlobServiceClient.from_connection_string(connect_str)
#             
#             container_name = "videosforroboticvision"
#             
#             # Create the container
#             blob_client = blob_service_client.get_blob_client(container=container_name, blob=image)
# 
#             print("\nUploading to Azure Storage as blob:\n\t" + image)
# 
#             # Upload the created file
#             with open(image, "rb") as data:
#                 blob_client.upload_blob(data, overwrite=True)
# 
#             return image
        
    except Exception as e:
        print ( "Unexpected error %s " % e )
        raise

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()