import streamlit as st
import pandas as pd
import re
import time
import base64
import os

# تثبيت متصفح بلاي رايت تلقائياً على السحابة
os.system("playwright install chromium")

from playwright.sync_api import sync_playwright

st.set_page_config(
    page_title="Cyber Intelligence & Social Extractor",
    page_icon="💀",
    layout="centered"
)

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/webp;base64,{encoded}"
    except:
        return ""

bg_image_code = get_base64_image("HK.webp")

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
        border: 2px solid #ff0033;
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

st.markdown("<div class='cyber-title'>💀 CYBER INTELLIGENCE & SOCIAL EXTRACTOR 💀</div>", unsafe_allow_html=True)
st.markdown("<p class='description'>[ Deep Target Mining & Lead Qualification - V4.0 ]</p>", unsafe_allow_html=True)

st.markdown("---")

post_url = st.text_input("🔗 أدخل رابط البوست المستهدف:", placeholder="https://www.facebook.com/...")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 بدء فحص المهتمين واستخراج البيانات العميقة"):
    if not post_url:
        st.warning("⚠️ أدخل الرابط يا غالي أولاً!")
    else:
        with st.spinner("⏳ جارٍ استهداف المهتمين بالبوست وفحص بروفايلاتهم شخصياً..."):
            try:
                extracted_data = []
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    context = browser.new_context(
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                    )
                    page = context.new_page()
                    page.goto(post_url, timeout=60000)
                    
                    time.sleep(8)
                    
                    # التمرير لتحميل التعليقات التفاعلية
                    for i in range(4):
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(3)
                    
                    # استخراج عناصر الروابط وأسماء المعلقين المهتمين من البوست
                    profile_elements = page.locator('a[href*="facebook.com/"], a[href*="instagram.com/"]').all()
                    
                    targets = []
                    seen_urls = set()

                    for el in profile_elements:
                        try:
                            href = el.get_attribute("href")
                            name = el.inner_text().strip()
                            
                            # فلترة الروابط لاستبعاد اللينكات العامة والتركيز على بروفايلات الأشخاص
                            if href and name and len(name) > 2:
                                if "/posts/" not in href and "/photos/" not in href and "/watch/" not in href and "/story.php" not in href:
                                    if href not in seen_urls:
                                        seen_urls.add(href)
                                        targets.append({"name": name, "url": href})
                                        if len(targets) >= 10:  # حد أقصى لاستهداف أول 10 أهداف لضمان السرعة وتجنب الحظر
                                            break
                        except:
                            continue

                    # فحص كل بروفايل على حدة لاستخراج البيانات المتاحة (رقم الهاتف / الاهتمام)
                    for target in targets:
                        profile_name = target["name"]
                        profile_url = target["url"]
                        phone_found = "غير متوفر (حساب خاص)"
                        
                        try:
                            # فتح صفحة البروفايل الشخصي للهدف
                            profile_page = context.new_page()
                            profile_page.goto(profile_url, timeout=30000)
                            time.sleep(4)
                            
                            profile_text = profile_page.inner_text("body")
                            
                            # البحث عن رقم هاتف داخل بروفايل الشخص
                            phone_regex = r'(?:\+?[0-9]{1,3}\s?)?(?:01[0125][0-9]{8}|[0-9]{10,12})'
                            found_phones = re.findall(phone_regex, profile_text)
                            valid_phones = [p for p in found_phones if 10 <= len(re.sub(r'\D', '', p)) <= 13]
                            
                            if valid_phones:
                                phone_found = re.sub(r'\D', '', valid_phones[0])
                            
                            profile_page.close()
                        except:
                            pass

                        extracted_data.append({
                            "اسم الشخص المهتم": profile_name,
                            "رقم الهاتف (إن وجد)": phone_found,
                            "رابط الحساب الشخصي": profile_url,
                            "الحالة": "مهتم بالبوست ومفحوص"
                        })

                    browser.close()
                
                if extracted_data:
                    df = pd.DataFrame(extracted_data)
                else:
                    df = pd.DataFrame({
                        "اسم الشخص المهتم": ["لم يتم العثور على أهداف (يتطلب فتح الصلاحيات أو تسجيل دخول)"],
                        "رقم الهاتف (إن وجد)": ["---"],
                        "رابط الحساب الشخصي": ["---"],
                        "الحالة": ["فشل الاستخراج"]
                    })
                
                st.session_state['df_results'] = df
                st.success("🔥 تم تجميع الأهداف المهتمة وفحص بروفايلاتهم بنجاح تام!")
                
            except Exception as e:
                st.error(f"❌ حدث خطأ أثناء فحص الأهداف: {e}")

if 'df_results' in st.session_state and not st.session_state['df_results'].empty:
    st.markdown("---")
    st.subheader("📋 تقرير الأهداف المهتمة والبيانات المستخرجة:")
    st.dataframe(st.session_state['df_results'], use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        excel_file = "qualified_targets.xlsx"
        st.session_state['df_results'].to_excel(excel_file, index=False)
        with open(excel_file, "rb") as f:
            st.download_button(
                label="📥 تنزيل كملف Excel",
                data=f,
                file_name="qualified_targets.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
    with col2:
        csv_data = st.session_state['df_results'].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 تنزيل كملف CSV",
            data=csv_data,
            file_name="qualified_targets.csv",
            mime="text/csv"
        )

st.markdown("""
    <div class="footer-container">
        <p class="developer-tag">Developed by Engineer Hamada Ayoub</p>
    </div>
""", unsafe_allow_html=Target Container if needed)
