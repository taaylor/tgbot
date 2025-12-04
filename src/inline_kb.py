from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


class KeyboardsApp:

    @property
    def my_contacts(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Мой GitHub",
                        url="https://github.com/taaylor/",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Мой Telegram",
                        url="https://t.me/taaaylor/",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Стартап который развиваю",
                        web_app=WebAppInfo(url="https://sovlium.ru/"),
                    )
                ],
            ]
        )

    @property
    def entertainments(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Испытать удачу",
                        callback_data="lucky_game",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Сгенерировать случайного пользователя",
                        callback_data="random_human",
                    )
                ],
            ]
        )

    @property
    def hh_main(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Поиск вакансий",
                        callback_data="hh_vacancies",
                    )
                ]
            ],
        )

    @property
    def hh_vacancies(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Вернуться",
                        callback_data="hh_main",
                    )
                ],
            ]
        )


keyboards: KeyboardsApp = KeyboardsApp()
