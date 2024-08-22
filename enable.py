from google.cloud import monitoring_v3
from google.protobuf import field_mask_pb2 as field_mask

def enable_alert_policies(project_name, enable, filter_=None):
    """Enable or disable alert policies in a project.

    Arguments:
        project_name (str): The Google Cloud Project to use. The project name
            must be in the format - 'projects/<PROJECT_NAME>'.
        enable (bool): Enable or disable the policies.
        filter_ (str, optional): Only enable/disable alert policies that match
            this filter_.  See
            https://cloud.google.com/monitoring/api/v3/sorting-and-filtering
    """

    client = monitoring_v3.AlertPolicyServiceClient()

    # Handle potential pagination of policies
    request = {"name": project_name, "filter": filter_}
    policies = client.list_alert_policies(request=request)
    print(policies)

    for policy in policies:
        if bool(enable) == policy.enabled:
            print(
                "Policy",
                policy.name,
                "is already",
                "enabled" if policy.enabled else "disabled",
            )
        else:
            policy.enabled = bool(enable)
            mask = field_mask.FieldMask(paths=["enabled"])
            client.update_alert_policy(alert_policy=policy, update_mask=mask)
            print("Enabled" if enable else "Disabled", policy.name)

# Example usage
if __name__ == "__main__":
    project_name = "projects/plated-planet-427716-u5"
    enable = True # Set to False to disable
    filter_ = None  # Add a filter if needed
    enable_alert_policies(project_name, enable, filter_)
