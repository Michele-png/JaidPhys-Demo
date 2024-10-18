import streamlit as st
from streamlit_webrtc import WebRtcMode, VideoTransformerBase, webrtc_streamer
from sample_utils.turn import get_ice_servers

# class VideoTransformer(VideoTransformerBase):
#     def transform(self, frame):
#         # Here you can process the frame if needed
#         return frame

def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    image = frame.to_ndarray(format="bgr24")
    return av.VideoFrame.from_ndarray(image, format="bgr24")

def main():
    st.title("Camera Stream with Streamlit WebRTC")
    st.write("This app captures the camera image stream and displays it on the interface.")

    # Set up the WebRTC streamer with STUN server
    webrtc_ctx = webrtc_streamer(
        key="posture-detection",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={
            "iceServers": get_ice_servers(),
            "iceTransportPolicy": "relay",
        },
        # video_processor_factory=VideoTransformer,
        video_frame_callback=video_frame_callback,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

if __name__ == "__main__":
    main()
