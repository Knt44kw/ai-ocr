import streamlit as st
from google.cloud import vision
import io


def detect_text(image_values, service_account_json: str):
    client = vision.ImageAnnotatorClient.from_service_account_json(service_account_json)
    image = vision.Image(content=image_values)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        return texts[0].description
    else:
        return "No text detected."

def main():
    st.title("OCRを用いて文字を読み取るサンプルアプリケーション")

    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    SERVICE_ACCOUNT_JSON = st.secrets.visionApiKey.json

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        image_values = uploaded_file.getvalue()
        detected_text: str = detect_text(image_values, SERVICE_ACCOUNT_JSON)
        st.write(f"検出された文字列:\n {detected_text}")

if __name__ == "__main__":
    main()
