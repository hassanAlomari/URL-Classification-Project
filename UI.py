import streamlit as st
import requests

# 1. عنوان الصفحة
st.title("🤖 كاشف الروابط الخبيثة (AI Model)")

# 2. حقل إدخال الرابط
url_input = st.text_input("أدخل الرابط هنا:", placeholder="http://google.com")

# 3. زر الفحص
if st.button("افحص الرابط 🔍"):
    if url_input:
        # عرض علامة تحميل
        with st.spinner('جاري الاتصال بالموديل...'):
            try:
                # -----------------------------------------------------
                # اللحظة الحاسمة: إرسال الرابط للسيرفر (FastAPI)
                # -----------------------------------------------------
                # لاحظ أننا نرسل البيانات كـ JSON كما يتوقع FastAPI
                response = requests.post(
                    "https://url-classification-project.onrender.com/predict", 
                    json={"url": url_input}
                )
                
                # التحقق من نجاح الطلب (Status Code 200)
                if response.status_code == 200:
                    data = response.json()
                    
                    # عرض النتائج بناء على الرد
                    if data["label"] == "Malicious":
                        st.error(f"⚠️ تحذير! هذا الرابط خبيث. (ثقة: {data['confidence']})")
                    else:
                        st.success(f"✅ هذا الرابط آمن. (ثقة: {data['confidence']})")
                        
                    # عرض البيانات الخام (للتجربة)
                    st.json(data)
                else:
                    st.error("حدث خطأ في السيرفر!")
                    st.write(response.text)
                    
            except Exception as e:
                st.error(f"فشل الاتصال بالسيرفر. هل تأكدت من تشغيل uvicorn؟")
                st.error(e)
    else:
        st.warning("الرجاء إدخال رابط أولاً.")
