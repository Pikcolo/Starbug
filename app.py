"""
Main Application Server for Starbucks Thailand AI Assistant.
Provides LINE Bot Webhook endpoint (/callback) and Web Testing Simulator (/api/chat).
"""
import os
import json
import logging
from flask import Flask, request, abort, render_template, jsonify

from config import LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN, HOST, PORT, DEBUG
from nlp.engine import parse_user_query
from nlp.intents import IntentType
from recommender.filter_engine import filter_menu
from recommender.fair_randomizer import get_top_5_recommendations
from data.scraper import get_menu_data, get_promotions_data
from line_ui.flex_carousel import create_product_carousel_flex
from line_ui.flex_detail import create_product_detail_flex
from line_ui.flex_promo import create_promotions_carousel
from line_ui.flex_receipt import create_order_confirmation_flex
from line_ui.quick_replies import get_default_quick_replies
from nlp.funny_features import get_random_barista_roast

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")

# Initialize LINE Bot SDK v3 handlers if credentials exist
handler = None
line_api = None
try:
    from linebot.v3 import WebhookHandler
    from linebot.v3.messaging import (
        Configuration, ApiClient, MessagingApi,
        ReplyMessageRequest, TextMessage, ImageMessage, FlexMessage, FlexContainer,
        QuickReply, QuickReplyItem, MessageAction
    )
    from linebot.v3.webhooks import MessageEvent, TextMessageContent, ImageMessageContent, StickerMessageContent
    
    if LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN:
        handler = WebhookHandler(LINE_CHANNEL_SECRET)
        configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
        api_client = ApiClient(configuration)
        line_api = MessagingApi(api_client)
        logger.info("LINE Messaging API v3 successfully initialized.")
    else:
        logger.info("Running in Web Simulator mode (LINE credentials not configured in .env).")
except Exception as sdk_err:
    logger.warning(f"LINE Bot SDK init notice: {sdk_err}")


def format_item_images(items_list, base_url=""):
    if not base_url or not base_url.startswith("https://"):
        return items_list
    formatted = []
    for it in items_list:
        it_c = dict(it)
        item_id = it_c.get("id")
        if item_id:
            it_c["image_url"] = f"{base_url}/static/images/products/{item_id}.png"
        formatted.append(it_c)
    return formatted


