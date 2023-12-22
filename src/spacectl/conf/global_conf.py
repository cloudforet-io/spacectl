import os
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.dirname(BASE_DIR)
DEFAULT_TEMPLATE_DIR = os.path.join(BASE_DIR, "template")
ASSET_DIR = os.path.join(BASE_DIR, "asset")

HOME_DIR = str(Path.home())
CONFIG_DIR = os.path.join(HOME_DIR, ".spaceone")
TEMPLATE_DIR = os.path.join(CONFIG_DIR, "template")
ENVIRONMENT_CONF_PATH = os.path.join(CONFIG_DIR, "environment.yml")
ENVIRONMENT_DIR = os.path.join(CONFIG_DIR, "environments")

DEFAULT_ENVIRONMENT = "default"
DEFAULT_PARSER = "spacectl.lib.parser.default.DefaultParser"
RESOURCE_ALIAS = {
    # Identity
    "domain": ["identity", "Domain"],
    "endpoint": ["identity", "Endpoint"],
    "workspace": ["identity", "Workspace"],
    "project": ["identity", "Project"],
    "project_group": ["identity", "ProjectGroup"],
    "pg": ["identity", "ProjectGroup"],
    "user": ["identity", "User"],
    "api_key": ["identity", "APIKey"],
    "policy": ["identity", "Policy"],
    "role": ["identity", "Role"],
    "role_binding": ["identity", "RoleBinding"],
    "rb": ["identity", "RoleBinding"],
    "user_profile": ["identity", "UserProfile"],
    "up": ["identity", "UserProfile"],
    "workspace_user": ["identity", "WorkspaceUser"],
    "wu": ["identity", "WorkspaceUser"],
    "user_group": ["identity", "UserGroup"],
    "ug": ["identity", "UserGroup"],
    "app": ["identity", "App"],
    "token": ["identity", "Token"],
    "provider": ["identity", "Provider"],
    "service_account": ["identity", "ServiceAccount"],
    "sa": ["identity", "ServiceAccount"],
    "trusted_account": ["identity", "TrustedAccount"],
    "ta": ["identity", "TrustedAccount"],
    # Secret
    "secret": ["secret", "Secret"],
    "ts": ["secret", "TrustedSecret"],
    # Inventory
    "region": ["inventory", "Region"],
    "cloud_service": ["inventory", "CloudService"],
    "cs": ["inventory", "CloudService"],
    "cloud_service_type": ["inventory", "CloudServiceType"],
    "cst": ["inventory", "CloudServiceType"],
    "cloud_service_report": ["inventory", "CloudServiceReport"],
    "csr": ["inventory", "CloudServiceReport"],
    "cloud_service_query_set": ["inventory", "CloudServiceQuerySet"],
    "cloud_service_stats": ["inventory", "CloudServiceStats"],
    "change_history": ["inventory", "ChangeHistory"],
    "note": ["inventory", "Note"],
    "collector": ["inventory", "Collector"],
    "collector_rule": ["inventory", "CollectorRule"],
    "cr": ["inventory", "CollectorRule"],
    # Config
    "user_config": ["config", "UserConfig"],
    "domain_config": ["config", "DomainConfig"],
    # Repository
    "repository": ["repository", "Repository"],
    "repo": ["repository", "Repository"],
    "plugin": ["repository", "Plugin"],
    # Monitoring
    "metric": ["monitoring", "Metric"],
    "log": ["monitoring", "Log"],
    "escalation_policy": ["monitoring", "EscalationPolicy"],
    "ep": ["monitoring", "EscalationPolicy"],
    "event_rule": ["monitoring", "EventRule"],
    "er": ["monitoring", "EventRule"],
    "webhook": ["monitoring", "Webhook"],
    "maintenance_window": ["monitoring", "MaintenanceWindow"],
    "alert": ["monitoring", "Alert"],
    "event": ["monitoring", "Event"],
    # Notification
    "protocol": ["notification", "Protocol"],
    "project_channel": ["notification", "ProjectChannel"],
    "ph": ["notification", "ProjectChannel"],
    "user_channel": ["notification", "UserChannel"],
    "uh": ["notification", "UserChannel"],
    "notification": ["notification", "Notification"],
    "noti": ["notification", "Notification"],
    # Cost Analysis
    "cost": ["cost_analysis", "Cost"],
    "ds": ["cost_analysis", "DataSource"],
    "dsr": ["cost_analysis", "DataSourceRule"],
    "budget": ["cost_analysis", "Budget"],
    "budget_usage": ["cost_analysis", "BudgetUsage"],
    "cost_query_set": ["cost_analysis", "CostQuerySet"],
    # Board
    "board": ["board", "Board"],
    # File Manager
    "file": ["file_manager", "File"],
    # Dashboard
    "public_dashboard": ["dashboard", "PublicDashboard"],
    "pub_d": ["dashboard", "PublicDashboard"],
    "private_dashboard": ["dashboard", "PrivateDashboard"],
    "pri_d": ["dashboard", "PrivateDashboard"],
}

EXCLUDE_APIS = [
    # 'identity.Domain.create',
    # 'identity.Domain.update',
]
