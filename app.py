
import streamlit as st
import feedparser
import openai
from datetime import datetime

openai.api_key = st.secrets["openai_api_key"]

rss_urls = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed",
    "https://bitcoinmagazine.com/.rss/full",
    "https://bitcoinist.com/feed/",
    "https://cryptoslate.com/feed/",
    "https://cryptobriefing.com/feed/",
    "https://www.newsbtc.com/feed/",
    "https://coingape.com/feed/",
    "https://cryptopotato.com/feed/",
    "https://u.today/rss",
    "https://www.ccn.com/rss-feeds/crypto/",
    "https://bitcoinnews.com/rss-feed/",
    "https://nulltx.com/feed/",
    "https://www.cryptoglobe.com/feed/",
    "https://cryptodaily.co.uk/feed",
    "https://cryptonews.com/news/feed/",
    "https://coinjournal.net/feed/",
    "https://coincheckup.com/rss",
    "https://www.coinspeaker.com/feed/"
]

def analyze_sentiment(text):
    prompt = f"""Проаналізуй наступний текст з точки зору впливу на ціну BTC/USDT.
Вкажи одну з відповідей: bullish (↑), bearish (↓), або neutral (→).

Текст: "{text}"
Висновок:"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {e}"

st.title("GPT-аналітик новин BTC/USDT")
st.write("Цей застосунок збирає новини з криптовалютних джерел і визначає їхній настрій щодо BTC/USDT.")

if st.button("🔍 Проаналізувати новини"):
    results = []
    with st.spinner("Збір і аналіз новин..."):
        for url in rss_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries[:3]:
                title = entry.get('title', 'No Title')
                summary = entry.get('summary', '')
                published = entry.get('published', datetime.utcnow().isoformat())
                full_text = f"{title}. {summary}"
                sentiment = analyze_sentiment(full_text)
                results.append({
                    "Дата": published,
                    "Джерело": url,
                    "Заголовок": title,
                    "Настрій": sentiment
                })

    st.success("Аналіз завершено!")
    st.write("### Результати аналізу:")
    for res in results:
        st.markdown(f"**{res['Дата']}** | *{res['Джерело']}*")
        st.markdown(f"**{res['Заголовок']}**")
        st.markdown(f"🧠 Настрій: **{res['Настрій']}**")
        st.markdown("---")
