#modules
from .Discovery_Modules.Technology_Detection.main import TechnologyDetectionModule
from .Discovery_Modules.Application_Discovery.main import ApplicationDiscoveryModule
from .Discovery_Modules.Deployment_Detection.main import DeploymentDetectionModule

from .Discovery_Modules.file_scanner import FileScanner
from .Discovery_Modules.file_filter import FileFilter

from .Discovery_Modules.Environment_Profiling.environment_profile import EnvironmentProfileModule

class DiscoveryModules:

    def __init__(self, TARGET_APPLICATION_PATH):

        self.TARGET_APPLICATION_PATH = TARGET_APPLICATION_PATH

        # File Scanner
        file_scanner = FileScanner(TARGET_APPLICATION_PATH)

        self.scanned_files = file_scanner.scan()
        
        # File Filter
        file_filter = FileFilter(self.scanned_files)

        self.filtered_files = file_filter.filter()


    #Application Discovery
    def Application_Discovery(self):

        application_discovery = ApplicationDiscoveryModule()


        #Identify application
        application = application_discovery.Application_Identification(
            self.filtered_files
        )


        #Discover services
        services = application_discovery.Service_Discovery(
            self.TARGET_APPLICATION_PATH
        )

        #Discover endpoints
        endpoints = application_discovery.Endpoint_Discovery(
            self.filtered_files
        )


        #Application metadata
        metadata = application_discovery.Application_Metadata(
            self.TARGET_APPLICATION_PATH,
            self.filtered_files
        )

        return{
            "application": application,
            "services" : services,
            "endpoints" : endpoints,
            "metadata" : metadata,
        }

    #Technology Detection
    def Technology_Detection(self):

        technology_detection = TechnologyDetectionModule()

        #Detect Language 
        language = technology_detection.Detect_Language(self.filtered_files)

        #Detect Framework
        framework = technology_detection.Detect_Framework(self.filtered_files)

        #Detect Runtime
        runtime = technology_detection.Detect_Runtime(self.filtered_files) 

        #Detect Library
        library = technology_detection.Detect_Library(self.filtered_files)

        #Detect Database
        database = technology_detection.Detect_Database(self.filtered_files)

        #Detect Messaging
        messaging = technology_detection.Detect_Messaging(self.filtered_files)

        technology_data = {
            "language" : language, 
            "framework" : framework,
            "runtime" : runtime,
            "database" : database,
        }

        #Detect Version
        version = technology_detection.Detect_Version(self.filtered_files, technology_data)
        
        return{
            "language" : language, 
            "framework" : framework,
            "runtime" : runtime,
            "library" : library,
            "database" : database,
            "messaging" : messaging,
            "version" : version,
            }

    #Deployment Detection
    def Deployment_Detection(self):

        deployment_detection = DeploymentDetectionModule()

        #Docker
        docker = deployment_detection.Detect_Docker(self.filtered_files) 

        #Docker
        kubernetes = deployment_detection.Detect_Kubernetes(self.filtered_files)

        #Local/VM
        local_vm = deployment_detection.Detect_Local_VM(self.filtered_files)
        
        return{
            "docker" : docker,
            "kubernetes" : kubernetes,
            "local vm" : local_vm,
        }

    #Environment profile
    def Environment_Profile(
        self,
        application_discovery_data,
        technology_detection_data,
        deployment_detection_data
    ):

        environment_profile = EnvironmentProfileModule(

            application_discovery_data,

            technology_detection_data,

            deployment_detection_data
        )

        return environment_profile.Environment_Profiler()