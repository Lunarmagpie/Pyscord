# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from enum import IntEnum
from dataclasses import dataclass
from typing import overload, TYPE_CHECKING

from ...utils.types import MISSING
from ..._config import GatewayConfig
from ...utils.api_object import APIObject

if TYPE_CHECKING:
    from typing import Dict, List, Optional, Union

    from ...client import Client
    from ..user.user import User
    from .member import GuildMember
    from .overwrite import Overwrite
    from .thread import ThreadMetadata
    from ...utils.types import APINullable
    from ...utils.snowflake import Snowflake
    from ...utils.timestamp import Timestamp


class ChannelType(IntEnum):
    """Represents a channel its type.

    Attributes
    ----------
    GUILD_TEXT:
        A text channel.
    DM:
        A DM channel.
    GUILD_VOICE:
        A voice channel.
    GROUP_DM:
        A group DM channel.
    GUILD_CATEGORY:
        A category channel.
    GUILD_NEWS:
        A news channel.
    GUILD_STORE:
        A store channel.
    GUILD_NEWS_THREAD:
        A news thread.
    GUILD_PUBLIC_THREAD:
        A public thread.
    GUILD_PRIVATE_THREAD:
        A private thread.
    GUILD_STAGE_VOICE:
        A stage channel.
    """
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_NEWS = 5
    GUILD_STORE = 6

    if GatewayConfig.version >= 9:
        GUILD_NEWS_THREAD = 10
        GUILD_PUBLIC_THREAD = 11
        GUILD_PRIVATE_THREAD = 12

    GUILD_STAGE_VOICE = 13


@dataclass
class Channel(APIObject):  # noqa E501
    """Represents a Discord Channel Mention object

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        The id of this channel
    type: :class:`~pincer.objects.guild.channel.ChannelType`
        The type of channel
    application_id: APInullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Application id of the group DM creator if it is bot-created
    bitrate: APINullable[:class:`int`]
        The bitrate (in bits) of the voice channel
    default_auto_archive_duration: APINullable[:class:`int`]
        Default duration for newly created threads, in minutes, to
        automatically archive the thread after recent activity, can be set to:
        60, 1440, 4320, 10080
    guild_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        The id of the guild (may be missing for some channel objects received
        over gateway guild dispatches)
    icon: APINullable[Optional[:class:`str`]]
        Icon hash
    last_message_id: APINullable[Optional[:class:`~pincer.utils.snowflake.Snowflake`]]
        The id of the last message sent in this channel (may not point to an
        existing or valid message)
    last_pin_timestamp: APINullable[Optional[:class:`~pincer.utils.timestamp.Timestamp`]]
        When the last pinned message was pinned. This may be null in events
        such as GUILD_CREATE when a message is not pinned.
    member: APINullable[:class:`~pincer.objects.guild.member.GuildMember`]
        Thread member object for the current user, if they have joined the
        thread, only included on certain API endpoints
    member_count: APINullable[:class:`int`]
        An approximate count of users in a thread, stops counting at 50
    message_count: :class:`int`
        An approximate count of messages in a thread, stops counting at 50
    name: APINullable[:class:`str`]
        The name of the channel (1-100 characters)
    nsfw: APINullable[:class:`bool`]
        Whether the channel is nsfw
    owner_id: APINullable[:class:`~pincer.utils.snowflake.Snowflake`]
        Id of the creator of the group DM or thread
    parent_id: APInullable[Optional[:class:`~pincer.utils.snowflake.Snowflake`]]
        For guild channels: id of the parent category for a channel (each
        parent category can contain up to 50 channels), for threads: id of the
        text channel this thread was created
    permissions: APINullable[:class:`str`]
        Computed permissions for the invoking user in the channel, including
        overwrites, only included when part of the resolved data received on a
        slash command interaction
    permission_overwrites: APINullable[List[:class:`~pincer.obects.guild.overwrite.Overwrite`]]
        Explicit permission overwrites for members and roles
    position: APINullable[:class:`int`]
        Sorting position of the channel
    rate_limit_per_user: APINullable[:class:`int`]
        Amount of seconds a user has to wait before sending another message
        (0-21600); bots, as well as users with the permission manage_messages
        or manage_channel, are unaffected
    recipients: APINullable[List[:class:`~pincer.objects.user.user.User`]]
        The recipients of the DM
    rtc_region: APINullable[Optional[:class:`str`]]
        Voice region id for the voice channel, automatic when set to null
    thread_metadata: APINullable[:class:`~pincer.objects.guild.thread.ThreadMetadata`]
        Thread-specific fields not needed by other channels
    topic: APINullable[Optional[:class:`str`]]
        The channel topic (0-1024 characters)
    user_limit: APINullable[:class:`int`]
        The user limit of the voice channel
    video_quality_mode: APINullable[:class:`int`]
        The camera video quality mode of the voice channel, 1 when not present
    """  # noqa: E501
    id: Snowflake
    type: ChannelType

    application_id: APINullable[Snowflake] = MISSING
    bitrate: APINullable[int] = MISSING
    default_auto_archive_duration: APINullable[int] = MISSING
    guild_id: APINullable[Snowflake] = MISSING
    icon: APINullable[Optional[str]] = MISSING

    last_message_id: APINullable[Optional[Snowflake]] = MISSING
    last_pin_timestamp: APINullable[Optional[Timestamp]] = MISSING
    member: APINullable[GuildMember] = MISSING

    member_count: APINullable[int] = MISSING

    message_count: APINullable[int] = MISSING

    name: APINullable[str] = MISSING
    nsfw: APINullable[bool] = MISSING
    owner_id: APINullable[Snowflake] = MISSING
    parent_id: APINullable[Optional[Snowflake]] = MISSING
    permissions: APINullable[str] = MISSING
    permission_overwrites: APINullable[List[Overwrite]] = MISSING
    position: APINullable[int] = MISSING
    rate_limit_per_user: APINullable[int] = MISSING
    recipients: APINullable[List[User]] = MISSING
    rtc_region: APINullable[Optional[str]] = MISSING
    thread_metadata: APINullable[ThreadMetadata] = MISSING
    topic: APINullable[Optional[str]] = MISSING
    user_limit: APINullable[int] = MISSING
    video_quality_mode: APINullable[int] = MISSING

    @property
    def mention(self):
        return f"<#{self.id}>"

    @classmethod
    async def from_id(cls, client: Client, channel_id: int) -> Channel:
        data = (await client.http.get(f"channels/{channel_id}")) or {}
        data.update(
            {
                "_client": client,
                "_http": client.http,
                "type": ChannelType(data.pop("type"))
            }
        )

        channel_cls = _channel_type_map.get(data["type"], Channel)
        return channel_cls.from_dict(data)

    @overload
    async def edit(
            self, *, name: str = None,
            type: ChannelType = None,
            position: int = None, topic: str = None, nsfw: bool = None,
            rate_limit_per_user: int = None, bitrate: int = None,
            user_limit: int = None,
            permissions_overwrites: List[Overwrite] = None,
            parent_id: Snowflake = None, rtc_region: str = None,
            video_quality_mod: int = None,
            default_auto_archive_duration: int = None
    ) -> Channel:
        ...

    async def edit(self, **kwargs):
        """Edit a channel with the given keyword arguments.

        Parameters
        ----------
        \\*\\*kwargs :
            The keyword arguments to edit the channel with.

        Returns
        -------
        :class:`~pincer.objects.guild.channel.Channel`
            The updated channel object.
        """
        data = await self._http.patch(f"channels/{self.id}", data=kwargs)
        data.update(
            {
                "_client": self._client,
                "_http": self._http,
                "type": ChannelType(data.pop("type"))
            }
        )
        channel_cls = _channel_type_map.get(data["type"], Channel)
        return channel_cls.from_dict(data)


