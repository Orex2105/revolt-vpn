from pydantic import BaseModel


class XUICredentials(BaseModel):
    username: str
    password: str
    emojis: list[str]


class ServerStatus(BaseModel):
    public_ip_v4: str
    public_ip_v6: str
    cpu_load: float
    memory_usage: float
    memory_total: float
    uptime: int
    cpu_speed: float
    disk_memory_total: float
    disk_memory_current: float
    xray_state: str
    xray_version: str