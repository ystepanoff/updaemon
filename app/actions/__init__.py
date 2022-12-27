from .log_action import LogAction
from .email_action import EmailAction

ACTIONS_REGISTRY = {
    'log': LogAction,
}