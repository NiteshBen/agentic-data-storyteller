import os
import sys
import json
import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# Set UTF-8 encoding for console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Attempt loading from local .env or fallback to the scratch directory
load_dotenv()
token = os.getenv("LINKEDIN_ACCESS_TOKEN")
if not token:
    fallback_env = r"C:\Users\91772\.gemini\antigravity\scratch\linkedin_ai_daily\.env"
    if os.path.exists(fallback_env):
        load_dotenv(fallback_env)
        token = os.getenv("LINKEDIN_ACCESS_TOKEN")

if not token:
    print("[-] Error: LINKEDIN_ACCESS_TOKEN not found in environment or .env file.")
    sys.exit(1)

def load_font(size, bold=False):
    win_path = "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"
    if os.path.exists(win_path):
        try:
            return ImageFont.truetype(win_path, size)
        except Exception:
            pass
    win_arial = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    if os.path.exists(win_arial):
        try:
            return ImageFont.truetype(win_arial, size)
        except Exception:
            pass
    return ImageFont.load_default()

def generate_infographic_png(output_path="artifacts/linkedin_infographic.png"):
    width, height = 1080, 1080
    img = Image.new("RGBA", (width, height), (11, 15, 25, 255))
    draw = ImageDraw.Draw(img)

    # Ambient Glows
    glow1 = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow1)
    glow_draw.ellipse([(650, -100), (1200, 450)], fill=(14, 165, 233, 40))
    glow_draw.ellipse([(-100, 650), (450, 1200)], fill=(139, 92, 246, 35))
    img = Image.alpha_composite(img, glow1)
    draw = ImageDraw.Draw(img)

    # Outer Container Card
    draw.rounded_rectangle([(45, 45), (1035, 1035)], radius=28, fill=(17, 24, 39, 245), outline=(56, 189, 248, 140), width=2)

    # Header Tags
    badge_font = load_font(20, bold=True)
    draw.rounded_rectangle([(85, 80), (380, 125)], radius=10, fill=(14, 165, 233, 255))
    draw.text((105, 92), "MULTI-AGENT AI SYSTEM", font=badge_font, fill=(255, 255, 255))

    draw.rounded_rectangle([(730, 80), (995, 125)], radius=10, fill=(30, 41, 59, 230), outline=(56, 189, 248, 160), width=1)
    draw.text((755, 92), "PORTFOLIO RELEASE", font=badge_font, fill=(56, 189, 248))

    draw.line([(85, 150), (995, 150)], fill=(51, 65, 85, 180), width=2)

    # Title & Subtitle
    title_font = load_font(42, bold=True)
    sub_font = load_font(22, bold=False)
    draw.text((85, 175), "Agentic Data Storyteller", font=title_font, fill=(255, 255, 255))
    draw.text((85, 230), "Autonomous Multi-Agent BI & Executive Narrative Engine", font=sub_font, fill=(148, 163, 184))

    # 4 Metric Cards Row
    kpis = [
        {"val": "500+", "lbl": "Records Profiled"},
        {"val": "12", "lbl": "Dimensions"},
        {"val": "4", "lbl": "AI Agents"},
        {"val": "100%", "lbl": "Test Coverage"}
    ]
    card_w = 205
    card_h = 95
    start_x = 85
    card_y = 285
    val_font = load_font(32, bold=True)
    lbl_font = load_font(14, bold=True)
    
    for i, k in enumerate(kpis):
        cx = start_x + (i * (card_w + 24))
        draw.rounded_rectangle([(cx, card_y), (cx + card_w, card_y + card_h)], radius=14, fill=(30, 41, 59, 220), outline=(71, 85, 105, 160), width=1)
        draw.text((cx + 18, card_y + 14), k["val"], font=val_font, fill=(56, 189, 248))
        draw.text((cx + 18, card_y + 58), k["lbl"].upper(), font=lbl_font, fill=(148, 163, 184))

    # Architecture Box (Center Content)
    draw.rounded_rectangle([(85, 415), (995, 875)], radius=20, fill=(15, 23, 42, 230), outline=(56, 189, 248, 80), width=1)
    
    sec_font = load_font(18, bold=True)
    draw.text((115, 435), "COLLABORATIVE AGENT ARCHITECTURE", font=sec_font, fill=(129, 140, 248))

    agents_info = [
        ("🔍 DataProfilerAgent", "Computes distribution moments, missingness matrix, and IQR outlier boundaries."),
        ("💡 InsightDiscoveryAgent", "Surfaces multivariate correlations (|r| >= 0.45) & categorical concentration."),
        ("📈 DataVisualizerAgent", "Synthesizes Plotly figures into an interactive glassmorphic HTML executive dashboard."),
        ("📝 StorytellerAgent", "Translates raw analytics into an actionable executive brief & strategic recommendations.")
    ]

    agent_title_font = load_font(22, bold=True)
    agent_desc_font = load_font(18, bold=False)

    ay = 480
    for name, desc in agents_info:
        draw.text((115, ay), name, font=agent_title_font, fill=(56, 189, 248))
        draw.text((115, ay + 32), desc, font=agent_desc_font, fill=(226, 232, 240))
        ay += 92

    # Footer Branding
    footer_font = load_font(18, bold=True)
    draw.text((85, 915), "Engineered by Nitesh Beniwal", font=footer_font, fill=(255, 255, 255))
    draw.text((85, 945), "GitHub: github.com/NiteshBen/agentic-data-storyteller", font=load_font(16, bold=False), fill=(148, 163, 184))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Convert RGBA to RGB for JPEG/PNG compatibility
    rgb_img = Image.new("RGB", img.size, (11, 15, 25))
    rgb_img.paste(img, mask=img.split()[3])
    rgb_img.save(output_path, "PNG", quality=95)
    return output_path

