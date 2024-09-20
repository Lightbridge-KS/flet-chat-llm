import flet as ft
from dataclasses import dataclass

from assistantLocal01 import AssistantLocal01

@dataclass
class Message:
    user_name: str
    text: str
    message_type: str




class ChatView(ft.ListView):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.spacing = 10
        self.auto_scroll = True
        self.clip_behavior = ft.ClipBehavior.ANTI_ALIAS

        


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name, weight="bold"),
                            ft.Container(
                                ft.Markdown(
                                        message.text, selectable=True, 
                                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                                        code_theme=ft.MarkdownCodeTheme.GITHUB
                                ),
                                bgcolor=ft.colors.GREEN_200,
                                theme_mode=ft.ThemeMode.LIGHT,
                                width=600,
                                border_radius=10,
                                margin=10,
                                padding=10,
                            )
                    
                    
                ],
                tight=True,
                spacing=5,
            ),
        ]

    def get_initials(self, user_name: str):
        if user_name:
            return user_name[:1].capitalize()
        else:
            return "User"  # or any default value you prefer

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    # Title
    page.title = "LLM Chat"
    page.window_min_width = 450
    page.window_width = 550
    page.window_min_height = 500
    page.window_height = 600
    # App Bar
    page.appbar = ft.CupertinoAppBar(
        leading=ft.Icon(ft.icons.PALETTE),
        bgcolor=ft.colors.SURFACE_VARIANT,
        middle=ft.Text("LLM Chat", weight=ft.FontWeight.BOLD),
        trailing=ft.IconButton(icon=ft.icons.BRIGHTNESS_2_OUTLINED, tooltip="Toggle theme", on_click=lambda e: toggle_theme(page))
    )
    
    # Creating LLM Assistance
    assistantLocal01 = AssistantLocal01()

    def join_chat_click(e):
        # If not provide give Anonymous name
        if not join_user_name.value:
            join_user_name.value = "User"
        
        page.session.set("user_name", join_user_name.value)
        page.dialog.open = False
        new_message.prefix =ft.Text(" " * 2) # ft.Text(f"{join_user_name.value}: ")
        page.pubsub.send_all(
            Message(
                user_name=join_user_name.value,
                text=f"{join_user_name.value} has joined the chat.",
                message_type="login_message",
            )
        )
        page.update()

    def send_message_click(e):
        if new_message.value != "":
            
            ## Send User Message
            page.pubsub.send_all(
                Message(
                    page.session.get("user_name"),
                    new_message.value,
                    message_type="chat_message",
                )
            )
            ## Asking user to Wait till we get our response
            ### [TODO]: Make it stream !!!
            page.pubsub.send_all(
                Message(
                    user_name="AI", 
                    text="AI is generating", 
                    message_type="generate_message"
                )
            )
            
            ## Fetching the AI response get_response
            ai_response = assistantLocal01.get_response(str(new_message.value))
            ## Sent AI Message
            page.pubsub.send_all(
                Message(
                    "AI", 
                    str(ai_response).lstrip(), 
                    message_type="chat_message"
                )
            )
            
            new_message.value = ""
            new_message.focus()
            page.update()

    def on_message(message: Message):
        match message.message_type:
            case "chat_message":
                m = ChatMessage(message)
            case "login_message":
                m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
            case "generate_message":
                m = ft.Text(message.text, italic=True, color=ft.colors.BLACK26, size=12)
        
        chat.controls.append(m)
        page.update()


    page.pubsub.subscribe(on_message)

    # A dialog asking for a user display name
    join_user_name = ft.TextField(
        label="Enter your name",
        autofocus=True,
        on_submit=join_chat_click,
    )
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([join_user_name], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text="Join chat", on_click=join_chat_click)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Chat messages
    chat = ChatView()

    # A new message entry form
    new_message = ft.TextField(
        hint_text="Message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=10, # 5
        border_radius=30,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    # Add everything to the page
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5, 
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                ),
            ]
        ),
    )


def toggle_theme(page: ft.Page):
    if page.theme_mode == ft.ThemeMode.LIGHT:
        page.theme_mode = ft.ThemeMode.DARK
        page.appbar.trailing = ft.IconButton(icon=ft.icons.DARK_MODE_OUTLINED, tooltip="Toggle theme", on_click=lambda e: toggle_theme(page))
        
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
        page.appbar.trailing = ft.IconButton(icon=ft.icons.BRIGHTNESS_5, tooltip="Toggle theme", on_click=lambda e: toggle_theme(page))
    # page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
    page.update()

ft.app(target=main)