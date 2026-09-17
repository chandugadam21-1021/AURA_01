from .Application_Discovery_Modules.application_identifier import ApplicationIdentifier
from .Application_Discovery_Modules.service_discovery import ServiceDiscovery
from .Application_Discovery_Modules.endpoint_discovery import EndpointDiscovery
from .Application_Discovery_Modules.application_metadata import ApplicationMetadata


class ApplicationDiscoveryModule:

    # Application Identification
    def Application_Identification(self, filtered_files):

        identifier = ApplicationIdentifier(filtered_files)

        return identifier.identify()

    # Service Discovery
    def Service_Discovery(self, target_application_path):

        discovery = ServiceDiscovery(target_application_path)

        return discovery.discover()

    # Endpoint Discovery
    def Endpoint_Discovery(self, filtered_files):

        discovery = EndpointDiscovery(filtered_files)

        return discovery.discover()

    # Application Metadata
    def Application_Metadata(self, target_application_path, filtered_files):

        metadata = ApplicationMetadata(target_application_path, filtered_files)

        return metadata.collect()