def __str__(self):
    """return the discord tag when object gets used as a string."""
    return self.name or str(self.id)


class TextChannel(Channel):
    """A subclass of ``Channel`` for text channels with all the same attributes.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @overload
    async def edit(
            self, name: str = None, type: ChannelType = None,
            position: int = None, topic: str = None, nsfw: bool = None,
            rate_limit_per_user: int = None,
            permissions_overwrites: List[Overwrite] = None,
            parent_id: Snowflake = None,
            default_auto_archive_duration: int = None
    ) -> Union[TextChannel, NewsChannel]:
        ...

    async def edit(self, **kwargs):
        """Edit a text channel with the given keyword arguments.

        Parameters
        ----------
        \\*\\*kwargs :
            The keyword arguments to edit the channel with.

        Returns
        -------
        :class:`~pincer.objects.guild.channel.Channel`
            The updated channel object.
        """
        return await super().edit(**kwargs)


class VoiceChannel(Channel):
    """A subclass of ``Channel`` for voice channels with all the same attributes.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @overload
    async def edit(
            self, name: str = None, position: int = None, bitrate: int = None,
            user_limit: int = None,
            permissions_overwrites: List[Overwrite] = None,
            rtc_region: str = None, video_quality_mod: int = None
    ) -> VoiceChannel:
        ...

    async def edit(self, **kwargs):
        """Edit a text channel with the given keyword arguments.

        Parameters
        ----------
        \\*\\*kwargs :
            The keyword arguments to edit the channel with.

        Returns
        -------
        :class:`~pincer.objects.guild.channel.Channel`
            The updated channel object.
        """
        return await super().edit(**kwargs)


class CategoryChannel(Channel):
    """A subclass of ``Channel`` for categories channels
    with all the same attributes.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NewsChannel(Channel):
    """A subclass of ``Channel`` for news channels with all the same attributes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @overload
    async def edit(
            self, name: str = None, type: ChannelType = None,
            position: int = None, topic: str = None, nsfw: bool = None,
            permissions_overwrites: List[Overwrite] = None,
            parent_id: Snowflake = None,
            default_auto_archive_duration: int = None
    ) -> Union[TextChannel, NewsChannel]:
        ...

    async def edit(self, **kwargs):
        """Edit a text channel with the given keyword arguments.

        Parameters
        ----------
        \\*\\*kwargs :
            The keyword arguments to edit the channel with.

        Returns
        -------
        :class:`~pincer.objects.guild.channel.Channel`
            The updated channel object.
        """
        return await super().edit(**kwargs)


@dataclass
class ChannelMention(APIObject):
    """Represents a Discord Channel Mention object

    Attributes
    ----------
    id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the channel
    guild_id: :class:`~pincer.utils.snowflake.Snowflake`
        Id of the guild containing the channel
    type: :class:`~pincer.objects.guild.channel.ChannelType`
        The type of channel
    name: :class:`str`
        The name of the channel
    """
    id: Snowflake
    guild_id: Snowflake
    type: ChannelType
    name: str


_channel_type_map: Dict[ChannelType, Channel] = {
    ChannelType.GUILD_TEXT: TextChannel,
    ChannelType.GUILD_VOICE: VoiceChannel,
    ChannelType.GUILD_CATEGORY: CategoryChannel,
    ChannelType.GUILD_NEWS: NewsChannel
}
