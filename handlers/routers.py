from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, callback_data
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
load_dotenv()


router = Router()

class User_data(StatesGroup):
    name = State()
    pin = State()
    main_valut = State()
    revenues = State()
    expenses = State()
    new_revenue_category = State()
    new_expense_category = State()
    change_name = State()
    change_pin_old = State()
    change_pin_new = State()
    confirm_pin = State()

class revenues_category(StatesGroup):
    now = State()
    zp = State()
    tipo_zp = State()
    prize = State()
    duty = State()
    xz = State()

class expenses_category(StatesGroup):
    ex_food = State()
    ex_transport = State()
    ex_home = State()
    ex_shopping = State()
    ex_comms = State()
    ex_fun = State()
    ex_subs = State()
    ex_credit = State()
    ex_xz = State()


currency_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="₸ Тенге", callback_data="currency_KZT"),
            InlineKeyboardButton(text="₽ Рубль", callback_data="currency_RUB")
        ],
        [
            InlineKeyboardButton(text="$ Доллар", callback_data="currency_USD"),
            InlineKeyboardButton(text="€ Евро", callback_data="currency_EUR")
        ]
    ]
)

def revenues_kategory(custom_categories: dict) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="💸 Зарплата", callback_data="zp"),
            InlineKeyboardButton(text="💲 Подработка", callback_data="tipo_zp")
        ],
        [
            InlineKeyboardButton(text="🎁 Подарок", callback_data="prize"),
            InlineKeyboardButton(text="✔ Долг", callback_data="duty")
        ],
        [
            InlineKeyboardButton(text="❓ Забытое", callback_data="xz"),
        ],
    ]
    names = list(custom_categories.keys())
    for i in range(0, len(names), 2):
        row = [InlineKeyboardButton(text=f"📌 {n}", callback_data=f"customrev:{n}") for n in names[i:i+2]]
        keyboard.append(row)

    keyboard.append([
        InlineKeyboardButton(text="➕ Создать новую категорию", callback_data="new_kategory"),
        InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_get_revenues")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def expenses_kategory(custom_categories: dict) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="🍔 Еда", callback_data="ex_food"),
            InlineKeyboardButton(text="🚌 Транспорт", callback_data="ex_transport")
        ],
        [
            InlineKeyboardButton(text="🏠 Жильё", callback_data="ex_home"),
            InlineKeyboardButton(text="🛒 Покупки", callback_data="ex_shopping")
        ],
        [
            InlineKeyboardButton(text="📱 Связь", callback_data="ex_comms"),
            InlineKeyboardButton(text="🎮 Развлечения", callback_data="ex_fun")
        ],
        [
            InlineKeyboardButton(text="💳 Подписки", callback_data="ex_subs"),
            InlineKeyboardButton(text="🏦 Кредиты", callback_data="ex_credit")
        ],
        [
            InlineKeyboardButton(text="❓ Забытое", callback_data="ex_xz")
        ],
    ]
    names = list(custom_categories.keys())
    for i in range(0, len(names), 2):
        row = [InlineKeyboardButton(text=f"📌 {n}", callback_data=f"customex:{n}") for n in names[i:i+2]]
        keyboard.append(row)

    keyboard.append([
        InlineKeyboardButton(text="➕ Создать новую категорию", callback_data="ex_new_kategory"),
        InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_get_expenses")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💰 Ввести доход", callback_data="revenues"),
            InlineKeyboardButton(text="💸 Ввести расход", callback_data="expenses")
        ],
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="stats"),
            InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")
        ],
    ]
)

settings_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👤 Изменить имя", callback_data="set_name"),
            InlineKeyboardButton(text="🔐 Изменить PIN", callback_data="set_pin")
        ],
        [
            InlineKeyboardButton(text="🧹 Сбросить статистику", callback_data="reset_stats"),
            InlineKeyboardButton(text="🗑 Удалить все данные", callback_data="delete_all")
        ],
        [
            InlineKeyboardButton(text="⬅ В меню", callback_data="back_to_menu")
        ],
    ]
)