def get_author_urn():
    resp = requests.get("https://api.linkedin.com/v2/userinfo", headers={"Authorization": f"Bearer {token}"})
    if resp.status_code == 200:
        return resp.json()["sub"]
    resp2 = requests.get("https://api.linkedin.com/v2/me", headers={"Authorization": f"Bearer {token}"})
    resp2.raise_for_status()
    return resp2.json()["id"]

def upload_image(image_path, author_urn):
    register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
    payload = {
        "registerUploadRequest": {
            "owner": f"urn:li:person:{author_urn}",
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "serviceRelationships": [{"identifier": "urn:li:userGeneratedContent", "relationshipType": "OWNER"}]
        }
    }
    resp = requests.post(register_url, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, json=payload)
    resp.raise_for_status()
    upload_info = resp.json()
    upload_url = upload_info["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
    asset_urn = upload_info["value"]["asset"]

    with open(image_path, "rb") as f:
        img_data = f.read()

    upload_resp = requests.put(upload_url, data=img_data, headers={"Authorization": f"Bearer {token}", "Content-Type": "image/png"})
    upload_resp.raise_for_status()
    return asset_urn

def publish_post(author_urn, image_urn, commentary):
    post_url = "https://api.linkedin.com/v2/ugcPosts"
    post_payload = {
        "author": f"urn:li:person:{author_urn}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": commentary},
                "shareMediaCategory": "IMAGE",
                "media": [{
                    "status": "READY",
                    "description": {"text": "Agentic Data Storyteller Multi-Agent System Infographic"},
                    "media": image_urn,
                    "title": {"text": "Agentic Data Storyteller: Autonomous Multi-Agent BI Engine"}
                }]
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }

    resp = requests.post(
        post_url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        },
        json=post_payload
    )
    resp.raise_for_status()
    return resp.json()

def main():
    print("==================================================")
    print("      PUBLISHING TO LINKEDIN (AUTOMATED API)      ")
    print("==================================================")
    print("[*] 1. Generating high-resolution infographic PNG...")
    png_path = generate_infographic_png()
    print(f"[+] Infographic generated at: {png_path}")

    print("[*] 2. Authenticating with LinkedIn API...")
    author_urn = get_author_urn()
    print(f"[+] Authenticated as Author URN: {author_urn}")

    print("[*] 3. Uploading infographic media asset to LinkedIn...")
    image_urn = upload_image(png_path, author_urn)
    print(f"[+] Image asset registered and uploaded: {image_urn}")

    # Read post content
    post_path = "LINKEDIN_POST.md"
    if not os.path.exists(post_path):
        post_path = "artifacts/LINKEDIN_POST.md"
    with open(post_path, "r", encoding="utf-8") as f:
        commentary = f.read()

    print("[*] 4. Publishing UGC Post to LinkedIn feed...")
    res = publish_post(author_urn, image_urn, commentary)
    post_id = res.get("id", "Unknown")
    print("\n[+] SUCCESS! Post successfully published to LinkedIn!")
    print(f"[+] LinkedIn Post ID / URN: {post_id}")
    print(f"[+] View on your profile: https://www.linkedin.com/in/nitesh-ben/")
    print("==================================================")

if __name__ == "__main__":
    main()
