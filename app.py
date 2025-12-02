import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import random

# Sayfa Ayarları
st.set_page_config(
    page_title="AI Photo Studio (Fast)",
    page_icon="⚡",
    layout="wide"
)

# --- Fonksiyonlar ---

def generate_image_pollinations(prompt, auto_enhance=True):
    """
    Pollinations.ai kullanarak resim oluşturur.
    API Key gerektirmez.
    """
    try:
        # Prompt Geliştirme (Manuel Ekleme Yöntemi)
        # Gemini olmadığı için kaliteyi artıracak kelimeleri biz ekliyoruz.
        final_prompt = prompt
        if auto_enhance:
            quality_boosters = ", cinematic lighting, 8k resolution, photorealistic, masterpiece, sharp focus, high contrast, vivid colors"
            final_prompt += quality_boosters
        
        # Rastgelelik (Seed)
        seed = random.randint(1, 100000)
        
        # URL'yi oluştur (Pollinations GET isteği ile çalışır)
        # 'enhance=true' parametresi Pollinations'ın kendi AI'sının promptu yorumlamasını sağlar
        base_url = "https://image.pollinations.ai/prompt/"
        params = f"{final_prompt}?seed={seed}&width=1024&height=1024&nologo=true&enhance=true&model=flux"
        
        image_url = base_url + params
        
        # İsteği gönder
        response = requests.get(image_url, timeout=30) # 30 saniye zaman aşımı
        
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            st.error(f"Sunucu Hatası: {response.status_code}")
            return None
            
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")
        return None

# --- Arayüz (UI) ---

st.sidebar.title("AI Photo Studio")
st.sidebar.success("⚡ Mod: Hızlı & Limitsiz")
st.sidebar.write("Gemini devre dışı bırakıldı. Doğrudan çizim yapılıyor.")
st.sidebar.markdown("---")
st.sidebar.caption("Developed by Akın ÖZTÜRK with ❤️")

st.title("⚡ Hızlı AI Ressam")
st.markdown("API anahtarı yok, bekleme yok. Fikrini yaz ve butona bas.")

col1, col2 = st.columns([1, 1])

with col1:
    # Kullanıcı Girişi
    user_input = st.text_area(
        "Ne çizdirmek istersin?", 
        placeholder="Örn: Ormanda yürüyen sevimli bir robot...",
        height=150
    )
    
    # Ayarlar
    auto_enhance = st.checkbox("🪄 Kaliteyi Otomatik Artır (Magic Boost)", value=True, help="Promptunuza '8k, sinematik' gibi kelimeler ekler.")
    
    # Buton
    generate_btn = st.button("🚀 Resmi Oluştur", type="primary", use_container_width=True)

with col2:
    if generate_btn:
        if not user_input:
            st.warning("Lütfen önce bir şeyler yazın.")
        else:
            status_box = st.status("Resim sunucudan isteniyor...", expanded=True)
            
            # İşlem
            status_box.write("🎨 Çizim yapılıyor (Ortalama 5-10 sn)...")
            image = generate_image_pollinations(user_input, auto_enhance)
            
            if image:
                status_box.update(label="Tamamlandı!", state="complete", expanded=False)
                st.image(image, caption=user_input, use_container_width=True)
                
                # İndirme Butonu
                buf = BytesIO()
                image.save(buf, format="PNG")
                st.download_button(
                    label="📥 Resmi İndir",
                    data=buf.getvalue(),
                    file_name="ai_image.png",
                    mime="image/png",
                    use_container_width=True
                )
            else:
                status_box.update(label="Başarısız", state="error")
                st.error("Bir sorun oluştu. Lütfen tekrar deneyin.")
