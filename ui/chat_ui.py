import html
import re

import streamlit as st

user_avatar='https://preview.redd.it/d1nhcalbqn1b1.png?width=511&format=png&auto=webp&s=7084cb3777d628927cb623e735c9a0d2de5c5bf7'
bot_avatar='https://upload.wikimedia.org/wikipedia/commons/a/a1/Greek_lc_alpha.svg'
# user_avatar='assets/investor_avatar.jpg'
# bot_avatar='assets/robot.jpg'

def format_message(text):
    """
    This function is used to format the messages in the chatbot UI.

    Parameters:
    text (str): The text to be formatted.
    """
    text_blocks = re.split(r"```[\s\S]*?```", text)
    code_blocks = re.findall(r"```([\s\S]*?)```", text)

    text_blocks = [html.escape(block) for block in text_blocks]

    formatted_text = ""
    for i in range(len(text_blocks)):
        formatted_text += text_blocks[i].replace("\n", "<br>")
        if i < len(code_blocks):
            formatted_text += f'<pre style="white-space: pre-wrap; word-wrap: break-word;"><code>{html.escape(code_blocks[i])}</code></pre>'

    return formatted_text

def message_func(message):
    """
    This function is used to display the messages in the chatbot UI.

    Parameters:
    text (str): The text to be displayed.
    """
    text=message['content']
    if message['role'] == 'user':
            message_alignment = "flex-end"
            message_bg_color = "linear-gradient(135deg, #00B2FF 0%, #006AFF 100%)"
            avatar_class = "user-avatar"
            st.write(
            f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                    <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%; font-size: 14px;">
                        {text} \n </div>
                    <img src="{user_avatar}" class="{avatar_class}" alt="avatar" style="width: 50px; height: 50px;" />
                </div>
                """,
            unsafe_allow_html=True,
        )

    elif message['role'] == 'assistant':
        message_alignment = "flex-start"
        message_bg_color = "#D3D3D3"
        avatar_class = "bot-avatar"
        text = format_message(text)

        st.write(
            f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                    <img src="{bot_avatar}" class="{avatar_class}" alt="avatar" style="width: 50px; height: 50px;" />
                    <div style="background: {message_bg_color}; color: black; border-radius: 20px; padding: 10px; margin-right: 5px; margin-left: 5px; max-width: 75%; font-size: 14px;">
                        {text} \n </div>                    
                </div>
                """,
            unsafe_allow_html=True,
        )
