import flet as ft
import translate


class LangDropDown(ft.Dropdown):
    def __init__(self, lang_list, on_change, hint_text):
        super().__init__(
            padding=0,
            options=[
                # ft.dropdown.Option(lang_list.keys()[x]) for x in range(len(lang_list))
                ft.dropdown.Option(list(lang_list.keys())[x]) for x in range(len(lang_list))
            ],
            width=180,
            border_width=0,
        )
        self.on_change = on_change
        self.hint_text = hint_text


class SourceText(ft.Container):
    def __init__(self, translate_clicked):
        super().__init__(
            expand=True,
            border=ft.border.all(3, color="blue"),
            border_radius=6,
            padding=10,
            margin=ft.margin.only(top=10, left=0, right=0, bottom=10),
        )

        # currently not set (auto-detect the source language)
        self.choose_lang = LangDropDown(
            lang_list=translate.source_languages,
            on_change=self.source_lang_chosen,
            hint_text="Transte from..",
        )

        self.text = ft.TextField(
            content_padding=ft.padding.only(top=0, left=10, right=10, bottom=15),
            multiline=True,
            max_lines=4,
            autofocus=True,
            border=ft.InputBorder.NONE,
        )

        self.translate_clicked = translate_clicked

        self.content = ft.Column(
            spacing=5,
            controls=[
                # ft.Row(
                #     wrap=True,
                #     controls=[
                #         self.choose_lang,
                #         ft.FilledTonalButton(text="Paste", on_click=self.paste_on_click),
                #     ],
                #     vertical_alignment=ft.CrossAxisAlignment.END,
                # ),
                self.text,
                ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.icons.CLEAR, tooltip="Clear text", on_click=self.clear_on_click),
                        ft.FilledTonalButton(text="Paste", on_click=self.paste_on_click),
                        ft.FilledButton(text="Translate", tooltip="Translate into all selected languages", on_click=self.translate_clicked)
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ]
        )

    def source_lang_chosen(self, e):
        source_lang = self.choose_lang.value
        print(f"{source_lang} ({lang_list.lang_code[source_lang]}) is chosen as source language")

    def paste_on_click(self, e):
        get_paste = self.page.get_clipboard()
        print(f"Text pasted: {get_paste}")
        self.text.value += get_paste
        self.update()

    def clear_on_click(self, e):
        print(f"Textfield cleared")
        self.text.value = ""
        self.update()


class NumberOfLangMenu(ft.Container):
    def __init__(self, on_change):
        super().__init__(
            width=300,
            height=35,
            border=ft.border.all(0),
        )

        self.on_change = on_change

        self.choose_num_lang = ft.Dropdown(
            fill_color="transparent",

            on_change=self.on_change,
            hint_text="Number of Target Languages",
            options=[
                # ft.dropdown.Option(x+1) for x in range(4)
                ft.dropdown.Option("1"),
                ft.dropdown.Option("2"),
                ft.dropdown.Option("3 (default)"),
                ft.dropdown.Option("4"),
            ],
            alignment=ft.alignment.center,
            content_padding=ft.padding.only(top=0, left=10, right=10, bottom=0),
            # width=80,
            border_width=0,
        )

        self.content = ft.Row(
            controls=[
                self.choose_num_lang
            ],
        )


