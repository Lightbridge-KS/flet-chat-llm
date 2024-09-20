from dataclasses import dataclass
import flet as ft

@dataclass
class Message:
    user_name: str
    text: str
    message_type: str


    
class ChatMessage(ft.UserControl):
    def __init__(self, message: Message):
        super().__init__()
        self.message = message
    
    def build(self):
        circle_avatar = ft.CircleAvatar(
            content=ft.Text(self.get_initials(self.message.user_name)),
            color=ft.colors.WHITE,
            bgcolor=self.get_avatar_color(self.message.user_name),
        )
        msg_bubble = ft.Container(
                                ft.Markdown(
                                        self.message.text, selectable=True, 
                                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                                        code_theme=ft.MarkdownCodeTheme.GITHUB
                                ),
                                bgcolor=ft.colors.GREEN_200,
                                theme_mode=ft.ThemeMode.LIGHT,
                                border_radius=10,
                                margin=10,
                                padding=10,
                    )
        
        
        rr = ft.ResponsiveRow(
            controls = [
                ft.Column(col=1, controls=[circle_avatar]),
                ft.Column(col=10,
                    controls = [ft.Text(self.message.user_name, weight="bold"),
                    msg_bubble],
                    tight=True,
                    spacing=5,
                )
            ],
            vertical_alignment = ft.CrossAxisAlignment.START,
        )
        
        return rr
    
    
    @staticmethod
    def get_initials(user_name: str):
        if user_name:
            return user_name[:1].capitalize()
        else:
            return "User"  # or any default value you prefer


    @staticmethod
    def get_avatar_color(user_name: str):
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
    





# class ChatMessage(ft.ResponsiveRow):
#     def __init__(self, message: Message):
#         super().__init__()
#         self.vertical_alignment = ft.CrossAxisAlignment.START
        
#         circle_avatar = ft.CircleAvatar(
#             content=ft.Text(self.get_initials(message.user_name)),
#             color=ft.colors.WHITE,
#             bgcolor=self.get_avatar_color(message.user_name),
#         )
#         msg_bubble = ft.Container(
#                                 ft.Markdown(
#                                         message.text, selectable=True, 
#                                         extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
#                                         code_theme=ft.MarkdownCodeTheme.GITHUB
#                                 ),
#                                 bgcolor=ft.colors.GREEN_200,
#                                 theme_mode=ft.ThemeMode.LIGHT,
#                                 width=600,
#                                 border_radius=10,
#                                 margin=10,
#                                 padding=10,
#         )
        
#         self.controls = [
#             circle_avatar,
#             ft.Column(
#                 [ft.Text(message.user_name, weight="bold"),
#                 msg_bubble],
#                 tight=True,
#                 spacing=5,
#             ),
#         ]

#     @staticmethod
#     def get_initials(user_name: str):
#         if user_name:
#             return user_name[:1].capitalize()
#         else:
#             return "User"  # or any default value you prefer
    
#     @staticmethod
#     def get_avatar_color(user_name: str):
#         colors_lookup = [
#             ft.colors.AMBER,
#             ft.colors.BLUE,
#             ft.colors.BROWN,
#             ft.colors.CYAN,
#             ft.colors.GREEN,
#             ft.colors.INDIGO,
#             ft.colors.LIME,
#             ft.colors.ORANGE,
#             ft.colors.PINK,
#             ft.colors.PURPLE,
#             ft.colors.RED,
#             ft.colors.TEAL,
#             ft.colors.YELLOW,
#         ]
#         return colors_lookup[hash(user_name) % len(colors_lookup)]