from opentrons import protocol_api
from opentrons.drivers.rpi_drivers import gpio
import time
import math

# Metadata
metadata = {
    'protocolName': 'S3 Station C Version 1',
    'author': 'Nick <protocols@opentrons.com>, Sara <smonzon@isciii.es>, Miguel <mjuliam@isciii.es>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.1'
}

# Parameters to adapt the protocol
NUM_SAMPLES = 96
MM_LABWARE = 'opentrons aluminum block'
MMTUBE_LABWARE = '2ml tubes'
PCR_LABWARE = 'opentrons aluminum nest plate'
ELUTION_LABWARE = 'opentrons aluminum nest plate'
PREPARE_MASTERMIX = True
TRANSFER_MASTERMIX = True
TRANSFER_SAMPLES = True
MM_TYPE = 'MM1'
