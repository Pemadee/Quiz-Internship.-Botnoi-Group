from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, QuickReply, QuickReplyButton, CarouselTemplate, CarouselColumn, PostbackAction, MessageAction, URIAction
from linebot.exceptions import InvalidSignatureError


LINE_CHANNEL_ACCESS_TOKEN = "xFdnUH6bkKuOEsJXQuzTg9XSDzIXPVJdnIPdU5VYQvq+XA79tLDVcjCPakhnx4HJsfqREfINviF6pZX3rQbfxZ657z5IEIRUV+wSy6CKoJkAq1ptNykeQl5d7zvUgTnP9+gsPQ3GxsNkIy7w8i74MgdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "520d3f0cf3017a61eef01990cb91a257"

app = FastAPI()
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.post("/webhook")
async def callback(request: Request):
    signature = request.headers['X-Line-Signature']
    body = await request.body()

    try:
        handler.handle(body.decode('utf-8'), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event: MessageEvent):
    user_message = event.message.text
    if user_message.lower() == "hello":
        reply_text = TextSendMessage(text="Hello!")
        line_bot_api.reply_message(event.reply_token, reply_text)
    
    elif user_message == "text":
        reply_text = TextSendMessage(text="Hello! This is a text message.")
        line_bot_api.reply_message(event.reply_token, reply_text)

    elif user_message == "button":
        buttons_template = TemplateSendMessage(
            alt_text="Button Template",
            template=ButtonsTemplate(
                title="Menu",
                text="Please select",
                actions=[
                    MessageAction(label="Say hello", text="Hello!"),
                    URIAction(label="Visit website", uri="https://www.facebook.com/botnoi.academy")
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)

    elif user_message == "quickreply":
        quick_reply = TextSendMessage(
            text="Choose one:",
            quick_reply=QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="Option 1", text="You chose option 1")),
                QuickReplyButton(action=MessageAction(label="Option 2", text="You chose option 2"))
            ])
        )
        line_bot_api.reply_message(event.reply_token, quick_reply)

    elif user_message == "carousel":
        carousel_template = TemplateSendMessage(
            alt_text="Carousel Template",
            template=CarouselTemplate(columns=[
                CarouselColumn(
                    thumbnail_image_url="https://scontent.fphs1-1.fna.fbcdn.net/v/t39.30808-6/416316406_122118852836133868_7060942155565883647_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=wd_WNizJL20Q7kNvgEdr4LJ&_nc_ht=scontent.fphs1-1.fna&_nc_gid=AlHgzFNo3meGWEYx7aGsmCl&oh=00_AYCYmsurB58T4i1SXi0CPP9bQUSOHAInGoeQDOadBCH6Mg&oe=671012C6",
                    title="Option 1",
                    text="Facebook",
                    actions=[
                        MessageAction(label="Select 1", text="You selected option 1"),
                        URIAction(label="Visit website", uri="https://www.facebook.com/botnoi.academy")
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url="https://framerusercontent.com/images/1aOghRYsIDGzNhrwTy3tcerX2c.png?scale-down-to=1024",
                    title="Option 2",
                    text="Website",
                    actions=[
                        MessageAction(label="Select 2", text="You selected option 2"),
                        URIAction(label="Visit website", uri="https://botnoigroup.com/th/?fbclid=IwZXh0bgNhZW0CMTAAAR3QQn-f27tVBOipErJBn95qu29K-vwDrLO4qpO3hz120lPsDkNHmjvBwf4_aem_LbYJpR0UUfL407SW4NoSTw")
                    ]
                )
            ])
        )
        line_bot_api.reply_message(event.reply_token, carousel_template)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# command : uvicorn main:app --reload --host 0.0.0.0 --port 8000
# command : ngrok http 8000