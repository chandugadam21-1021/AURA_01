from Environment_Discovery.main import DiscoveryModules


TARGET_APPLICATION_PATH = "../target-apps/python-app"

# ***Environment Discovery***

# **Discovery_modules**
discovery_mod = DiscoveryModules(TARGET_APPLICATION_PATH)

#Application_Discovery
application_discovery_data = discovery_mod.Application_Discovery()

#Technology_Detection
technology_detection_data = discovery_mod.Technology_Detection()

#Deployment_Detection
deployment_detection_data = discovery_mod.Deployment_Detection()

#Environment_Profile
environment_profile = (
    discovery_mod.Environment_Profile(

        application_discovery_data,

        technology_detection_data,

        deployment_detection_data
    )
)


env_discovery_data = {
    #"APPLICATION DISCOVERY DATA" : application_discovery_data,
    #"TECHNOLOGY DETECTION DATA" : technology_detection_data,
    #"DEPLOYMENT DETECTION DATA" : deployment_detection_data,
    "ENVIRONMENT PROFILE" : environment_profile,
}

print(env_discovery_data)

