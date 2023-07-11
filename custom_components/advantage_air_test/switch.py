"""Switch platform for Advantage Air integration."""
from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    ADVANTAGE_AIR_STATE_OFF,
    ADVANTAGE_AIR_STATE_ON,
    DOMAIN as ADVANTAGE_AIR_DOMAIN,
)
from .entity import AdvantageAirAcEntity, AdvantageAirThingEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up AdvantageAir switch platform."""

    instance = hass.data[ADVANTAGE_AIR_DOMAIN][config_entry.entry_id]

    entities: list[SwitchEntity] = []
    if "myThings" in instance["coordinator"].data:
        for thing in instance["coordinator"].data["myThings"]["things"].values():
            if thing["channelDipState"] == 8:  # 8 = Other relay
                entities.append(AdvantageAirRelay(instance, thing))
    async_add_entities(entities)



class AdvantageAirRelay(AdvantageAirThingEntity, SwitchEntity):
    """Representation of Advantage Air Thing."""

    _attr_device_class = SwitchDeviceClass.SWITCH
