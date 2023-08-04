from dataclasses import dataclass

@dataclass
class Config:
    BASE_URL: str = "https://bumblebee.hive.swarm.space/hive"
    CONTENT_TYPE: str = "application/x-www-form-urlencoded"
    DEVICE_TYPE: int = 1  # Swarm M138 Modem
