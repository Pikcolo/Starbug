"""
Funny & Creative Interactive Features for Starbug AI Assistant (Indian Chaiwala & Bollywood Style).
Includes Fortune Teller, Chaos Secret Recipe Generator, Sassy Barista Roast, and Wealth Calculator.
"""
import random
from typing import Dict, Any, List

FORTUNES = [
    {
        "topic": "💼 ดวงการงาน & สู้ชีวิตนะจ๊ะนายจ๋า",
        "fortune": "วันนี้นายจ๋าจะเจองานด่วนทะลวงมิติเข้ามาตอน 17:59 น. พระศุกร์เข้าพระเสาร์แทรก ส่ายหัวดุ๊กดิ๊กสามทีแล้วลุยต่อนะจ๊ะนายจ๋า บาริสต้าดอลลี่เป็นกำลังใจให้จ้ะ!",
        "lucky_drink": "ไอซ์ คาเฟ่ อเมริกาโน่ (ดับเบิ้ลช็อตเข้มตาค้าง)",
        "tip": "จิบแล้วสะบัดหัว 45 องศา พิมพ์ตอบ 'รับทราบครับนายจ๋า' ด้วยความเร็วแสงนะจ๊ะ",
        "color": "#1E3932",
        "image_url": "https://blob.starbucks.co.th/publicproduct26/home-banner-1784217494661.jpg"
    },
    {
        "topic": "💖 ดวงความรัก & สะบัดส่าหรี",
        "fortune": "ความรักของนายจ๋าช่วงนี้เหมือนนมข้นหวานในชาชัก... หวานเจี๊ยบจนมดขึ้น หรือไม่ก็กำลังโดนเทเหมือนกาแฟตกพื้นนะจ๊ะนายจ๋า!",
        "lucky_drink": "ไอซ์ คาราเมล มัคคิอาโต (หวาน 100% ไปเลยจ้ะ)",
        "tip": "สั่งหวานฉ่ำๆ ชดเชยความหวานที่ขาดหายไปในชีวิตจริงนะจ๊ะนายจ๋า",
        "color": "#CBA258",
        "image_url": "https://blob.starbucks.co.th/publicproduct26/home-banner-1784217494665.jpg"
    },
    {
        "topic": "💰 ดวงการเงิน & มหาราชารวยล้นฟ้า",
        "fortune": "เงินในกระเป๋าของนายจ๋าพร้อมไหลออกดั่งสายน้ำคงคา แต่ดาวสะสมในแอป Starbug จะพุ่งกระฉูดระดับเศรษฐีมุมไบนะจ๊ะนายจ๋า!",
        "lucky_drink": "กรีนที ครีม แฟรปปูชิโน่ (เพิ่มวิปครีมล้นๆ)",
        "tip": "อย่าคิดมากนะจ๊ะ เงินหาใหม่ได้ แต่กาแฟอร่อยสะบัดไม่ได้มีทุกวันจ้ะนายจ๋า",
        "color": "#006241",
        "image_url": "https://blob.starbucks.co.th/publicproduct26/home-banner-1784517024412.png"
    },
    {
        "topic": "🧘 ดวงสุขภาพ & พลังกายภารตะ",
        "fortune": "ร่างกายนายจ๋าต้องการนอนพักผ่อน แต่จิตวิญญาณบอกว่า 'ลุกขึ้นมาเต้นสู้ต่อสิพวก!' กาแฟ 1 แก้วนี้จะช่วยต่ออายุขัยอีก 4 ชั่วโมงนะจ๊ะ!",
        "lucky_drink": "โคลด์ บรูว์ ไนโตร (Nitro Cold Brew เข้มทะลุปอด)",
        "tip": "จิบช้าๆ หายใจเข้าลึกๆ แล้วท่องว่า 'เดี๋ยวก็ได้นอนแล้ว (ตอนชาติหน้านะจ๊ะนายจ๋า)'",
        "color": "#2D2926",
        "image_url": "https://blob.starbucks.co.th/publicproduct26/home-banner-1784217494663.jpg"
    }
]

