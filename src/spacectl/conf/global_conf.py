import os
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.dirname(BASE_DIR)
DEFAULT_TEMPLATE_DIR = os.path.join(BASE_DIR, 'template')
ASSET_DIR = os.path.join(BASE_DIR, 'asset')

HOME_DIR = str(Path.home())
CONFIG_DIR = os.path.join(HOME_DIR, '.spaceone')
TEMPLATE_DIR = os.path.join(CONFIG_DIR, 'template')
ENVIRONMENT_CONF_PATH = os.path.join(CONFIG_DIR, 'environment.yml')
ENVIRONMENT_DIR = os.path.join(CONFIG_DIR, 'environments')

DEFAULT_ENVIRONMENT = 'default'
DEFAULT_PARSER = 'spacectl.lib.parser.default.DefaultParser'

RESOURCE_ALIAS = {
    # Identity
    'domain': ['identity', 'Domain'],
    'domain_owner': ['identity', 'DomainOwner'],
    'project': ['identity', 'Project'],
    'project_group': ['identity', 'ProjectGroup'],
    'pg': ['identity', 'ProjectGroup'],
    'user': ['identity', 'User'],
    'api_key': ['identity', 'APIKey'],
    'policy': ['identity', 'Policy'],
    'role': ['identity', 'Role'],
    'provider': ['identity', 'Provider'],
    'service_account': ['identity', 'ServiceAccount'],
    'sa': ['identity', 'ServiceAccount'],
    'endpoint': ['identity', 'Endpoint'],

    # Inventory
    'region': ['inventory', 'Region'],
    'cloud_service': ['inventory', 'CloudService'],
    'cloud_service_type': ['inventory', 'CloudServiceType'],
    'cs': ['inventory', 'CloudService'],
    'cloud_service_query_set': ['inventory', 'CloudServiceQuerySet'],
    'cloud_service_stats': ['inventory', 'CloudServiceStats'],
    'resource_group': ['inventory', 'ResourceGroup'],
    'rg': ['inventory', 'ResourceGroup'],
    'collector': ['inventory', 'Collector'],

    # Config
    'user_config': ['config', 'UserConfig'],
    'domain_config': ['config', 'UserConfig'],

    # Repository
    'repository': ['repository', 'Repository'],
    'repo': ['repository', 'Repository'],
    'plugin': ['repository', 'Plugin'],
    'schema': ['repository', 'Schema'],

    # Secret
    'secret': ['secret', 'Secret'],

    # Monitoring
    'metric': ['monitoring', 'Metric'],
    'log': ['monitoring', 'Log'],
    'project_alert_config': ['monitoring', 'ProjectAlertConfig'],
    'escalation_policy': ['monitoring', 'EscalationPolicy'],
    'webhook': ['monitoring', 'Webhook'],
    'maintenance_window': ['monitoring', 'MaintenanceWindow'],
    'alert': ['monitoring', 'Alert'],
    'event': ['monitoring', 'Event'],

    # Notification
    'protocol': ['notification', 'Protocol'],
    'project_channel': ['notification', 'ProjectChannel'],
    'ph': ['notification', 'ProjectChannel'],
    'user_channel': ['notification', 'UserChannel'],
    'uh': ['notification', 'UserChannel'],
    'notification': ['notification', 'Notification'],
    'noti': ['notification', 'Notification'],

    # Cost Analysis
    'cost': ['cost_analysis', 'Cost'],
    'budget': ['cost_analysis', 'Budget'],
    'budget_usage': ['cost_analysis', 'BudgetUsage'],

    # Board
    'board': ['board', 'Board'],
    'post': ['board', 'Post'],

    # Dashboard
    'cw': ['dashboard', 'CustomWidget'],
    'domain_dashboard': ['dashboard', 'DomainDashboard'],
    'project_dashboard': ['dashboard', 'ProjectDashboard']
}

EXCLUDE_APIS = [
    # 'identity.Domain.create',
    # 'identity.Domain.update',
]
