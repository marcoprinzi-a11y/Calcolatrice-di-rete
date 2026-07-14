import abc
import re
from typing import Dict, Any, Tuple, List

class NetworkObject(abc.ABC):
    CIDR_PATTERN = re.compile(r"^([0-9a-fA-F\.\:]+)/(\d+)$")

def __init__(self, raw_input: str):
    self.raw_input = raw_input.strip()
    self.ip_str, self.prefix_len = self._validate_and_parse()

