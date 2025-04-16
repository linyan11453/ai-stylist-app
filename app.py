
# app.py - 主程式
import streamlit as st
import datetime
import random
from db_module.database import init_db, save_item_to_db, get_all_items_from_db, save_tryon_to_db, get_latest_tryon_from_db


# 初始化資料庫
init_db()

# 頁面設定
st.set_page_config(page_title="AI 穿搭顧問", layout="centered")
st.title("👗 AI 穿搭顧問 (中文初版)")

# 使用者輸入基本資料
st.sidebar.header("👤 基本設定")
gender = st.sidebar.selectbox("性別", ["女性", "男性"])
occasion = st.sidebar.selectbox("今日場合", ["日常", "上班", "約會", "聚會", "旅行", "派對", "面試", "沙灘", "運動"])
mood = st.sidebar.selectbox("今日心情", ["中性", "優雅", "活潑", "性感", "高冷"])
style = st.sidebar.selectbox("偏好風格", ["日系", "韓系", "成熟", "甜美", "極簡", "街頭", "傳統"])
period = st.sidebar.checkbox("正在生理期")
pregnant = st.sidebar.checkbox("懷孕中")
crazy_day = st.sidebar.checkbox("Crazy Day 穿搭挑戰")

# 衣櫥管理模組
st.subheader("👚 我的衣櫥")
with st.expander("➕ 新增衣物"):
    item_img = st.file_uploader("上傳衣物圖片", type=["jpg", "jpeg", "png"])
    item_type = st.selectbox("類別", ["上衣", "下身", "洋裝", "外套", "鞋子", "襪子", "帽子", "香水", "飾品"])
    if st.button("儲存衣物"):
        if item_img:
            save_path = f"img_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            with open(save_path, "wb") as f:
                f.write(item_img.getbuffer())
            save_item_to_db(item_type, save_path)
            st.success("已儲存至資料庫！")

# 顯示衣櫥資料
wardrobe_items = get_all_items_from_db()
for t, path in wardrobe_items:
    st.markdown(f"**{t}**")
    st.image(path, width=100)

# 推薦穿搭邏輯模擬
st.subheader("🧠 今日穿搭建議")
if st.button("生成穿搭建議"):
    st.markdown("### 👗 建議項目：")
    sample_items = random.sample(wardrobe_items, min(3, len(wardrobe_items)))
    for t, path in sample_items:
        st.markdown(f"**{t}**")
        st.image(path, width=120)
    if period:
        st.info("建議香氣：柔和木質或柑橘香，舒緩情緒")
    elif pregnant:
        st.info("建議香氣：低敏天然香氛，避免刺激")
    else:
        st.info("建議香氣：依照風格選擇甜美花香或沉穩木質")
    if crazy_day:
        st.warning("今日 Crazy Day 建議：嘗試與平時風格截然不同的穿搭！")

# 試穿模組
st.subheader("🛍️ 購物試穿分析")
tryon_img = st.file_uploader("上傳試穿圖片", type=["jpg", "jpeg", "png"], key="tryon")
tryon_type = st.selectbox("衣物類型", ["上衣", "下身", "洋裝"])
tryon_use = st.selectbox("打算穿去的場合", ["日常", "上班", "約會", "旅行", "派對"])
if st.button("AI 分析試穿照") and tryon_img:
    verdict = random.choice(["✅ 推薦購買", "⚠️ 建議調整搭配後購買", "❌ 不建議購買"])
    suggestion = "可搭配簡約外套與白色球鞋，整體比例更佳。"
    perfume_tip = "推薦香氣：清新柑橘或柔和木質調"
    save_path = f"tryon_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    with open(save_path, "wb") as f:
        f.write(tryon_img.getbuffer())
    save_tryon_to_db(tryon_type, tryon_use, verdict, suggestion, perfume_tip, save_path)
    st.success("已儲存分析紀錄！")
    st.image(save_path, width=160)
    st.markdown(f"**AI 評級：{verdict}**")
    st.markdown(f"**建議：{suggestion}**")
    st.markdown(f"**香氛建議：{perfume_tip}**")

# 分享卡區塊
st.subheader("🎴 分享你的今日造型")
latest = get_latest_tryon_from_db()
if st.button("生成分享卡") and latest:
    t, oc, r, sug, pf, path = latest
    st.image(path, width=200)
    st.markdown("### 👗 我的 AI 穿搭卡")
    st.markdown(f"場合：{oc}")
    st.markdown(f"評級：{r}")
    st.markdown(f"建議語句：{sug}")
    st.markdown(f"香氛：{pf}")
    st.success("可截圖或儲存分享卡至相簿！")
