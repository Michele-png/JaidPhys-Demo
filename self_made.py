import cv2
import streamlit as st
from random import randrange


train_face_data = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
webcam = cv2.VideoCapture(0)
temp = st.empty()
count = st.empty()
while True:
    successful_frame_read, frame = webcam.read()
    gray_style_picture = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_coordinate = train_face_data.detectMultiScale(gray_style_picture)
    count.success("检测到"+str(len(face_coordinate))+"个人脸")
    for (x, y, w, h) in face_coordinate:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (randrange(0, 255), randrange(0, 255), randrange(0, 255)), 7)
    temp.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB", use_column_width=True)


def overlaid_video():
  

def main():
  st.set_page_config(layout="centered", page_title="实时人脸识别")
