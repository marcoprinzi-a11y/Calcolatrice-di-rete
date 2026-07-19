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

def print_pretty_summary(summary: dict):
    """Formatta e stampa a video i risultati dell'analisi."""
    print("\n" + "="*45)
    print(f" RISULTATI ANALISI RETE ({summary['Protocollo']}) ")
    print("="*45)
    for key, value in summary.items():
        if key == "Protocollo":
            continue
        # Formatta i numeri grandi in modo leggibile
        if isinstance(value, int):
            value = f"{value:,}".replace(",", ".")
        print(f"{key:<22}: {value}")
    print("="*45 + "\n")


