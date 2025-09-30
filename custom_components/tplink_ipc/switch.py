import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.exceptions import HomeAssistantError

from .api import TPLinkIPCApiClient, TPIPCApiError
from .const import DOMAIN
from .models import TPLinkCameraData

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the TP-Link IPC Camera switches from a config entry."""
    camera_data: TPLinkCameraData = hass.data[DOMAIN][config_entry.entry_id]
    
    lens_mask_switch = LensMaskSwitch(camera_data.api_client, config_entry)
    async_add_entities([lens_mask_switch], update_before_add=True)


class LensMaskSwitch(SwitchEntity):
    """Representation of a lens mask switch for a TP-Link camera."""

    _attr_has_entity_name = True

    def __init__(self, client: TPLinkIPCApiClient, config_entry: ConfigEntry) -> None:
        """Initialize the switch."""
        self._client = client
        self._attr_is_on = None
        self._attr_name = "Lens Mask"
        self._attr_unique_id = f"{config_entry.unique_id or config_entry.entry_id}_lens_mask"
        self._attr_icon = "mdi:cctv-off"
        
        # Link to the device
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.unique_id or config_entry.entry_id)},
            name=config_entry.title,
            # You can add more device info here if the API provides it, e.g., model, fw_version
        )

    async def _execute_api_call(self, api_call, *args):
        """Execute a blocking API call in the executor."""
        try:
            return await self.hass.async_add_executor_job(api_call, *args)
        except TPIPCApiError as err:
            _LOGGER.error("API call failed: %s", err)
            raise HomeAssistantError(f"Failed to communicate with camera: {err}") from err

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the lens mask on (enable privacy mode)."""
        await self._execute_api_call(self._client.set_lens_mask_on)
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the lens mask off (disable privacy mode)."""
        await self._execute_api_call(self._client.set_lens_mask_off)
        self._attr_is_on = False
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Fetch the latest state of the lens mask."""
        self._attr_is_on = await self._execute_api_call(self._client.get_lens_mask_status)