def process_query_and_build_response(query: str, session_id: str = "default_user", base_url: str = "") -> dict:
    """
    Core conversational routing and response generation.
    Returns structured result with message, flex_payload, nlp_meta, and quick_replies.
    """
    nlp_res = parse_user_query(query)
    intent = nlp_res["intent"]
    entities = nlp_res["entities"]
    
    reply_text = ""
    flex_payload = None
    items_shown = []
    greeting_image_url = None

    if intent == IntentType.GREETING.value:
        greeting_image_url = f"{base_url}/static/images/starbug_barista.jpg" if base_url and base_url.startswith("https://") else "/static/images/starbug_barista.jpg"
        reply_text = (
            "👳‍♂️ ยินดีต้อนรับสู่ Starbug สาขาภารตะแดนสวรรค์นะจ๊ะนายจ๋า! ☕✨\n\n"
            "บาริสต้าดอลลี่ ชัยวาลา พร้อมโชว์ลีลาสะบัดกาน้ำชงกาแฟ 45 องศาระดับตำนานให้นายจ๋าแล้วจ้ะ! 🤣\n\n"
            "💬 วันนี้นายจ๋าอยากสั่งกาแฟ ขนมโรตี หรือเช็คดวง บอกมาได้เลยนะจ๊ะ เช่น:\n"
            "• 'ขอดูกาแฟปั่นงบไม่เกิน 170 บาทนะจ๊ะ'\n"
            "• 'มีชาเขียวมัทฉะอะไรบ้างนายจ๋า'\n"
            "• 'มีโปรโมชั่นเด็ดๆ อะไรบ้างจ้ะ'\n"
            "• 'เมนูแนะนำวันนี้'\n"
            "• 'แซวฉันหน่อย บาริสต้าปากแซ่บ'"
        )
        # Show top general beverages
        candidates = get_menu_data()
        items_shown = format_item_images(get_top_5_recommendations(candidates, session_id=session_id), base_url=base_url)
        flex_payload = create_product_carousel_flex(items_shown, "เมนู Starbug แนะนำสำหรับคุณ")

    elif intent == IntentType.HELP.value:
        reply_text = (
            "📖 **คู่มือเอาตัวรอดร้าน Starbug สไตล์ภารตะนะจ๊ะนายจ๋า:**\n\n"
            "1. ☕ **สั่งกาแฟ/ชา:** 'ขอดูกาแฟ', 'ชาเขียวมัทฉะ', 'เมนูปั่น'\n"
            "2. 🥐 **เติมพลังของว่าง:** 'มีขนมอะไรบ้าง', 'ขอดูเค้ก'\n"
            "3. 💸 **เซฟเงินรูปี:** 'งบไม่เกิน 150 บาท', 'ราคาต่ำกว่า 170'\n"
            "4. 🔍 **ส่องแคลอรี่:** 'Iced Caffe Americano กี่แคล'\n"
            "5. 🛒 **สั่งของกิน:** 'สั่งซื้อ Green Tea Cream Frappuccino 1 แก้ว'\n"
            "6. 🏷️ **ล่าโปรโมชั่น:** 'มีโปรโมชั่นอะไรบ้าง'\n"
            "7. ⭐ **คิดไม่ออก:** 'เมนูแนะนำวันนี้' หรือ 'กินอะไรดี'\n"
            "8. 🤣 **หาเรื่องโดนแซว:** 'แซวฉันหน่อย บาริสต้าปากแซ่บนะจ๊ะ'"
        )
        candidates = get_menu_data()
        items_shown = format_item_images(get_top_5_recommendations(candidates, session_id=session_id), base_url=base_url)
        flex_payload = create_product_carousel_flex(items_shown, "เมนูยอดนิยม Starbug")

    elif intent == IntentType.PROMOTIONS.value:
        promos = get_promotions_data()
        reply_text = "🎉 รวมโปรโมชั่นและดีลลับ Starbug ประจำเดือนนะจ๊ะนายจ๋า! (เซฟเงินรูปีไว้ซื้อทองใส่จ้ะ)"
        flex_payload = create_promotions_carousel(promos)

    elif intent == IntentType.ITEM_DETAIL.value and nlp_res.get("matched_item"):
        item = format_item_images([nlp_res["matched_item"]], base_url=base_url)[0]
        reply_text = f"✨ ส่องเมนู {item['name_th']} ({item['name_en']}) จาก Starbug ซูมดูความอร่อยแบบชัดๆ เลยนะจ๊ะนายจ๋า:"
        flex_payload = create_product_detail_flex(item)
        items_shown = [item]

    elif intent == IntentType.ORDER.value:
        item = nlp_res.get("matched_item")
        if item:
            item = format_item_images([item], base_url=base_url)[0]
            item_name = item.get("name_th", "เมนู Starbug")
            item_en = item.get("name_en", "")

            # Dynamic size & price calculation based on user entity
            selected_size = entities.get("selected_size")
            prices_dict = item.get("prices", {})
            if selected_size and selected_size in prices_dict:
                size_label = selected_size
                price = prices_dict[selected_size]
            elif "Tall" in prices_dict:
                size_label = "Tall"
                price = prices_dict["Tall"]
            elif prices_dict:
                size_label = list(prices_dict.keys())[0]
                price = prices_dict[size_label]
            else:
                size_label = "Standard"
                price = item.get("price", 150)

            order_item = dict(item)
            order_item["price"] = price
            order_item["selected_size"] = size_label

            action_desc = "อบและจัดเตรียมเมนู 🥐" if item.get("is_food") else "สะบัดกาน้ำชงเมนู ☕"

            reply_text = (
                f"✅ รับออเดอร์ Starbug แล้วจ้านายจ๋า!\n"
                f"👨‍🍳 บาริสต้าดอลลี่กำลัง{action_desc}: {item_name} ({item_en})\n"
                f"📏 ขนาด: {size_label}\n"
                f"💰 ค่าเสียหาย: ฿{price}\n"
                f"⏱️ เวลารอประมาณ 10-15 นาที (หรือจนกว่าโรตีจะสุก 🤣)\n\n"
                f"🌐 กดปุ่มด้านล่างเพื่อเปิดหน้าเว็บ Starbug ไปชำระเงินต่อได้ทันทีเลยนะจ๊ะนายจ๋า!"
            )
            flex_payload = create_order_confirmation_flex(order_item)
            items_shown = [order_item]
        else:
            reply_text = (
                "✅ รับออเดอร์ Starbug เรียบร้อยแล้วจ้านายจ๋า!\n"
                "บาริสต้ากำลังสะบัดกาน้ำชงเครื่องดื่มให้อย่างไว ☕✨\n\n"
                "🌐 กดปุ่มด้านล่างเพื่อเปิดหน้าเว็บ Starbug และชำระเงินต่อได้ทันทีนะจ๊ะ!"
            )
            flex_payload = create_order_confirmation_flex()

    elif intent == IntentType.BARISTA_ROAST.value:
        roast_text = get_random_barista_roast()
        reply_text = (
            f"🤣 **บาริสต้า Starbug ปากแซ่บสไตล์ภารตะพร้อมเสิร์ฟนะจ๊ะ!**\n\n"
            f"{roast_text}\n\n"
            f"💚 บาริสต้าดอลลี่แซวเล่นนะจ๊ะนายจ๋า ดื่ม Starbug ให้อร่อยและมีความสุขตลอดวันจ้ะ!"
        )

    else:
        # Filtering & Recommendation
        candidates = filter_menu(nlp_res)
        is_random = (intent == IntentType.RANDOM_RECOMMEND.value)
        items_shown = format_item_images(get_top_5_recommendations(candidates, session_id=session_id, is_random_intent=is_random), base_url=base_url)

        cats = entities.get("categories", [])
        if intent == IntentType.NEW_ARRIVALS.value:
            reply_text = "✨ เมนูมาใหม่สดๆ ร้อนๆ กลิ่นหอมฟุ้งข้ามแม่น้ำคงคาเลยนะจ๊ะนายจ๋า:"
        elif intent == IntentType.RANDOM_RECOMMEND.value:
            reply_text = "⭐ Starbug คัดตัวท็อป 5 เมนูเด็ดสะบัดสะบั้นมาให้นายจ๋าแล้วจ้า เมนูไหนก็อร่อยฟินนะจ๊ะนายจ๋า:"
        elif intent == IntentType.PRICE_FILTER.value:
            max_p = entities.get("max_price")
            reply_text = f"💰 เมนู Starbug สบายกระเป๋า (งบไม่เกิน ฿{max_p if max_p else 'ที่กำหนด'}) อร่อยคุ้มกระเป๋าไม่ฉีกนะจ๊ะนายจ๋า:"
        elif intent == IntentType.SEARCH_FOOD.value or "bakery" in cats:
            reply_text = "🥐 เมนูเบเกอรี่ เค้ก และของว่าง Starbug อบใหม่หอมฟุ้งเหมือนเตาทันดูร์พร้อมเสิร์ฟนะจ๊ะนายจ๋า:"
        elif "tea" in cats:
            reply_text = "🍵 เมนูชาเขียวมัทฉะ และชาพรีเมียม Teavana รสเลิศกลิ่นหอมชื่นใจนะจ๊ะนายจ๋า:"
        elif "frappuccino" in cats:
            reply_text = "🥤 เมนูเครื่องดื่มปั่น Frappuccino หวานฉ่ำเย็นชื่นใจถึงทรวงนะจ๊ะนายจ๋า:"
        elif "espresso" in cats or "cold_brew" in cats:
            reply_text = "☕ เมนูกาแฟสดและเอสเพรสโซ่เข้มข้นสะใจ ตาค้างถึงวันพรุ่งนี้นะจ๊ะนายจ๋า:"
        elif "refresher" in cats:
            reply_text = "🍓 เมนูรีเฟรชเชอร์และน้ำผลไม้สดชื่นดับร้อน สดชื่นสะบัดส่าหรีนะจ๊ะนายจ๋า:"
        else:
            reply_text = "☕ เมนู Starbug สุดฮิตที่คัดมาให้นายจ๋าโดยเฉพาะเลยนะจ๊ะ:"

        flex_payload = create_product_carousel_flex(items_shown, "เมนู Starbug แนะนำ")

        flex_payload = create_product_carousel_flex(items_shown, "เมนู Starbug แนะนำ")

    return {
        "reply_text": reply_text,
        "image_url": greeting_image_url,
        "flex_payload": flex_payload,
        "nlp_meta": nlp_res,
        "items_shown": items_shown,
        "quick_replies": get_default_quick_replies()
    }


