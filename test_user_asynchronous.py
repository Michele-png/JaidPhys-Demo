import streamlit as st

# Set the title of the app
st.title("Video Player App")

# Add a file uploader for video input
video_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi", "mkv"])

# Check if a video file has been uploaded
if video_file is not None:
    # Show a button to play the video
    play_video = st.button("Play Video")

    if play_video:
        # Display the video in the Streamlit app
        st.video(video_file)

        # Optional: Display the file name and size
        st.write(f"File name: {video_file.name}")
        st.write(f"File size: {video_file.size} bytes")
