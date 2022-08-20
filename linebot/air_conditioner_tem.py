from linebot.models import (QuickReply, QuickReplyButton, PostbackAction)

airConditionerTem_reply = QuickReply(
    items=[
        QuickReplyButton(
            action=PostbackAction(label="18°C", data="18°C")
        ),
        QuickReplyButton(
            action=PostbackAction(label="19°C", data="19°C")
        ),
        QuickReplyButton(
            action=PostbackAction(label="20°C", data="20°C")
        ),
        QuickReplyButton(
            action=PostbackAction(label="21°C", data="21°C")
        ),
        QuickReplyButton(
            action=PostbackAction(label="22°C", data="22°C")
        ),
        QuickReplyButton(
            action=PostbackAction(label="23°C", data="23°C")
        ),
        QuickReplyButton(
            action=PostbackAction(label="24°C", data="24°C")
        ),
        QuickReplyButton(
            action=PostbackAction(label="25°C", data="25°C")
        ),
        QuickReplyButton(
            action=PostbackAction(label="26°C", data="26°C")
        ),
        QuickReplyButton(
            action=PostbackAction(label="27°C", data="27°C")
        ),
        QuickReplyButton(
            action=PostbackAction(label="28°C", data="28°C")
        ),
        QuickReplyButton(
            action=PostbackAction(label="29°C", data="29°C")
        ),
        QuickReplyButton(
            action=PostbackAction(label="30°C", data="30°C")
        )
    ]
)
