import streamlit as st
from streamlit_webrtc import WebRtcMode, VideoTransformerBase, webrtc_streamer, RTCConfiguration
from sample_utils.turn import get_ice_servers
import av

class VideoProcessor:
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        return av.VideoFrame.from_ndarray(img, format="bgr24")
    
st.title("Camera Stream with Streamlit WebRTC")
st.write("This app captures the camera image stream and displays it on the interface.")

# Set up the WebRTC streamer with STUN server
webrtc_ctx = webrtc_streamer(
    key="posture-detection",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration = {
        "iceServers": get_ice_servers(),
        "iceTransportPolicy": "relay",
    },
    media_stream_constraints={"video": True, "audio": False},
    video_processor_factory=VideoProcessor,
    async_processing=True,
)

