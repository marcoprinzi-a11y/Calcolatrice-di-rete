import argparse
import json
from network import NetworkObject, IPv4Network, IPv6Network


def create_network_object(cidr_input: str) -> NetworkObject:
    """Factory function che istanzia la classe corretta in base all'IP."""
    ip_part = cidr_input.split('/')[0]
    if ':' in ip_part:
        return IPv6Network(cidr_input)
    return IPv4Network(cidr_input)


def main():
    parser = argparse.ArgumentParser(description="Calcolatrice di Rete CLI per IPv4 e IPv6")
    parser.add_argument("cidr", type=str, help="Indirizzo IP in notazione CIDR (es. 192.168.1.10/24 o 2001:db8::/64)")
    parser.add_argument("-o", "--output", choices=["text", "json"], default="text", help="Formato di output (default: text)")

    args = parser.parse_args()

    try:
        net = create_network_object(args.cidr)
        summary = net.get_network_summary()

        if args.output == "json":
            print(json.dumps(summary, indent=4, ensure_ascii=False))
        else:
            print("\n" + "=" * 35)
            print("     RIEPILOGO CALCOLO RETE     ")
            print("=" * 35)
            for k, v in summary.items():
                print(f"{k:<20}: {v}")
            print("=" * 35 + "\n")

    except Exception as e:
        print(f"Errore: {e}")


if __name__ == "__main__":
    main()