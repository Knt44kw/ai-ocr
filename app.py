import streamlit as st
from google.cloud import vision
import io


def detect_text(image_bytes: bytes, service_account_json: str) -> str:
    """
    画像の中に書かれている文字を読み取る関数

    Args:
        image_bytes (byte): 
        入力画像のバイト列
        service_account_json (str): 
        Google Cloud Vision APIの service accountに関する secretが入ったjsonファイル名

    Returns:
        str: 読み取られた入力画像の文字列
    """

    client = vision.ImageAnnotatorClient.from_service_account_json(service_account_json)
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        return texts[0].description
    else:
        return "No text detected."

def main():
    st.title("OCRを用いて文字を読み取るサンプルアプリケーション")
    
    service_account_json_object = st.file_uploader("Upload service account json for Vision API", type=["json"])
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None and service_account_json_object is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        image_bytes: bytes = uploaded_file.getvalue()
        SERVICE_ACCOUNT_JSON: str = service_account_json_object.name 
        detected_text: str = detect_text(image_bytes, SERVICE_ACCOUNT_JSON)
        st.write(f"検出された文字列:\n {detected_text}")

if __name__ == "__main__":
    main()
