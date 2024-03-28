## Import Libraries
import os
import webuiapi
from io import BytesIO
import PIL
from PIL import Image
import streamlit as st
from defs import pre_setting, gen_animate_img


## Set your API client
api = webuiapi.WebUIApi(host='127.0.0.1', port=7860)
api.util_set_model('darkSushi')


## Streamlit Frontend:
def main():

    # main page pre-setting
    st.set_page_config(page_title="My App", layout="wide")
    st.header("🔥 Animate You 🔥")
    st.subheader("Upload your Photo and Animate")
    st.divider()
    genders = ["Male", "Female", "People"]

    # sidebar
    with st.sidebar:
        st.subheader("Drop Box")
        st.write("\n\n\n")
        photo_upload = st.file_uploader('Attach Photo Below:', type=['jpg','jpeg','png'])
        
        st.write("\n\n\n")
        selected_gender = st.radio("Select Your Gender", genders)
        st.write("\n\n\n")
        gen_button = st.button("Apply Animation Style", type="primary")



        if selected_gender == "Male":
            prompt_selected="a guy, attractive, handsome, masterpiece, 4k, animation style, high quality, looking at the viewers, clean, <lora:LCM_LoRA_Weights_SD15:1>" # lora 추가
        elif selected_gender == "Female":
            prompt_selected="a girl, cute, attractive, pretty, masterpiece, animation style, 4k, high quality, looking at the viewers, clean, <lora:LCM_LoRA_Weights_SD15:1>"
        elif selected_gender == "People":
            prompt_selected= "people, attractive, 4k, masterpiece, cute, brothers and sisters, animation style, <lora:sister_and_little_brother_V2:1>, <lora:LCM_LoRA_Weights_SD15:1>"

    # columns divide    
    col1, col2, col3 = st.columns([1,0.1,1])

    # col1
    with col1:
        if photo_upload:
            uploaded_img_path = photo_upload
            input_img = st.image(uploaded_img_path, caption="Uploaded Photo")
            img = Image.open(uploaded_img_path)
            print(img.size)
    
    # col3
    with col3:
        if gen_button:
            with st.spinner("Generating Animation Photo ..."):
                w, h = img.size[0], img.size[1]
                ads, unit1, unit2 = pre_setting(img)
                result = gen_animate_img(img, api, ads, unit1, unit2, w, h, prompt_selected)
                result_img = st.image(result, caption="Animated Photo")
                if result_img:
                    st.sidebar.success("Animated Successfully ...!")


if __name__ == "__main__":
    main()