"""
WienerNetze Smartmeter sensor platform
"""
import collections.abc
from datetime import timedelta
from typing import Optional

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import core, config_entries
from homeassistant.components.sensor import (
    PLATFORM_SCHEMA
)
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_DEVICE_ID
)
from homeassistant.core import DOMAIN
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
)
from .const import CONF_ZAEHLPUNKTE, CONF_SCAN_INTERVAL
from .wnsm_sensor import WNSMSensor, WNSMSensorWithApiDate
# Time between updating data from Wiener Netze
SCAN_INTERVAL = timedelta(minutes=60 * 6)
DEFAULT_SCAN_INTERVAL_MINUTES = 60 * 6
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_DEVICE_ID): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL_MINUTES): cv.positive_int,
    }
)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Setup sensors from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    scan_interval_minutes = config_entry.options.get(
        CONF_SCAN_INTERVAL, config.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL_MINUTES)
    )
    scan_interval = timedelta(minutes=scan_interval_minutes)
    wnsm_sensors = []
    for zp in config[CONF_ZAEHLPUNKTE]:
        display_name = zp.get("label") or zp.get("zaehlpunktnummer")
        base_sensor = WNSMSensor(
            config[CONF_USERNAME], config[CONF_PASSWORD], zp["zaehlpunktnummer"], display_name
        )
        base_sensor._attr_scan_interval = scan_interval
        api_sensor = WNSMSensorWithApiDate(
            config[CONF_USERNAME], config[CONF_PASSWORD], zp["zaehlpunktnummer"], display_name
        )
        api_sensor._attr_scan_interval = scan_interval
        wnsm_sensors.extend([base_sensor, api_sensor])
    async_add_entities(wnsm_sensors, update_before_add=True)


async def async_setup_platform(
    hass: core.HomeAssistant,  # pylint: disable=unused-argument
    config: ConfigType,
    async_add_entities: collections.abc.Callable,
    discovery_info: Optional[
        DiscoveryInfoType
    ] = None,  # pylint: disable=unused-argument
) -> None:
    """Set up the sensor platform by adding it into configuration.yaml"""
    scan_interval_minutes = config.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL_MINUTES)
    scan_interval = timedelta(minutes=scan_interval_minutes)
    wnsm_sensor = WNSMSensor(config[CONF_USERNAME], config[CONF_PASSWORD], config[CONF_DEVICE_ID])
    wnsm_sensor._attr_scan_interval = scan_interval
    wnsm_sensor_with_api_date = WNSMSensorWithApiDate(
        config[CONF_USERNAME], config[CONF_PASSWORD], config[CONF_DEVICE_ID]
    )
    wnsm_sensor_with_api_date._attr_scan_interval = scan_interval
    async_add_entities([wnsm_sensor, wnsm_sensor_with_api_date], update_before_add=True)
