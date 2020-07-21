"""Platform for sensor integration."""
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
import requests

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=900)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([Oersted_Power_Price()])


class Oersted_Power_Price(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Ørsted Power Price'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return 'DKK'

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        today = '2020-07-21'
        tomorrow = '2020-07-22'
        hour = 12
        r = requests.get(f'https://privat.orsted.dk/?obexport_format=csv&obexport_start={today}&obexport_end={tomorrow}&obexport_region=east')
        r.raise_for_status()
        self._state = float(r.text.splitlines()[1].split(',')[hour+1])
