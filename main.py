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