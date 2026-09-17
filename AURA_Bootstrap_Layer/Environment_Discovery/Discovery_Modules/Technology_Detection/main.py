from .Detection_Modules.language_detection import LanguageDetectionModule
from .Detection_Modules.framework_detection import FrameworkDetectionModule
from .Detection_Modules.runtime_detection import RuntimeDetectionModule
from .Detection_Modules.library_detection import LibraryDetectionModule
from .Detection_Modules.database_detection import DatabaseDetectionModule
from .Detection_Modules.messaging_detection import MessagingDetectionModule
from .Detection_Modules.version_detection import VersionDetectionModule

class TechnologyDetectionModule:

    # language
    def Detect_Language(self, files):

        language_mod = LanguageDetectionModule(files)

        return language_mod.Language_Detector()

    #framework
    def Detect_Framework(self, files):

        framework_mod = FrameworkDetectionModule(files)

        return framework_mod.Framework_Detector()

    #runtime 
    def Detect_Runtime(self,files):

        runtime_mod = RuntimeDetectionModule(files)

        return runtime_mod.Runtime_Detector()

    #library
    def Detect_Library(self, files):

        library_mod = LibraryDetectionModule(files)

        return library_mod.Library_Detector()

    #database
    def Detect_Database(self, files):

        database_mod = DatabaseDetectionModule(files)

        return database_mod.Database_Detector()

    #messaging
    def Detect_Messaging(self, files):
    
            messaging_mod = MessagingDetectionModule(files)
    
            return messaging_mod.Messaging_Detector()

    #version
    def Detect_Version(self, files, technology_data):

         version_mod = VersionDetectionModule(files, technology_data)

         return version_mod.Version_Detector()