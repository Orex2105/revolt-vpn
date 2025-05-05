from pydantic import BaseModel


class XUICredentials(BaseModel):
    username: str
    password: str


class BotCredentials(BaseModel):
    token: str


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
    cpu_cores: int


class SubscriptionsCredentials(BaseModel):
    profile_title: str
    support_url: str
    update_interval: str
    profile_web_page_url: str
    announce_text: str
    announce_url: str


class ServerIsAlive(BaseModel):
    status: bool
    last_check: str


class ClientSubData(BaseModel):
    up: int
    down: int
    total_spent: int
    limitation: int
    expiry_time: int