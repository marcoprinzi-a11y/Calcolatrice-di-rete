import abc
import re
from typing import Dict, Any, Tuple, List
"classe base astratta (modello di base)"
class NetworkObject(abc.ABC):
    CIDR_PATTERN = re.compile(r"^([0-9a-fA-F\.\:]+)/(\d+)$")
"costruttore classe"
def __init__(self, raw_input: str):
    self.raw_input = raw_input.strip()
    self.ip_str, self.prefix_len = self._validate_and_parse()

    def _validate_and_parse(self) -> Tuple[str, int]:
        "Valida la sintassi della stringa in ingresso usando regex."
        match = self.CIDR_PATTERN.match(self.raw_input)
        if not match:
            raise ValueError(
                f"Formato non valido: '{self.raw_input}'. Usa la notazione CIDR (es. 192.168.1.1/24 o 2001:db8::/64).")

        ip, prefix = match.groups()
        return ip, int(prefix)

    @abc.abstractmethod
    def get_network_summary(self) -> Dict[str, Any]:
        "restituisce un riepilogo dettagliato della rete."
        pass

    @abc.abstractmethod
    def get_host_range(self) -> Tuple[str, str]:
        "restituisce il primo e l'ultimo host utilizzabili."
        pass


class IPv4Network(NetworkObject):
    """
    Rappresenta una rete IPv4. Specializza i calcoli matematici su 32 bit.
    """

    def __init__(self, raw_input: str):
        # Uso corretto di super() per delegare la validazione iniziale alla classe base
        super().__init__(raw_input)

        if not 0 <= self.prefix_len <= 32:
            raise ValueError("Prefisso IPv4 non valido (deve essere compreso tra 0 e 32).")

        self.ip_int = self._ip_to_int(self.ip_str)
        self.mask_int = (0xFFFFFFFF << (32 - self.prefix_len)) & 0xFFFFFFFF
        self.network_int = self.ip_int & self.mask_int
        self.broadcast_int = self.network_int | (~self.mask_int & 0xFFFFFFFF)

        def _ip_to_int(self, ip_str: str) -> int:
            """Converte una stringa IPv4 in un intero a 32 bit."""
            parts = ip_str.split('.')
            if len(parts) != 4:
                raise ValueError(f"Indirizzo IPv4 non valido: {ip_str}")
            try:
                octets = [int(p) for p in parts if 0 <= int(p) <= 255]
                if len(octets) != 4:
                    raise ValueError()
            except ValueError:
                raise ValueError(f"Ottetti IPv4 non validi: {ip_str}")

            return (octets[0] << 24) + (octets[1] << 16) + (octets[2] << 8) + octets[3]

        def _int_to_ip(self, ip_int: int) -> str:
            """Converte un intero a 32 bit in una stringa IPv4 decimale puntata."""
            return f"{(ip_int >> 24) & 255}.{(ip_int >> 16) & 255}.{(ip_int >> 8) & 255}.{ip_int & 255}"

        def get_host_range(self) -> Tuple[str, str]:
            """Calcola l'intervallo di host IPv4 utilizzabili (escludendo Rete e Broadcast)."""
            if self.prefix_len >= 31:
                # Nei collegamenti point-to-point /31 o host singoli /32 non c'è il range classico
                return self._int_to_ip(self.network_int), self._int_to_ip(self.broadcast_int)

            first_host = self.network_int + 1
            last_host = self.broadcast_int - 1
            return self._int_to_ip(first_host), self._int_to_ip(last_host)

        def get_network_summary(self) -> Dict[str, Any]:
            """Implementazione dell'override polimorfico per IPv4."""
            first_host, last_host = self.get_host_range()
            total_hosts = 2 ** (32 - self.prefix_len)
            usable_hosts = total_hosts - 2 if self.prefix_len < 31 else total_hosts

            return {
                "Protocollo": "IPv4",
                "Indirizzo Base": self.ip_str,
                "Sotto-Maschera": self._int_to_ip(self.mask_int),
                "Prefisso CIDR": f"/{self.prefix_len}",
                "Indirizzo Rete": self._int_to_ip(self.network_int),
                "Indirizzo Broadcast": self._int_to_ip(self.broadcast_int),
                "Range Host": f"{first_host} - {last_host}",
                "Host Totali": total_hosts,
                "Host Utilizzabili": usable_hosts,
                "Privato": self._is_private()
            }

        def _is_private(self) -> bool:
            """Verifica se l'IP appartiene alle classi private RFC 1918."""
            # 10.0.0.0/8
            if (self.network_int & 0xFF000000) == 0x0A000000:
                return True
            # 172.16.0.0/12
            if (self.network_int & 0xFFF00000) == 0xAC100000:
                return True
            # 192.168.0.0/16
            if (self.network_int & 0xFFFF0000) == 0xC0A80000:
                return True
            return False