cancel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data="settings")]
    ]
)

@router.message(Command('start'))
async def start(message: Message, state: FSMContext):

    await state.set_state(User_data.name)
    await state.update_data(
        custom_revenue_categories={},
        custom_expense_categories={},
    )
    await state.update_data(onboarding_done=False,
                            revenues=0,
                            expenses=0,
                            zp=0,
                            tipo_zp=0,
                            xz=0,
                            duty=0,
                            prize=0,
                            now=0,
                            )

    await state.update_data(
        revenues=0, expenses=0,
        ex_zp=0, ex_tipo_zp=0, ex_xz=0, ex_duty=0, ex_prize=0, ex_now=0,
        ex_food=0, ex_transport=0, ex_home=0, ex_shopping=0,
        ex_comms=0, ex_fun=0, ex_subs=0, ex_credit=0,
    )

    await message.answer("👋 Добро пожаловать в CashPilot!\n\n"
       "Я помогу вам вести учёт доходов и расходов, контролировать бюджет и следить за вашими финансами.\n\n"
       "Для начала давайте создадим ваш профиль.\n\n" 
       "📝 Введите ваше имя:")

@router.message(Command('menu'))
async def menu(message: Message):
    await message.answer("📋 Главное меню:", reply_markup=menu_kb)

@router.callback_query(F.data == "revenues")
async def revenues(callback: CallbackQuery, state: FSMContext):
    await state.update_data(now=0)
    await state.set_state(User_data.revenues)
    data = await state.get_data()
    main_valut = data["main_valut"]
    name = data["name"]

    await callback.message.answer(f"{name} введите доходы за сегодняшний день")

@router.callback_query(F.data == "expenses")
async def expenses(callback: CallbackQuery, state: FSMContext):
    await state.update_data(ex_now=0)
    await state.set_state(User_data.expenses)
    data = await state.get_data()
    main_valut = data["main_valut"]
    name = data["name"]
    await callback.message.answer(f"{name} введите расходы за сегодняшний день")

@router.message(User_data.name)
async def get_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)

    await message.answer(f"Приятно познакомиться, {name}! 👋\n\n"
    "🔐 Теперь придумайте PIN-код (4–6 цифр).\n\n"
    "Он потребуется для подтверждения важных действий, таких как:\n"
    "• удаление всех данных;\n"
    "• изменение настроек безопасности;\n"
    "• восстановление профиля.\n\n"
    "⚠️ Обязательно запомните PIN-код.\n\n"
    "Введите PIN-код:")

    await state.set_state(User_data.pin)

@router.message(User_data.pin)
async def get_pin(message: Message, state: FSMContext):
    pin = message.text

    if not pin.isdigit():
        await message.answer("❌ PIN-код должен состоять только из цифр.")
        return

    if len(pin) < 4:
        await message.answer("❌ PIN-код должен содержать минимум 4 цифры.")
        return

    if len(pin) > 6:
        await message.answer("❌ PIN-код должен содержать не болше 6 цифр.")
        return

    await state.update_data(pin=pin)

    await message.answer("💱 Отлично! Теперь выберите основную валюту.\n\n"
    "Все доходы, расходы и статистика будут отображаться в выбранной валюте.\n\n"
    "При необходимости её можно изменить позже в настройках.",reply_markup=currency_kb)

@router.callback_query(F.data == "currency_KZT")
async def currency_tg(callback: CallbackQuery, state: FSMContext):
    await state.set_state(User_data.revenues)
    await state.update_data(main_valut="₸")
    data = await state.get_data()
    main_valut = data["main_valut"]
    name = data["name"]
    await callback.answer(f"✅ Валюта {main_valut} установлена")
    await callback.message.answer(f"Отлично {name}!Теперь введите доходы за сегодняшний день")

@router.callback_query(F.data == "currency_RUB")
async def currency_ru(callback: CallbackQuery, state: FSMContext):
    await state.set_state(User_data.revenues)
    await state.update_data(main_valut="₽")
    data = await state.get_data()
    main_valut = data["main_valut"]
    name = data["name"]
    await callback.answer(f"✅ Валюта {main_valut} установлена")
    await callback.message.answer(f"Отлично {name}!Теперь введите доходы за сегодняшний день")

