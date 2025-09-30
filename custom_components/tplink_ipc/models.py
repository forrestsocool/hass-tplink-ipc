"""Data models for the TP-Link IPC Camera integration."""
from dataclasses import dataclass

from .api import TPLinkIPCApiClient
from .talkback import TPLinkTalkbackPlayer


@dataclass
class TPLinkCameraData:
    """A container for all client instances."""

    api_client: TPLinkIPCApiClient
    talkback_client: TPLinkTalkbackPlayer