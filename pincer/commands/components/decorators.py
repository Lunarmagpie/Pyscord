# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from functools import partial
from inspect import iscoroutinefunction
from typing import Any, List

from .button import Button, ButtonStyle
from .select_menu import SelectMenu, SelectOption
from .component_handler import ComponentHandler
from ..interactable import PartialInteractable
from ...objects.app.command import InteractableStructure
from ...exceptions import CommandIsNotCoroutine
from ...objects.message.emoji import Emoji
from ...utils.conversion import remove_none


def component(custom_id):
    """
    Generic handler for Message Components. Can be used with manually constructed
    :class:`~pincer.commands.components.button.Button` and
    :class:`~pincer.commands.components.select_menu.SelectMenu` objects.

    Parameters
    ---------
    custom_id : str
        The ID of the message component to handle.
    """
    def wrap(custom_id, func):
        ComponentHandler().register_id(_id=custom_id, func=func)
        return func

    return partial(wrap, custom_id)


def button(
    label: str,
    style: ButtonStyle,
    emoji: Emoji = None,
    url: str = None,
    disabled: bool = None,
    custom_id: str = None
) -> Button:
    """
    Turn a function into handler for a :class:`~pincer.commands.components.button.Button`.
    See :class:`~pincer.commands.components.button.Button` for information on parameters.

    The function will still be callable.

    .. code-block:: python

        from pincer.commands import ActionRow, Button

        class Bot(Client):

            @command
            async def send_a_button(self):
                return Message(
                    content="Click a button",
                    components=[
                        ActionRow(
                            self.button_one
                        )
                    ]
                )

            @button(label="Click me!", style=ButtonStyle.PRIMARY)
            async def button_one():
                return "Button one pressed"
    """  # noqa: E501

    def wrap(custom_id, func) -> Button:
        if not iscoroutinefunction(func):
            raise CommandIsNotCoroutine(f"`{func.__name__}` must be a coroutine.")

        if custom_id is None:
            custom_id = func.__name__

        return _PartialButton(
            func=func,
            custom_id=custom_id,
            style=style,
            label=label,
            disabled=disabled,
            emoji=emoji,
            url=url,
        )

    return partial(wrap, custom_id)


class _PartialButton(PartialInteractable):
    def register(self, manager: Any) -> Button:
        button = Button(*self.args, _func=self.func, **remove_none(self.kwargs))
        button.func = self.func
        button.__call__ = partial(self.func)

        ComponentHandler.register[self.kwargs.get("custom_id")] = InteractableStructure(
            call=self.func,
            manager=manager
        )

        return button


def select_menu(
    func=None,
    options: List[SelectOption] = None,
    placeholder: str = None,
    min_values: int = None,
    max_values: int = None,
    disabled: bool = None,
    custom_id: str = None


) -> SelectMenu:
    """
    Turn a function into handler for a :class:`~pincer.commands.components.select_menu.SelectMenu`.
    See :class:`~pincer.commands.components.select_menu.SelectMenu` for information on parameters.

    The function will still be callable.

    .. code-block:: python

        from pincer.commands import button, ActionRow, ButtonStyle

        class Bot(Client):

            @command
            async def send_a_select_menu(self):
                return Message(
                    content="Choose an option",
                    components=[
                        ActionRow(
                            self.select_menu
                        )
                    ]
                )

            @select_menu(options=[
                SelectOption(label="Option 1"),
                SelectOption(label="Option 2", value="value different than label")
            ])
            async def select_menu(values: List[str]):
                return f"{values[0]} selected"

    """  # noqa: E501

    def wrap(custom_id, func) -> SelectMenu:
        if not iscoroutinefunction(func):
            raise CommandIsNotCoroutine(f"`{func.__name__}` must be a coroutine.")

        if custom_id is None:
            custom_id = func.__name__

        return _PartialSelectMenu(
            func=func,
            custom_id=custom_id,
            options=options,
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            disabled=disabled,
        )

    if func is None:
        return partial(wrap, custom_id)

    return wrap(custom_id, func)


class _PartialSelectMenu(PartialInteractable):
    def register(self, manager: Any) -> SelectMenu:
        ComponentHandler.register[self.kwargs.get("custom_id")] = InteractableStructure(
            call=self.func,
            manager=manager
        )

        return SelectMenu(
            *self.args,
            _func=self.func,
            **remove_none(self.kwargs)
        )
