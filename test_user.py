import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        # Here you can process the frame if needed
        return frame

def main():
    st.title("Camera Stream with Streamlit WebRTC")
    st.write("This app captures the camera image stream and displays it on the interface.")

    # Set up the WebRTC streamer with STUN server
    webrtc_streamer(
        key="example", 
        video_transformer_factory=VideoTransformer,
        stun_servers=["stun:stun.l.google.com:19302"]  # Google STUN server
    )

if __name__ == "__main__":
    main()
