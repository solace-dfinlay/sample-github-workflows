import hvac

class VaultClient:
    def __init__(self, vault_addr, github_token):
        """
        Initialize VaultClient with the specified vault address and github token
        """
        self.vault_addr = vault_addr
        self.github_token = github_token
        self.vault_client = self.vault_login_with_github()

    def get_performance_secrets(self):
        """
        Get secrets from vault for performance environment
        client: hvac client
        """
        common_secrets_path = 'tools/githubactions/connectors/performance_secrets'
        read_response = self.vault_client.secrets.kv.v2.read_secret_version(path=common_secrets_path, raise_on_deleted_version=True)
        return read_response['data']['data']
