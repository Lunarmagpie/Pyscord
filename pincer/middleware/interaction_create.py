# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import logging
from typing import TYPE_CHECKING
from inspect import isasyncgenfunction, getfullargspec
from typing import Dict, Any

from pincer.utils import get_index
from ..commands import ChatCommandHandler
from ..core.dispatch import GatewayDispatch
from ..objects import Interaction, MessageContext
from ..utils.convert_message import convert_message
from ..utils.conversion import construct_client_dict
from ..utils.signature import get_params, get_signature_and_params
from ..utils import MISSING, should_pass_cls, Coro, should_pass_ctx

if TYPE_CHECKING:
    from typing import List, Tuple


_log = logging.getLogger(__name__)


async def interaction_response_handler(
        self,
        command: Coro,
        context: MessageContext,
        interaction: Interaction,
        kwargs: Dict[str, Any]
):
    """|coro|

    Handle any coroutine as a command.

    Parameters
    ----------
    command : :data:`~pincer.utils.types.Coro`
        The coroutine which will be seen as a command.
    context : :class:`~pincer.objects.message.context.MessageContext`
        The context of the command.
    interaction : :class:`~pincer.objects.app.interactions.Interaction`
        The interaction which is linked to the command.
    \\*\\*kwargs :
        The arguments to be passed to the command.
    """
    if should_pass_cls(command):
        cls_keyword = getfullargspec(command).args[0]
        kwargs[cls_keyword] = ChatCommandHandler.managers[command.__module__]

    sig, params = get_signature_and_params(command)
    if should_pass_ctx(sig, params):
        kwargs[params[0]] = context

    if isasyncgenfunction(command):
        message = command(**kwargs)
        started = False

        async for msg in message:
            msg = convert_message(self, msg)

            if started:
                await interaction.followup(msg)
            else:
                started = True
                await interaction.reply(msg)
    else:
        message = await command(**kwargs)
        await interaction.reply(convert_message(self, message))


async def interaction_handler(
        self,
        interaction: Interaction,
        context: MessageContext,
        command: Coro
):
    """|coro|

    Processes an interaction.

    Parameters
    ----------
    interaction : :class:`~pincer.objects.app.interactions.Interaction`
        The interaction which is linked to the command.
    context : :class:`~pincer.objects.message.context.MessageContext`
        The context of the command.
    command : :data:`~pincer.utils.types.Coro`
        The coroutine which will be seen as a command.
    """
    self.throttler.handle(context)

    defaults = {param: None for param in get_params(command)}
    params = {}

    if interaction.data.options is not MISSING:
        params = {
            opt.name: opt.value for opt in interaction.data.options
        }

    kwargs = {**defaults, **params}

    await interaction_response_handler(
        self, command, context, interaction, kwargs)


async def interaction_create_middleware(
    self,
    payload: GatewayDispatch
) -> Tuple[str, List[Interaction]]:
    """Middleware for ``on_interaction``, which handles command
    execution.

    Parameters
    ----------
    payload : :class:`~pincer.core.dispatch.GatewayDispatch`
        The data received from the interaction event.

    Raises
    ------
    e
        Generic try except on ``await interaction_handler`` and
        ``if 0 < len(params) < 3``

    Returns
    -------
    Tuple[:class:`str`, List[:class:`~pincer.objects.app.interactions.Interaction`]]
        ``on_interaction_create`` and an ``Interaction``
    """  # noqa: E501
    interaction: Interaction = Interaction.from_dict(
        construct_client_dict(self, payload.data)
    )
    await interaction.build()
    command = ChatCommandHandler.register.get(interaction.data.name)

    if command:
        context = interaction.convert_to_message_context(command)

        try:
            await interaction_handler(self, interaction, context,
                                      command.call)
        except Exception as e:
            if coro := get_index(self.get_event_coro("on_command_error"), 0):
                params = get_signature_and_params(coro)[1]

                # Check if a context or error var has been passed.
                if 0 < len(params) < 3:
                    await interaction_response_handler(
                        self,
                        coro,
                        context,
                        interaction,
                        # Always take the error parameter its name.
                        {params[(len(params) - 1) or 0]: e}
                    )
                else:
                    raise e
            else:
                raise e

    return "on_interaction_create", [interaction]


def export() -> Coro:
    return interaction_create_middleware
