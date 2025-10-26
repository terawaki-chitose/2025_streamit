import streamlit as st
import pandas as pd
import os

CSV_FILE = "shopping.csv"

# データ読み込み
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["商品名", "数量", "購入済み"])

st.title("🛒　お買い物リストアプリ")

# 商品追加フォーム
st.subheader("📝　商品を追加")
col1, col2 = st.columns([3, 1])
with col1:
    item = st.text_input("商品名")
with col2:
    quantity = st.number_input("数量", min_value=1, value=1)

if st.button("追加"):
    if item:
        new_item = pd.DataFrame([{
            "商品名": item, "数量": quantity, "購入済み": False
        }])
        df = pd.concat([df, new_item], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        st.success(f"{item}を追加しました！")
        st.rerun() # 画像を再読み込み

# 買い物リストの表示と購入済みチェック
st.subheader("📝　買い物リスト")
if len(df) > 0:
    for idx, row in df.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{row['商品名']}**")
        with col2:
            st.write(f"数量： {row['数量']}")
        with col3:
            checked = st.checkbox(
                "購入済み",
                value=bool(row['購入済み']),
                key=f"check_{idx}"
            )
            if checked != bool(row['購入済み']):
                df.loc[idx, '購入済み'] = checked
                df.to_csv(CSV_FILE, index=False)
                st.rerun()

            # 統計情報
        total = len(df)
        completed = len(df[df['購入済み'] == True])
        st.write(f"進捗: {completed}/{total} 完了")
    else:
        st.info("まだ商品が登録されていません")