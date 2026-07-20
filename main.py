import sys
import argparse
import json
from typing import List
from network import NetworkObject, IPv4Network, IPv6Network

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
    "Formatta e stampa a video i risultati dell'analisi."
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


def main():
    parser = argparse.ArgumentParser(
        description="SubnetCalc-X: Calcolatrice di Rete Didattica per Esame Finale."
    )
    parser.add_argument(
        "cidr",
        type=str,
        help="L'indirizzo di rete in formato CIDR (es: 192.168.10.1/24 o fc00::/64)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        choices=["text", "json"],
        default="text",
        help="Scegli il formato di output (predefinito: text)"
    )

    args = parser.parse_args()

    try:
        # Polimorfismo in azione:
        # 1. Creiamo l'oggetto senza sapere quale classe concreta stiamo usando
        network: NetworkObject = create_network_object(args.cidr)

        # 2. Invochiamo il metodo polimorfico 'get_network_summary()'
        # Il main non sa se sta parlando con un'istanza IPv4 o IPv6, sa solo che espone questo metodo.
        summary_data = network.get_network_summary()

        if args.output == "json":
            print(json.dumps(summary_data, indent=4))
        else:
            print_pretty_summary(summary_data)

    except ValueError as e:
        print(f"Errore di Validazione: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Errore Inaspettato: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