@router.callback_query(F.data == "currency_USD")
async def currency_dl(callback: CallbackQuery, state: FSMContext):

    await state.set_state(User_data.revenues)
    await state.update_data(main_valut="$")
    data = await state.get_data()
    main_valut = data["main_valut"]
    name = data["name"]
    await callback.answer(f"✅ Валюта {main_valut} установлена")
    await callback.message.answer(f"Отлично {name}!Теперь введите доходы за сегодняшний день")


@router.callback_query(F.data == "currency_EUR")
async def currency_er(callback: CallbackQuery, state: FSMContext):

    await state.set_state(User_data.revenues)
    await state.update_data(main_valut="€")
    data = await state.get_data()
    main_valut = data["main_valut"]
    name = data["name"]
    await callback.answer(f"✅ Валюта {main_valut} установлена")
    await callback.message.answer(f"Отлично {name}!Теперь введите доходы за сегодняшний день")

@router.message(User_data.revenues)
async def get_revenues(message:Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(
            "💰 Введите сумму дохода.\n\nПожалуйста, укажите только число, без валюты и других символов.\n\n✅ Пример: 1000\n❌ Неправильно: 1000₸, 1 000 тг, тысяча")
        return
    data = await state.get_data()

    revenues = data["revenues"]
    now = data["now"]

    await state.update_data(revenues=revenues + int(message.text))
    await state.update_data(now=now + int(message.text))

    custom = data.get("custom_revenue_categories", {})
    await message.answer("Отлично!Теперь выберите категорию куда вписать эти доходы", reply_markup=revenues_kategory(custom))

@router.callback_query(F.data == "zp")
async def zp_category(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_valut = data["main_valut"]
    now = data["now"]
    zp = data["zp"]
    onboarding_done = data.get("onboarding_done", False)

    await state.update_data(zp=zp + now, now=0)
    await callback.message.answer(
        f"✅ Отлично, вы вписали {now}{main_valut} в категорию 'Зарплата'"
    )

    if onboarding_done:
        await callback.message.answer("📋 Что дальше?", reply_markup=menu_kb)
    else:
        await state.set_state(User_data.expenses)
        await callback.message.answer("Введите расходы за сегодняшний день:")

    await callback.answer()

@router.callback_query(F.data == "tipo_zp")
async def tipo_zp_category(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_valut = data["main_valut"]
    now = data["now"]
    tipo_zp = data["tipo_zp"]
    onboarding_done = data.get("onboarding_done", False)

    await state.update_data(tipo_zp=tipo_zp + now, now=0)
    await callback.message.answer(
        f"✅ Отлично, вы вписали {now}{main_valut} в категорию 'Подработка'"
    )

    if onboarding_done:
        await callback.message.answer("📋 Что дальше?", reply_markup=menu_kb)
    else:
        await state.set_state(User_data.expenses)
        await callback.message.answer("Введите расходы за сегодняшний день:")

    await callback.answer()

@router.callback_query(F.data == "prize")
async def prize_category(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_valut = data["main_valut"]
    now = data["now"]
    prize = data["prize"]
    onboarding_done = data.get("onboarding_done", False)

    await state.update_data(prize=prize + now, now=0)
    await callback.message.answer(
        f"✅ Отлично, вы вписали {now}{main_valut} в категорию 'Подарок'"
    )

    if onboarding_done:
        await callback.message.answer("📋 Что дальше?", reply_markup=menu_kb)
    else:
        await state.set_state(User_data.expenses)
        await callback.message.answer("Введите расходы за сегодняшний день:")

    await callback.answer()

@router.callback_query(F.data == "duty")
async def duty_category(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_valut = data["main_valut"]
    now = data["now"]
    duty = data["duty"]
    onboarding_done = data.get("onboarding_done", False)

    await state.update_data(duty=duty + now, now=0)
    await callback.message.answer(
        f"✅ Отлично, вы вписали {now}{main_valut} в категорию 'Долг'"
    )

    if onboarding_done:
        await callback.message.answer("📋 Что дальше?", reply_markup=menu_kb)
    else:
        await state.set_state(User_data.expenses)
        await callback.message.answer("Введите расходы за сегодняшний день:")

    await callback.answer()

@router.callback_query(F.data == "xz")
async def xz_category(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_valut = data["main_valut"]
    now = data["now"]
    xz = data["xz"]
    onboarding_done = data.get("onboarding_done", False)

    await state.update_data(xz=xz + now, now=0)
    await callback.message.answer(
        f"✅ Отлично, вы вписали {now}{main_valut} в категорию 'Забытое'"
    )

    if onboarding_done:
        await callback.message.answer("📋 Что дальше?", reply_markup=menu_kb)
    else:
        await state.set_state(User_data.expenses)
        await callback.message.answer("Введите расходы за сегодняшний день:")

    await callback.answer()


@router.callback_query(F.data == "new_kategory")
async def new_category(callback: CallbackQuery, state: FSMContext):
    await state.set_state(User_data.new_revenue_category)
    await callback.message.answer("Введите название новой категории:")
    await callback.answer()

@router.callback_query(F.data == "ex_new_kategory")
async def new_ex_category(callback: CallbackQuery, state: FSMContext):
    await state.set_state(User_data.new_expense_category)
    await callback.message.answer("Введите название новой категории:")
    await callback.answer()

@router.message(User_data.new_revenue_category)
async def save_new_revenue_category(message: Message, state: FSMContext):
    name = message.text.strip()[:20]
    if not name:
        await message.answer("Название не может быть пустым, попробуйте ещё раз:")
        return

    data = await state.get_data()
    main_valut = data["main_valut"]
    now = data["now"]
    onboarding_done = data.get("onboarding_done", False)

    custom = data.get("custom_revenue_categories", {})
    custom[name] = custom.get(name, 0) + now
    await state.update_data(custom_revenue_categories=custom, now=0)

    await message.answer(f"✅ Отлично, вы вписали {now}{main_valut} в новую категорию '{name}'")

    if onboarding_done:
        await message.answer("📋 Что дальше?", reply_markup=menu_kb)
    else:
        await state.set_state(User_data.expenses)
        await message.answer("Введите расходы за сегодняшний день:")

@router.message(User_data.new_expense_category)
async def save_new_expense_category(message: Message, state: FSMContext):
    name = message.text.strip()[:20]
    if not name:
        await message.answer("Название не может быть пустым, попробуйте ещё раз:")
        return

    data = await state.get_data()
    main_valut = data["main_valut"]
    ex_now = data["ex_now"]
    onboarding_done = data.get("onboarding_done", False)

    custom = data.get("custom_expense_categories", {})
    custom[name] = custom.get(name, 0) + ex_now
    await state.update_data(custom_expense_categories=custom, ex_now=0, onboarding_done=True)

    await message.answer(f"✅ Отлично, вы вписали {ex_now}{main_valut} в новую категорию '{name}'")

    if onboarding_done:
        await message.answer("📋 Что дальше?", reply_markup=menu_kb)
    else:
        await message.answer("🎉 Обучение завершено! Вот главное меню:", reply_markup=menu_kb)

@router.callback_query(F.data.startswith("customrev:"))
async def custom_revenue_category(callback: CallbackQuery, state: FSMContext):
    name = callback.data.split("customrev:", 1)[1]
    data = await state.get_data()
    main_valut = data["main_valut"]
    now = data["now"]
    onboarding_done = data.get("onboarding_done", False)

    custom = data.get("custom_revenue_categories", {})
    custom[name] = custom.get(name, 0) + now
    await state.update_data(custom_revenue_categories=custom, now=0)

    await callback.message.answer(f"✅ Отлично, вы вписали {now}{main_valut} в категорию '{name}'")

    if onboarding_done:
        await callback.message.answer("📋 Что дальше?", reply_markup=menu_kb)
    else:
        await state.set_state(User_data.expenses)
        await callback.message.answer("Введите расходы за сегодняшний день:")

    await callback.answer()

@router.callback_query(F.data == "none")
async def none(callback: CallbackQuery, state: FSMContext):
    await state.set_state(User_data.expenses)
    await callback.message.answer("Введите расходы за сегодняшний день:")


@router.callback_query(F.data == "back_to_get_revenues")
async def reget_revenues(callback: CallbackQuery, state: FSMContext):
    await state.update_data(revenues=0,
                            expenses=0,
                            zp=0,
                            tipo_zp=0,
                            xz=0,
                            duty=0,
                            prize=0,
                            now=0,
                            )

    await state.set_state(User_data.revenues)
    data = await state.get_data()
    main_valut = data["main_valut"]
    name = data["name"]

    await callback.message.answer(f"{name} введите доходы за сегодняшний день")

@router.message(User_data.expenses)
async def get_expenses(message: Message, state: FSMContext):
    if not message.text.isdigit():
        ...
        return
    data = await state.get_data()

    expenses = data["expenses"]
    ex_now = data["ex_now"]

    await state.update_data(expenses=expenses + int(message.text))
    await state.update_data(ex_now=ex_now + int(message.text))

    custom = data.get("custom_expense_categories", {})
    await message.answer("Отлично!Теперь выберите категорию куда вписать эти расходы", reply_markup=expenses_kategory(custom))

@router.callback_query(F.data == "ex_food")
async def ex_food(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_valut = data["main_valut"]
    ex_now = data["ex_now"]
    ex_food = data["ex_food"]
    onboarding_done = data.get("onboarding_done", False)

    await state.update_data(ex_food=ex_food + ex_now, ex_now=0, onboarding_done=True)
    await callback.message.answer(
        f"✅ Отлично, вы вписали {ex_now}{main_valut} в категорию 'Еда'"
    )

    if onboarding_done:
        await callback.message.answer("📋 Что дальше?", reply_markup=menu_kb)
    else:
        await callback.message.answer("🎉 Обучение завершено! Вот главное меню:", reply_markup=menu_kb)

    await callback.answer()

@router.callback_query(F.data == "ex_transport")
async def ex_transport(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_valut = data["main_valut"]
    ex_now = data["ex_now"]
    ex_transport = data["ex_transport"]
    onboarding_done = data.get("onboarding_done", False)

    await state.update_data(ex_transport=ex_transport + ex_now, ex_now=0, onboarding_done=True)
    await callback.message.answer(
        f"✅ Отлично, вы вписали {ex_now}{main_valut} в категорию 'Транспорт'"
    )

    if onboarding_done:
        await callback.message.answer("📋 Что дальше?", reply_markup=menu_kb)
    else:
        await callback.message.answer("🎉 Обучение завершено! Вот главное меню:", reply_markup=menu_kb)

    await callback.answer()

@router.callback_query(F.data == "ex_home")
async def ex_home(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_valut = data["main_valut"]
    ex_now = data["ex_now"]
    ex_home = data["ex_home"]
    onboarding_done = data.get("onboarding_done", False)

    await state.update_data(ex_home=ex_home + ex_now, ex_now=0, onboarding_done=True)
    await callback.message.answer(
        f"✅ Отлично, вы вписали {ex_now}{main_valut} в категорию 'Дом'"
    )

    if onboarding_done:
        await callback.message.answer("📋 Что дальше?", reply_markup=menu_kb)
    else:
        await callback.message.answer("🎉 Обучение завершено! Вот главное меню:", reply_markup=menu_kb)

    await callback.answer()

@router.callback_query(F.data == "ex_shopping")
async def ex_shopping(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_valut = data["main_valut"]
    ex_now = data["ex_now"]
    ex_shopping = data["ex_shopping"]
    onboarding_done = data.get("onboarding_done", False)

    await state.update_data(ex_shopping=ex_shopping + ex_now, ex_now=0, onboarding_done=True)
    await callback.message.answer(
        f"✅ Отлично, вы вписали {ex_now}{main_valut} в категорию 'Покупки'"
    )

    if onboarding_done:
        await callback.message.answer("📋 Что дальше?", reply_markup=menu_kb)
    else:
        await callback.message.answer("🎉 Обучение завершено! Вот главное меню:", reply_markup=menu_kb)

    await callback.answer()

@router.callback_query(F.data == "ex_comms")
async def ex_comms(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_valut = data["main_valut"]
    ex_now = data["ex_now"]
    ex_comms = data["ex_comms"]
    onboarding_done = data.get("onboarding_done", False)

    await state.update_data(ex_comms=ex_comms + ex_now, ex_now=0, onboarding_done=True)
    await callback.message.answer(
        f"✅ Отлично, вы вписали {ex_now}{main_valut} в категорию 'Связь'"
    )

    if onboarding_done:
        await callback.message.answer("📋 Что дальше?", reply_markup=menu_kb)
    else:
        await callback.message.answer("🎉 Обучение завершено! Вот главное меню:", reply_markup=menu_kb)

    await callback.answer()

@router.callback_query(F.data == "ex_fun")
async def ex_fun(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_valut = data["main_valut"]
    ex_now = data["ex_now"]
    ex_fun = data["ex_fun"]
    onboarding_done = data.get("onboarding_done", False)

    await state.update_data(ex_fun=ex_fun + ex_now, ex_now=0, onboarding_done=True)
    await callback.message.answer(
        f"✅ Отлично, вы вписали {ex_now}{main_valut} в категорию 'Развлечения'"
    )

    if onboarding_done:
        await callback.message.answer("📋 Что дальше?", reply_markup=menu_kb)
    else:
        await callback.message.answer("🎉 Обучение завершено! Вот главное меню:", reply_markup=menu_kb)

    await callback.answer()

@router.callback_query(F.data == "ex_subs")
async def ex_subs(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_valut = data["main_valut"]
    ex_now = data["ex_now"]
    ex_subs = data["ex_subs"]
    onboarding_done = data.get("onboarding_done", False)

    await state.update_data(ex_subs=ex_subs + ex_now, ex_now=0, onboarding_done=True)
    await callback.message.answer(
        f"✅ Отлично, вы вписали {ex_now}{main_valut} в категорию 'Подписки'"
    )

    if onboarding_done:
        await callback.message.answer("📋 Что дальше?", reply_markup=menu_kb)
    else:
        await callback.message.answer("🎉 Обучение завершено! Вот главное меню:", reply_markup=menu_kb)

    await callback.answer()

@router.callback_query(F.data == "ex_credit")
async def ex_credit(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_valut = data["main_valut"]
    ex_now = data["ex_now"]
    ex_credit = data["ex_credit"]
    onboarding_done = data.get("onboarding_done", False)

    await state.update_data(ex_credit=ex_credit + ex_now, ex_now=0, onboarding_done=True)
    await callback.message.answer(
        f"✅ Отлично, вы вписали {ex_now}{main_valut} в категорию 'Кредит'"
    )

    if onboarding_done:
        await callback.message.answer("📋 Что дальше?", reply_markup=menu_kb)
    else:
        await callback.message.answer("🎉 Обучение завершено! Вот главное меню:", reply_markup=menu_kb)

    await callback.answer()

@router.callback_query(F.data == "ex_xz")
async def ex_xz(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    main_valut = data["main_valut"]
    ex_now = data["ex_now"]
    ex_xz = data["ex_xz"]
    onboarding_done = data.get("onboarding_done", False)

    await state.update_data(ex_xz=ex_xz + ex_now, ex_now=0, onboarding_done=True)
    await callback.message.answer(
        f"✅ Отлично, вы вписали {ex_now}{main_valut} в категорию 'Забытое'"
    )

    if onboarding_done:
        await callback.message.answer("📋 Что дальше?", reply_markup=menu_kb)
    else:
        await callback.message.answer("🎉 Обучение завершено! Вот главное меню:", reply_markup=menu_kb)

    await callback.answer()

@router.callback_query(F.data.startswith("customex:"))
async def custom_expense_category(callback: CallbackQuery, state: FSMContext):
    name = callback.data.split("customex:", 1)[1]
    data = await state.get_data()
    main_valut = data["main_valut"]
    ex_now = data["ex_now"]
    onboarding_done = data.get("onboarding_done", False)

    custom = data.get("custom_expense_categories", {})
    custom[name] = custom.get(name, 0) + ex_now
    await state.update_data(custom_expense_categories=custom, ex_now=0, onboarding_done=True)

    await callback.message.answer(f"✅ Отлично, вы вписали {ex_now}{main_valut} в категорию '{name}'")

    if onboarding_done:
        await callback.message.answer("📋 Что дальше?", reply_markup=menu_kb)
    else:
        await callback.message.answer("🎉 Обучение завершено! Вот главное меню:", reply_markup=menu_kb)

    await callback.answer()


@router.callback_query(F.data == "back_to_get_expenses")
async def reget_expenses(callback: CallbackQuery, state: FSMContext):
    await state.update_data(expenses=0,
                            ex_xz=0,
                            ex_credit=0,
                            ex_now=0,
                            ex_subs=0,
                            ex_fun=0,
                            ex_comms=0,
                            ex_shopping=0,
                            ex_home=0,
                            ex_transport=0,
                            ex_food=0,
                            )

    await state.set_state(User_data.expenses)
    data = await state.get_data()
    main_valut = data["main_valut"]
    name = data["name"]

    await callback.message.answer(f"{name} введите расходы за сегодняшний день")

back_to_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⬅ В меню", callback_data="back_to_menu")]
    ]
)

@router.callback_query(F.data == "stats")
async def show_stats(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    v = data["main_valut"]
    revenues = data["revenues"]
    expenses = data["expenses"]


    revenue_items = [
        ("💸 Зарплата", data["zp"]),
        ("💲 Подработка", data["tipo_zp"]),
        ("🎁 Подарок", data["prize"]),
        ("✔ Долг", data["duty"]),
        ("❓ Забытое", data["xz"]),
    ]
    expense_items = [
        ("🍔 Еда", data["ex_food"]),
        ("🚌 Транспорт", data["ex_transport"]),
        ("🏠 Жильё", data["ex_home"]),
        ("🛒 Покупки", data["ex_shopping"]),
        ("📱 Связь", data["ex_comms"]),
        ("🎮 Развлечения", data["ex_fun"]),
        ("💳 Подписки", data["ex_subs"]),
        ("🏦 Кредиты", data["ex_credit"]),
        ("❓ Забытое", data["ex_xz"]),
    ]


    custom_rev = data.get("custom_revenue_categories", {})
    for name, amount in custom_rev.items():
        revenue_items.append((f"📌 {name}", amount))

    custom_ex = data.get("custom_expense_categories", {})
    for name, amount in custom_ex.items():
        expense_items.append((f"📌 {name}", amount))

    text = "📊 Статистика\n\n"

    text += f"💰 Доходы: {revenues}{v}\n"
    for name, amount in revenue_items:
        if amount > 0:
            text += f"   • {name}: {amount}{v}\n"

    text += f"\n💸 Расходы: {expenses}{v}\n"
    for name, amount in expense_items:
        if amount > 0:
            text += f"   • {name}: {amount}{v}\n"

    balance = revenues - expenses
    text += f"\n⚖️ Баланс: {balance}{v}"

    await callback.message.answer(text, reply_markup=back_to_menu_kb)
    await callback.answer()


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.answer("📋 Главное меню:", reply_markup=menu_kb)
    await callback.answer()



@router.callback_query(F.data == "settings")
async def settings(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    data = await state.get_data()
    text = (
        "⚙️ Настройки\n\n"
        f"👤 Имя: {data['name']}\n"
        f"💱 Валюта: {data['main_valut']}"
    )
    await callback.message.answer(text, reply_markup=settings_kb)
    await callback.answer()



@router.callback_query(F.data == "set_name")
async def set_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(User_data.change_name)
    await callback.message.answer("Введите новое имя:", reply_markup=cancel_kb)
    await callback.answer()

@router.message(User_data.change_name)
async def save_name(message: Message, state: FSMContext):
    name = message.text.strip()[:30]
    if not name:
        await message.answer("Имя не может быть пустым, попробуйте ещё раз:")
        return
    await state.update_data(name=name)
    await state.set_state(None)
    await message.answer(f"✅ Имя изменено на {name}", reply_markup=settings_kb)



@router.callback_query(F.data == "set_pin")
async def set_pin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(User_data.change_pin_old)
    await callback.message.answer("Введите текущий PIN-код:", reply_markup=cancel_kb)
    await callback.answer()

@router.message(User_data.change_pin_old)
async def check_old_pin(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    if message.text != data["pin"]:
        await message.answer("❌ Неверный PIN-код. Попробуйте ещё раз:", reply_markup=cancel_kb)
        return
    await state.set_state(User_data.change_pin_new)
    await message.answer("Введите новый PIN-код (4–6 цифр):", reply_markup=cancel_kb)

@router.message(User_data.change_pin_new)
async def save_new_pin(message: Message, state: FSMContext):
    pin = message.text
    await message.delete()
    if not pin.isdigit() or len(pin) < 4 or len(pin) > 6:
        await message.answer("❌ PIN-код должен состоять из 4–6 цифр. Попробуйте ещё раз:", reply_markup=cancel_kb)
        return
    await state.update_data(pin=pin)
    await state.set_state(None)
    await message.answer("✅ PIN-код изменён", reply_markup=settings_kb)


@router.callback_query(F.data.startswith("set_cur_"))
async def save_currency(callback: CallbackQuery, state: FSMContext):
    code = callback.data.split("set_cur_", 1)[1]
    symbols = {"KZT": "₸", "RUB": "₽", "USD": "$", "EUR": "€"}
    await state.update_data(main_valut=symbols[code])
    await callback.message.answer(
        f"✅ Валюта изменена на {symbols[code]}\n"
        "Суммы не пересчитываются, меняется только значок.",
        reply_markup=settings_kb
    )
    await callback.answer()



@router.callback_query(F.data == "reset_stats")
async def ask_reset_stats(callback: CallbackQuery, state: FSMContext):
    await state.update_data(pending_action="reset_stats")
    await state.set_state(User_data.confirm_pin)
    await callback.message.answer(
        "🧹 Вся статистика (доходы, расходы, категории) будет обнулена.\n"
        "Введите PIN-код для подтверждения:",
        reply_markup=cancel_kb
    )
    await callback.answer()

@router.callback_query(F.data == "delete_all")
async def ask_delete_all(callback: CallbackQuery, state: FSMContext):
    await state.update_data(pending_action="delete_all")
    await state.set_state(User_data.confirm_pin)
    await callback.message.answer(
        "⚠️ Будут удалены ВСЕ данные, включая профиль.\n"
        "Введите PIN-код для подтверждения:",
        reply_markup=cancel_kb
    )
    await callback.answer()

@router.message(User_data.confirm_pin)
async def confirm_pin(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    if message.text != data["pin"]:
        await message.answer("❌ Неверный PIN-код. Попробуйте ещё раз:", reply_markup=cancel_kb)
        return

    if data["pending_action"] == "reset_stats":
        await state.update_data(
            revenues=0, expenses=0,
            zp=0, tipo_zp=0, prize=0, duty=0, xz=0, now=0,
            ex_food=0, ex_transport=0, ex_home=0, ex_shopping=0,
            ex_comms=0, ex_fun=0, ex_subs=0, ex_credit=0, ex_xz=0, ex_now=0,
            custom_revenue_categories={},
            custom_expense_categories={},
            pending_action=None,
        )
        await state.set_state(None)
        await message.answer("✅ Статистика сброшена", reply_markup=settings_kb)
    else:
        await state.clear()
        await message.answer("🗑 Все данные удалены. Чтобы начать заново, нажмите /start")