SECRET_RECIPES = [
    {
        "title": "👳‍♂️ สูตร 'ดอลลี่ ชัยวาลา ชงทะลุเมฆ' (The 45-Degree Flying Shot)",
        "base": "Cold Brew ขนาด Venti",
        "custom": "+ Espresso 3 ช็อต + ซอสไวท์ช็อกโกแลต 2 ปั๊ม + โฟมนมสะบัด 45 องศา",
        "price_est": 225,
        "effect": "⚡ ตาสว่างยาวนานทะลุถึงวันพรุ่งนี้ หัวใจเต้นเป็นจังหวะเพลงบอลลีวูดเลยนะจ๊ะนายจ๋า!",
        "script_to_order": "นายจ๋า ขอ Cold Brew Venti เพิ่ม 3 ช็อต วันนี้ข้าพเจ้ามีนัดไฟท์กับเดดไลน์จ้ะ!",
        "image_url": "https://blob.starbucks.co.th/publicproduct26/home-banner-1784217494661.jpg"
    },
    {
        "title": "🦄 สูตร 'มหาราชาน้ำตาลสะท้านโลกา'",
        "base": "Green Tea Cream Frappuccino",
        "custom": "+ Java Chip + ผงมัทฉะเบิ้ล 4 ช้อน + ราดซอสคาราเมลรอบแก้ว + วิปครีมพูนๆ",
        "price_est": 230,
        "effect": "🌈 อารมณ์ดีระดับมหาราชา ยิ้มแป้นสะบัดส่าหรีได้ทั้งวันแม้โดนหัวหน้าบ่นนะจ๊ะ!",
        "script_to_order": "นายจ๋า ขอชาเขียวปั่น ใส่จาวาชิพ ผงมัทฉะ 4 ช้อน วิปแน่นๆ คาราเมลท่วมๆ นะจ๊ะ!",
        "image_url": "https://blob.starbucks.co.th/publicproduct26/home-banner-1784517024412.png"
    },
    {
        "title": "💸 สูตร 'เศรษฐีมุมไบเดินช้อปปิ้ง' (Mumbai Billionaire)",
        "base": "Iced Shaken Hibiscus Tea",
        "custom": "+ เติมน้ำเชื่อมวนิลา + เปลี่ยนเป็นนมโอ๊ต + ฟองนมโคลด์โฟมด้านบน",
        "price_est": 215,
        "effect": "✨ ดื่มแล้วรัศมีความรวยเปล่งประกาย คนในคิวข้างหลังต้องยกมือไหว้ด้วยความเคารพนะจ๊ะ",
        "script_to_order": "นายจ๋า ขอฮิบิสคัสทีเย็น ใส่วนิลาไซรัป ท็อปด้วยโอ๊ตมิลค์โคลด์โฟม แก้วใหญ่สุดเลยนะจ๊ะ!",
        "image_url": "https://blob.starbucks.co.th/publicproduct26/home-banner-1784517025843.jpg"
    },
    {
        "title": "🥗 สูตร 'ไดเอทแบบภารตะหลอกตัวเอง' (Guilty Free Diet)",
        "base": "Iced Americano Grande",
        "custom": "+ สั่งหวาน 0% ไม่ใส่น้ำตาล แต่สั่งแกล้มกับ 'แฮมชีสครัวซองต์' ชิ้นโต!",
        "price_est": 225,
        "effect": "🧘 รู้สึกผอมลง 50% ทันทีที่สั่งหวาน 0% ส่วนแคลจากครัวซองต์ถือว่าพระเจ้าประทานมานะจ๊ะนายจ๋า!",
        "script_to_order": "อเมริกาโน่เย็น ไม่หวานเลยนะจ๊ะนายจ๋า... แล้วขอครัวซองต์แฮมชีสอบร้อนๆ เพิ่มชิ้นนึงด้วยจ้ะ!",
        "image_url": "https://blob.starbucks.co.th/publicproduct26/ham-cheddar-croissant-1777715237936.png"
    }
]

BARISTA_ROASTS = [
    "👳‍♂️ แหม... นายจ๋าสั่งกาแฟหวาน 0% แต่ยืนจ้องตู้เค้กตาเป็นมัน บาริสต้าแอบเห็นนะจ๊ะนายจ๋า! 🤣",
    "😴 นายจ๋าเดินเข้ามาสภาพเหมือนวิญญาณหลุดออกจากร่างไปแล้ว 90% เดี๋ยวบาริสต้าสะบัดกาน้ำชงกาแฟกู้ชีพให้นะจ๊ะ!",
    "🥤 สั่งชาเขียวหวาน 0% แต่นมข้นกับผงมัทฉะในหม้อต้มหวานเจี๊ยบอยู่แล้ว... แต่ไม่เป็นไร บาริสต้าจะไม่บอกเทรนเนอร์ของนายจ๋านะจ๊ะ!",
    "💸 สั่งกาแฟแก้วละเกือบสองร้อยได้สบายๆ แต่ต่อราคาค่ามอเตอร์ไซค์ 5 บาท... เท่ระดับมหาราชาจริงๆ นะจ๊ะนายจ๋า!",
    "📱 ถ่ายรูปแก้วกาแฟลงสตอรี่ IG ไป 8 มุม 15 นาที น้ำแข็งละลายหมดแล้วแต่ฟิลเตอร์สตอรี่ยังไม่เสร็จ! แซวเล่นนะจ๊ะนายจ๋า 💚"
]


def get_random_fortune() -> Dict[str, Any]:
    """Returns a randomized Indian Chaiwala fortune reading."""
    return random.choice(FORTUNES)


def get_random_secret_recipe() -> Dict[str, Any]:
    """Returns a randomized Indian chaos secret recipe."""
    return random.choice(SECRET_RECIPES)


def get_random_barista_roast() -> str:
    """Returns a funny Indian chaiwala barista roast."""
    return random.choice(BARISTA_ROASTS)
