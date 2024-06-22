import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.mgmt.containerinstance import ContainerInstanceManagementClient

# Configuración de credenciales y variables
credential = DefaultAzureCredential()
key_vault_name = "radio-bot-vault"
subscription_secret_name = "az-sub-id"
resource_group = "radio-bot"
container_instance_name = "radio-bot-container"  # Nombre de la instancia de contenedor única

# Cliente para interactuar con Azure Key Vault
keyvault_url = f"https://{key_vault_name}.vault.azure.net"
secret_client = SecretClient(vault_url=keyvault_url, credential=credential)
try:
    # Obtener el Subscription ID desde Key Vault
    subscription_id = secret_client.get_secret(subscription_secret_name).value
except Exception as e:
    logging.error(f"Error: {e}")
    raise Exception(f"Error: {e}")

# Cliente para interactuar con Azure Container Instances
aci_client = ContainerInstanceManagementClient(credential, subscription_id)

def start_container_instance(resource_group, container_instance_name):
    logging.info(f"Starting container instance: {container_instance_name}")
    aci_client.container_groups.begin_start(resource_group, container_instance_name)

def stop_container_instance(resource_group, container_instance_name):
    logging.info(f"Stopping container instance: {container_instance_name}")
    aci_client.container_groups.begin_delete(resource_group, container_instance_name)

def get_container_instance_state(resource_group, container_instance_name):
    logging.info(f"Getting state of container instance: {container_instance_name}")
    instance = aci_client.container_groups.get(resource_group, container_instance_name)
    return instance.instance_view.state

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        action = req_body.get('action')
        
        if action == "start":
            start_container_instance(resource_group, container_instance_name)
            return func.HttpResponse(f"Container instance {container_instance_name} started.", status_code=200)
        elif action == "stop":
            stop_container_instance(resource_group, container_instance_name)
            return func.HttpResponse(f"Container instance {container_instance_name} stopped.", status_code=200)
        elif action == "state":
            container_state = get_container_instance_state(resource_group, container_instance_name)
            return func.HttpResponse(f"Container instance {container_instance_name} state: {container_state}", status_code=200)
        else:
            return func.HttpResponse("Invalid action. Use 'start', 'stop', or 'state'.", status_code=400)
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