class TranslatedText(ft.Container):
    def __init__(self, lang_num, target_lang, results):
        super().__init__(
            # height=150,
            border=ft.border.all(1),
            border_radius=6,
            margin=ft.margin.only(top=10, left=30, right=0, bottom=10),
        )

        self.lang_num = lang_num
        self.target_lang = target_lang
        self.results = results

        self.choose_lang = LangDropDown(
            lang_list=translate.target_languages,
            on_change=self.target_lang_chosen,
            hint_text="Transte into..",
        )

        self.text = ft.TextField(
            content_padding=ft.padding.only(top=0, left=10, right=10, bottom=15),
            multiline=True,
            autocorrect=True,
            max_lines=4,
            border=ft.InputBorder.NONE,
            value=self.results,
        )

        self.copy_button = ft.Container(
            content=ft.FilledTonalButton(text="Copy", on_click=self.copy_on_click),
            margin=ft.margin.only(right=20, bottom=10),
        )

        self.content = ft.Column(
            spacing=5,
            controls=[
                self.choose_lang,
                self.text,
                ft.Row(
                    controls=[
                        self.copy_button
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ]
        )

    def target_lang_chosen(self, e):
        self.target_lang = self.choose_lang.value
        print(f"{self.choose_lang.value} is chosen as target language {self.lang_num}")

    def copy_on_click(self, e):
        get_text = self.text.value
        self.page.set_clipboard(get_text)
        print("Text copied")


class Landing(ft.Container):
    def __init__(self):
        super().__init__(
            theme=ft.Theme(color_scheme_seed="blue"),
        )

        self.title = ft.Text(
            value="Poly",
            size=30
        )

        self.subtitle = ft.Text(
            value="Multi-lingual translation",
            size=15
        )

        self.content = ft.Column(
            controls=[
                self.title, 
                self.subtitle
            ],
            expand=True
        )


### APP CLASS ###
class Polygloo(ft.UserControl):
    def __init__(self):
        super().__init__()

        # self.auth_key = '65523bc2-d6ba-426e-b605-6646a6d1bc2c'
        # self.translator = deepl.Translator(self.auth_key)

        self.number_of_target_lang = 3
        self.source_lang = None
        self.target_lang = [[] for i in range(self.number_of_target_lang)]
        self.source_text = ""
        self.results = ["" for i in range(self.number_of_target_lang)]

        self.source_panel = ft.Container(
                                content=SourceText(translate_clicked=self.translate_all_on_click),
                            )

        # self.number_of_target_lang = number_of_target_lang
                  
        self.target_panel = ft.Column(
            controls=[TranslatedText(x, self.target_lang[x], self.results[x]) for x in range(self.number_of_target_lang)]
        )
        
        self.num_lang_menu = ft.Container(
            content=NumberOfLangMenu(self.num_lang_selected),
            alignment=ft.alignment.bottom_right,
        )

        self.controls=[
            ft.Container(
                padding=ft.padding.only(left=20, right=20),
                content=ft.Column(
                    controls=[
                        Landing(),

                        # Source text
                        self.source_panel,

                        # Choose Number of Target Languages
                        self.num_lang_menu,

                        # Translation texts
                        ft.Container(
                            content=self.target_panel,
                        ),  
                    ]
                )
                )
        ]
        
    def update_target_panel(self):
        self.target_panel.controls = [TranslatedText(x, self.target_lang[x], self.results[x]) for x in range(self.number_of_target_lang)]

    def num_lang_selected(self, e):        
        match self.num_lang_menu.content.choose_num_lang.value:
            case "1": self.number_of_target_lang = 1
            case "2": self.number_of_target_lang = 2
            case "3 (default)": self.number_of_target_lang = 3
            case "4": self.number_of_target_lang = 4
        
        self.target_panel.controls.clear()
        self.target_lang = [[] for i in range(self.number_of_target_lang)]
        self.results = ["" for i in range(self.number_of_target_lang)]
        self.update_target_panel()

        self.update()

    def translate_all_on_click(self, e):
        source_text = self.source_panel.content.text.value
        results = self.results
        target_lang = self.target_lang
        target_panel = self.target_panel
        print(f"source text: {source_text}")

        if source_text:
            for i, panel in enumerate(target_panel.controls):
                if panel.target_lang:
                    results[i] = translate.translator.translate_text(source_text, target_lang=translate.target_languages[panel.target_lang])
                    panel.text.value = results[i]
                    print(f"translation: {panel.target_lang} {translate.target_languages[panel.target_lang]} - {results[i].text}")

        self.update()



def main(page: ft.Page):
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.scroll=ft.ScrollMode.ADAPTIVE
    page.update()

    # "Snackbar" - DeprecationWarning: snack_bar is deprecated in version 0.23.0
    # page.snack_bar= ft.SnackBar(
    #     content=ft.Text("Text copied!"),
    #     duration=1000,
    #     behavior=ft.SnackBarBehavior.FLOATING,
    #     width=120,
    # )

    # render Layout objects
    app = Polygloo()
    page.add(ft.SafeArea(app))


ft.app(main)
