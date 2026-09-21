import streamlit as st
import pandas as pd
import re
import time
import base64
import os

# تثبيت متصفح بلاي رايت تلقائياً على السحابة لو مش موجود
os.system("playwright install chromium")

from playwright.sync_api import sync_playwright

st.set_page_config(
    page_title="Cyber Intelligence & Social Extractor",
    page_icon="💀",
    layout="centered"
)

# دالة لتحويل الصورة المحلية لـ Base64 عشان تظهر في الخلفية بدون مشاكل
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/webp;base64,{encoded}"
    except:
        return ""

bg_image_code = get_base64_image("HK.webp")

# التصميم النهائي والألوان (أخضر وأحمر فقط + خلفية الهكر المتوهجة)
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.85)), 
                    url('{bg_image_code}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #00ff66;
        font-family: 'Courier New', Courier, monospace;
    }}
    
    @keyframes glow {{
        0% {{ text-shadow: 0 0 10px #ff0033, 0 0 20px #ff0033; }}
        100% {{ text-shadow: 0 0 20px #00ff66, 0 0 30px #00ff66; }}
    }}
    
    .cyber-title {{
        text-align: center;
        color: #00ff66;
        font-size: 26px;
        font-weight: bold;
        animation: glow 2s infinite alternate;
        margin-top: 25px;
    }}
    
    .description {{
        text-align: center;
        color: #ff0033;
        font-size: 14px;
        margin-bottom: 25px;
        font-weight: bold;
    }}
    
    .stTextInput label {{
        color: #00ff66 !important;
        font-weight: bold;
    }}
    
    .stTextInput > div > div > input {{
        background-color: rgba(0, 0, 0, 0.9);
        color: #00ff66;
        border-radius: 10px;
        border: 2px solid #ff0033;
        text-align: right;
    }}
    
    .stButton > button {{
        background: linear-gradient(45deg, #ff0033, #000000);
        color: #00ff66;
        font-weight: bold;
        font-size: 16px;
        border-radius: 10px;
        width: 100%;
        height: 50px;
        border: 2px solid #00ff33;
        box-shadow: 0px 5px 15px rgba(255, 0, 51, 0.5);
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        transform: scale(1.02);
        background: linear-gradient(45deg, #00ff66, #000000);
        color: #ff0033;
        border-color: #ff0033;
    }}
    
    .footer-container {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.95);
        text-align: center;
        padding: 9px 0;
        border-top: 2px solid #ff0033;
        z-index: 100;
    }}
    
    .developer-tag {{
        color: #ff0033;
        font-size: 14px;
        font-family: 'Tahoma', sans-serif;
        font-weight: bold;
        letter-spacing: 1.5px;
        text-shadow: 0 0 10px rgba(255, 0, 51, 0.8);
        margin: 0;
    }}
    </style>
""", unsafe_allow_html=True)

# العنوان
st.markdown("<div class='cyber-title'>💀 CYBER INTELLIGENCE & SOCIAL EXTRACTOR 💀</div>", unsafe_allow_html=True)
st.markdown("<p class='description'>[ Secure Target Data Mining Interface - V2.0 ]</p>", unsafe_allow_html=True)

st.markdown("---")

post_url = st.text_input("🔗 أدخل رابط بوست الضحية (فيسبوك أو إنستجرام):", placeholder="https://www.facebook.com/...")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 بدء الاختراق السحابي وسحب البيانات"):
    if not post_url:
        st.warning("⚠️ أدخل الرابط يا غالي أولاً!")
    else:
        with st.spinner("⏳ جاري الحقن وسحب التعليقات واستخراج الحسابات..."):
            try:
                with sync_playwright() as p:
                    # تم التعديل هنا ليعمل في السحابة بدون شاشة (headless=True)
                    browser = p.chromium.launch(headless=True)
                    context = browser.new_context()
                    page = context.new_page()
                    page.goto(post_url)
                    
                    time.sleep(10)
                    for i in range(5):
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(3)
                        
                    content = page.content()
                    browser.close()
                
                phone_pattern = r'(\+?\d{10,15}|01[0125]\d{8})'
                url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
                
                phones = list(set(re.findall(phone_pattern, content)))
                urls = list(set(re.findall(url_pattern, content)))
                
                max_len = max(len(phones), len(urls), 1)
                phones += [""] * (max_len - len(phones))
                urls += [""] * (max_len - len(urls))
                
                df = pd.DataFrame({
                    "رقم الهاتف المستخرج": phones,
                    "الرابط / الحساب المستخرج": urls
                })
                
                st.session_state['df_results'] = df
                st.success("🔥 تم سحب البيانات بنجاح تام!")
                
            except Exception as e:
                st.error(f"❌ حدث خطأ: {e}")

if 'df_results' in st.session_state and not st.session_state['df_results'].empty:
    st.markdown("---")
    st.subheader("📋 صيد الضحايا (البيانات المستخرجة):")
    st.dataframe(st.session_state['df_results'], use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        excel_file = "comments_data.xlsx"
        st.session_state['df_results'].to_excel(excel_file, index=False)
        with open(excel_file, "rb") as f:
            st.download_button(
                label="📥 تنزيل كملف Excel",
                data=f,
                file_name="comments_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
    with col2:
        csv_data = st.session_state['df_results'].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 تنزيل كملف CSV",
            data=csv_data,
            file_name="comments_data.csv",
            mime="text/csv"
        )

# التوقيع أسفل الصفحة
st.markdown("""
    <div class="footer-container">
        <p class="developer-tag">Developed by Engineer Hamada Ayoub</p>
    </div>
""", unsafe_allow_html=True)
