# Email sending
import html
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# WebScrapper
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from unidecode import unidecode

# Pipeline de Dados
import pandas as pd

# Ambiente
import os


# Carregar resumos mais recentes
def load_news():
    path_database = "./02. Databases/Summaries/"
    most_recent = max(os.listdir(path_database))

    df = pd.read_csv(path_database + most_recent)
    
    return df


def format_news_html(df):
    html_rows = []
    for _, row in df.iterrows():
        title = html.escape(str(row['Titulo']))
        url = str(row.get("url", "#"))
        impacto = str(row.get("impacto", "")).strip().lower()
        nivel = html.escape(str(row.get("nivel", "")))
        takeaways_raw = str(row.get("Takeaways", ""))

        title_html = f"<b><a href='{html.escape(url)}' style='color:#2a5db0; text-decoration:none;'>{title}</a></b><br>"

        impact_color = {"positivo": "green", "negativo": "red", "neutro": "gray"}.get(impacto, "black")
        impact_html = f"<span style='color:{impact_color}'>{nivel} impacto {impacto}</span><br>"

        takeaway_items = [item.strip() for item in takeaways_raw.split("-") if item.strip()]
        takeaway_list_html = "<ul>" + "".join(f"<li>{html.escape(item)}</li>" for item in takeaway_items) + "</ul>".replace("\n", "")

        row_html = f"""
        <div style="padding:15px; border-bottom:1px solid #ccc;">
            {title_html}
            {impact_html}
            {takeaway_list_html}
        </div>
        """
        html_rows.append(row_html)

    return "".join(html_rows)



def format_email_body(df):
    html_rows = []
    for _, row in df.iterrows():
        # Escape fields for safety
        title = html.escape(str(row['Titulo']))
        url = str(row.get("url", "#"))  # Default to "#" if url missing
        impacto = str(row.get("impacto", "")).strip().lower()
        nivel = html.escape(str(row.get("nivel", "")))
        takeaways_raw = str(row.get("Takeaways", ""))

        # Title as hyperlink
        title_html = f"<b><a href='{html.escape(url)}' style='color:#2a5db0; text-decoration:none;'>{title}</a></b><br>"

        # Color for impact
        impact_color = {
            "positivo": "green",
            "negativo": "red",
            "neutro": "gray"
        }.get(impacto, "black")
        impact_html = f"<span style='color:{impact_color}'>{nivel} impacto {impacto}</span><br>"

        # Bullet list for takeaways
        takeaway_items = [item.strip() for item in takeaways_raw.split("-") if item.strip()]
        takeaway_list_html = "<ul>" + "".join(f"<li>{html.escape(item)}</li>" for item in takeaway_items) + "</ul>"

        row_html = f"""
        <div style="padding:15px; border-bottom:1px solid #ccc;">
            {title_html}
            {impact_html}
            {takeaway_list_html}
        </div>
        """
        html_rows.append(row_html)

    full_html = f"""
    <html>
    <body style="font-family:Arial, sans-serif;">
        <h2>📰 Market-Relevant News</h2>
        {''.join(html_rows)}
    </body>
    </html>
    """

    return full_html



def send_email(subject, html_content, sender_email, sender_password, recipients):
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject

    # Attach HTML
    msg.attach(MIMEText(html_content, "html"))

    # Send via SMTP
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipients, msg.as_string())
        print("Disparo bem sucedido.")
    except Exception as e:
        print(f"Erro ao disparar email: {e}")



# Utility to extract visible text from an article
def extract_article_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip()
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text() for p in paragraphs)
        return text.strip(), title
    
    except Exception as e:
        print(f"Erro ao extrair {url}: {e}")
        return ""


# Utility to find relevant links
def find_relevant_links(site_url, palavras_chave = ["acoes", "bolsa", "mercado", "ibovespa", "b3", "juros", "inflação", "selic", "petrobras"]):
    try:
        response = requests.get(site_url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        anchors = soup.find_all("a", href=True)
        links = set()

        for a in anchors:
            href = a["href"]
            full_url = urljoin(site_url, href)
            text = a.get_text().lower()
            if any(keyword in unidecode(text) for keyword in palavras_chave) and (not "patrocinado" in full_url):
                links.add(full_url)

        return list(links)[:5]  # Top 5 relevant
    except Exception as e:
        print(f"Erro ao processar {site_url}: {e}")
        return []