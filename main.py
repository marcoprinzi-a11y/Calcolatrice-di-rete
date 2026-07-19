import sys
import argparse
import json
from typing import List
from network_models import NetworkObject, IPv4Network, IPv6Network

def create_network_object(cidr_input: str) -> NetworkObject:
    """
    Factory method che analizza l'input e restituisce l'istanza corretta.
    Dimostra che il codice chiamante non ha bisogno di sapere
    se l'oggetto creato sarà IPv4 o IPv6.
    """
    if ":" in cidr_input:
        return IPv6Network(cidr_input)
    else:
        return IPv4Network(cidr_input)