@app.route("/", methods=["GET", "POST"])
def home():
    """Renders the Interactive Web Chat Simulator on GET, or routes LINE Webhook on POST."""
    if request.method == "POST":
        # Fallback in case user set webhook URL to root URL instead of /callback
        return callback()
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Web simulator chat endpoint with live NLP analytics."""
    data = request.get_json() or {}
    query = data.get("message", "").strip()
    session_id = data.get("session_id", "web_simulator_user")

    if not query:
        return jsonify({"error": "Empty message"}), 400

    response = process_query_and_build_response(query, session_id=session_id)
    return jsonify(response)


@app.route("/api/menu", methods=["GET"])
def api_menu():
    """Returns the full parsed Starbucks menu."""
    return jsonify({"count": len(get_menu_data()), "menu": get_menu_data()})


@app.route("/api/promotions", methods=["GET"])
def api_promotions():
    """Returns all active promotions."""
    return jsonify(get_promotions_data())


@app.route("/api/health", methods=["GET"])
def api_health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Starbucks Thailand AI Chatbot",
        "menu_items_loaded": len(get_menu_data()),
        "promotions_count": len(get_promotions_data())
    })


@app.route("/callback", methods=["GET", "POST"])
def callback():
    """LINE Bot Webhook endpoint with signature verification."""
    if request.method == "GET":
        return "LINE Webhook Callback Endpoint is Active (Send POST from LINE Platform)", 200

    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    if not handler or not line_api:
        logger.info(f"Received webhook payload (simulator mode): {body[:200]}")
        return "OK (Simulator Mode)", 200

    try:
        handler.handle(body, signature)
    except Exception as e:
        logger.error(f"LINE Webhook verification failed: {e}")
        # Note: Return 200 on initial LINE verification ping if signature is dummy/test
        if not signature or signature == "dummy_signature":
            return "OK (Verify Mode)", 200
        abort(400)

    return "OK", 200


# Register LINE Message Handler if LINE SDK is active
if handler:
    @handler.add(MessageEvent, message=TextMessageContent)
    def handle_line_message(event):
        user_query = event.message.text
        user_id = event.source.user_id if hasattr(event.source, "user_id") else "line_user"
        
        # Get public HTTPS base URL from incoming webhook request
        base_url = request.host_url.rstrip("/")
        if "trycloudflare.com" in base_url and base_url.startswith("http://"):
            base_url = base_url.replace("http://", "https://")

        res = process_query_and_build_response(user_query, session_id=user_id, base_url=base_url)
        
        reply_messages = []
        if res.get("image_url") and res["image_url"].startswith("https://"):
            reply_messages.append(ImageMessage(original_content_url=res["image_url"], preview_image_url=res["image_url"]))

        if res.get("reply_text"):
            reply_messages.append(TextMessage(text=res["reply_text"]))
            
        if res.get("flex_payload"):
            flex_json = res["flex_payload"]
            flex_container = FlexContainer.from_dict(flex_json["contents"])
            reply_messages.append(FlexMessage(alt_text=flex_json.get("altText", "Starbug Menu"), contents=flex_container))
            
        # Build and attach QuickReply pills to the last message
        quick_reply_items = []
        for q_item in res.get("quick_replies", {}).get("items", []):
            act = q_item.get("action", {})
            quick_reply_items.append(
                QuickReplyItem(
                    action=MessageAction(
                        label=act.get("label", ""),
                        text=act.get("text", "")
                    )
                )
            )

        if reply_messages and quick_reply_items:
            reply_messages[-1].quick_reply = QuickReply(items=quick_reply_items)

        line_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=reply_messages
            )
        )

    @handler.add(MessageEvent, message=ImageMessageContent)
    def handle_line_image(event):
        user_id = event.source.user_id if hasattr(event.source, "user_id") else "line_user"
        base_url = request.host_url.rstrip("/")
        if "trycloudflare.com" in base_url and base_url.startswith("http://"):
            base_url = base_url.replace("http://", "https://")

        reply_text = (
            "📸 โอ้โหนายจ๋า! ส่งรูปอะไรมาน่ะจ๊ะ ตาบาริสต้าดอลลี่พร่ามัวไปหมดแล้ว 🤣✨\n\n"
            "ดูเหมือนนายจ๋ากำลังอยากดื่มกาแฟคลายง่วง หรืออยากหาของว่างอร่อยๆ ทานใช่ไหมจ๊ะ?\n\n"
            "👳‍♂️ ถ้านายจ๋าอยากสั่งเมนูไหน ลองพิมพ์ชื่อเมนู หรือเลือก 5 เมนูเด็ดด้านล่างนี้ให้บาริสต้าดอลลี่จัดเสิร์ฟให้นายจ๋าได้เลยนะจ๊ะ! ☕🥐✨"
        )
        
        candidates = get_menu_data()
        items_shown = format_item_images(get_top_5_recommendations(candidates, session_id=user_id, is_random_intent=True), base_url=base_url)
        flex_payload = create_product_carousel_flex(items_shown, "เมนูแนะนำพิเศษสำหรับนายจ๋า")
        flex_container = FlexContainer.from_dict(flex_payload["contents"])

        quick_reply_items = []
        for q_item in get_default_quick_replies().get("items", []):
            act = q_item.get("action", {})
            quick_reply_items.append(
                QuickReplyItem(
                    action=MessageAction(
                        label=act.get("label", ""),
                        text=act.get("text", "")
                    )
                )
            )

        flex_msg = FlexMessage(alt_text="เมนูแนะนำพิเศษสำหรับนายจ๋า", contents=flex_container)
        if quick_reply_items:
            flex_msg.quick_reply = QuickReply(items=quick_reply_items)

        line_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text=reply_text),
                    flex_msg
                ]
            )
        )

    @handler.add(MessageEvent, message=StickerMessageContent)
    def handle_line_sticker(event):
        user_id = event.source.user_id if hasattr(event.source, "user_id") else "line_user"
        reply_text = "👳‍♂️ สติกเกอร์น่ารักสะบัดส่าหรีเลยนะจ๊ะนายจ๋า! ✨ วันนี้นายจ๋าอยากรับกาแฟสด ขนมเค้ก หรือจะให้บาริสต้าดอลลี่จัดเสิร์ฟเมนูไหนดีจ๊ะ? ☕🥐"
        
        quick_reply_items = []
        for q_item in get_default_quick_replies().get("items", []):
            act = q_item.get("action", {})
            quick_reply_items.append(
                QuickReplyItem(
                    action=MessageAction(
                        label=act.get("label", ""),
                        text=act.get("text", "")
                    )
                )
            )

        text_msg = TextMessage(text=reply_text)
        if quick_reply_items:
            text_msg.quick_reply = QuickReply(items=quick_reply_items)

        line_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[text_msg]
            )
        )


if __name__ == "__main__":
    logger.info(f"Starting Starbucks AI Assistant on http://{HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=DEBUG)
