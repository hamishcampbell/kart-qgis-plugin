from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterFile,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsProcessingParameterExtent,
    QgsProcessingParameterFolderDestination,
    QgsProcessingOutputMultipleLayers,
    QgsReferencedRectangle,
)
from kart.gui import icons


class KartAlgorithm(QgsProcessingAlgorithm):
    def createInstance(self):
        return type(self)()

    def name(self):
        return f"kart_{self.__class__.__name__.lower()}"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)


class RepoInit(KartAlgorithm):
    REPO_PATH = "REPO_PATH"

    def displayName(self):
        return self.tr("Create Empty Repo")

    def shortHelpString(self):
        return self.tr("Create a new empty repository")

    def icon(self):
        return icons.createRepoIcon

    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterFile(
                self.REPO_PATH,
                self.tr("Repo Path"),
                behavior=QgsProcessingParameterFile.Folder,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        from kart.kartapi import Repository

        repo_path = self.parameterAsString(parameters, self.REPO_PATH, context)

        repo = Repository(repo_path)
        repo.init()

        return {self.REPO_PATH: repo_path}


class RepoClone(KartAlgorithm):
    REPO_CLONE_URL = "REPO_CLONE_URL"
    REPO_CLONE_REFISH = "REPO_CLONE_REFISH"
    REPO_CLONE_DEPTH = "REPO_CLONE_DEPTH"
    REPO_CLONE_SPATIAL_EXTENT = "REPO_CLONE_SPATIAL_EXTENT"
    REPO_OUTPUT_FOLDER = "REPO_OUTPUT_FOLDER"
    REPO_ADD_TO_MAP = "REPO_ADD_TO_MAP"
    REPO_OUTPUT_LAYERS = "REPO_OUTPUT_LAYERS"

    def displayName(self):
        return self.tr("Clone Repo")

    def shortHelpString(self):
        return self.tr("Clones a repository to a folder")

    def icon(self):
        return icons.cloneRepoIcon

    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterString(
                self.REPO_CLONE_URL,
                self.tr("Repo URL"),
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.REPO_CLONE_REFISH,
                self.tr("Branch/Tag/Ref"),
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterExtent(
                self.REPO_CLONE_SPATIAL_EXTENT,
                self.tr("Spatial Extent"),
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.REPO_CLONE_DEPTH,
                self.tr("Depth"),
                type=QgsProcessingParameterNumber.Integer,
                optional=True,
                minValue=1,
            )
        )

        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.REPO_OUTPUT_FOLDER, self.tr("Output folder")
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.REPO_ADD_TO_MAP, self.tr("Add layers to the Map")
            )
        )

        self.addOutput(
            QgsProcessingOutputMultipleLayers(
                self.REPO_OUTPUT_LAYERS,
                self.tr("Output Layers"),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        from kart.kartapi import Repository

        repo_url = self.parameterAsString(parameters, self.REPO_CLONE_URL, context)
        folder = self.parameterAsFile(parameters, self.REPO_OUTPUT_FOLDER, context)
        refish = self.parameterAsString(parameters, self.REPO_CLONE_REFISH, context)
        depth = self.parameterAsInt(parameters, self.REPO_CLONE_DEPTH, context)
        add_layers = self.parameterAsBool(parameters, self.REPO_ADD_TO_MAP, context)

        extent_rect = self.parameterAsExtent(parameters, self.REPO_CLONE_DEPTH, context)
        extent_crs = self.parameterAsExtentCrs(
            parameters, self.REPO_CLONE_SPATIAL_EXTENT, context
        )
        extent = None
        if parameters.get(self.REPO_CLONE_SPATIAL_EXTENT):
            extent = QgsReferencedRectangle(extent_rect, extent_crs)

        repo = Repository.clone(repo_url, folder, extent=extent, depth=depth or None)
        if refish:
            repo.checkoutBranch(refish)

        layers = []
        vector_datasets, table_datasets = repo.datasets()
        for dataset in vector_datasets:
            layers.append(repo.workingCopyLayer(dataset))
        for dataset in table_datasets:
            layers.append(repo.workingCopyLayer(dataset))

        if add_layers:
            for layer in layers:
                context.context.addLayerToLoadOnCompletion(layer)

        return {
            self.REPO_OUTPUT_FOLDER: folder,
            self.REPO_OUTPUT_LAYERS: layers,
        }


class RepoCreateBranch(KartAlgorithm):
    REPO_PATH = "REPO_PATH"
    REPO_BRANCH_NAME = "REPO_BRANCH_NAME"

    def displayName(self):
        return self.tr("Create Branch")

    def shortHelpString(self):
        return self.tr("Create a new branch")

    def icon(self):
        return icons.createBranchIcon

    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterFile(
                self.REPO_PATH,
                self.tr("Repo Path"),
                behavior=QgsProcessingParameterFile.Folder,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.REPO_BRANCH_NAME,
                self.tr("Branch Name"),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        from kart.kartapi import Repository

        repo_path = self.parameterAsFile(parameters, self.REPO_PATH, context)
        branch_name = self.parameterAsString(parameters, self.REPO_REFISH, context)

        repo = Repository(repo_path)
        repo.createBranch(branch_name)

        return {
            self.REPO_PATH: repo_path,
        }


class RepoSwitchBranch(KartAlgorithm):
    REPO_PATH = "REPO_PATH"
    REPO_BRANCH_NAME = "REPO_BRANCH_NAME"

    def displayName(self):
        return self.tr("Switch to Branch")

    def shortHelpString(self):
        return self.tr("Switches to a named branch")

    def icon(self):
        return icons.checkoutIcon

    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterFile(
                self.REPO_PATH,
                self.tr("Repo Path"),
                behavior=QgsProcessingParameterFile.Folder,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.REPO_BRANCH_NAME,
                self.tr("Branch Name"),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        from kart.kartapi import Repository

        repo_path = self.parameterAsFile(parameters, self.REPO_PATH, context)
        branch_name = self.parameterAsString(parameters, self.REPO_BRANCH_NAME, context)

        repo = Repository(repo_path)
        repo.checkoutBranch(branch_name)

        return {
            self.REPO_PATH: repo_path,
        }


class RepoDeleteBranch(KartAlgorithm):
    REPO_PATH = "REPO_PATH"
    REPO_BRANCH_NAME = "REPO_BRANCH_NAME"

    def displayName(self):
        return self.tr("Delete Branch")

    def shortHelpString(self):
        return self.tr("Delete a branch")

    def icon(self):
        return icons.deleteIcon

    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterFile(
                self.REPO_PATH,
                self.tr("Repo Path"),
                behavior=QgsProcessingParameterFile.Folder,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.REPO_BRANCH_NAME,
                self.tr("Branch Name"),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        from kart.kartapi import Repository

        repo_path = self.parameterAsFile(parameters, self.REPO_PATH, context)
        branch_name = self.parameterAsString(parameters, self.REPO_REFISH, context)

        repo = Repository(repo_path)
        repo.deleteBranch(branch_name)

        return {
            self.REPO_PATH: repo_path,
        }


class RepoDeleteBranch(KartAlgorithm):
    REPO_PATH = "REPO_PATH"
    REPO_BRANCH_NAME = "REPO_BRANCH_NAME"

    def displayName(self):
        return self.tr("Delete Branch")

    def shortHelpString(self):
        return self.tr("Delete a branch")

    def icon(self):
        return icons.deleteIcon

    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterFile(
                self.REPO_PATH,
                self.tr("Repo Path"),
                behavior=QgsProcessingParameterFile.Folder,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.REPO_BRANCH_NAME,
                self.tr("Branch Name"),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        from kart.kartapi import Repository

        repo_path = self.parameterAsFile(parameters, self.REPO_PATH, context)
        branch_name = self.parameterAsString(parameters, self.REPO_BRANCH_NAME, context)

        repo = Repository(repo_path)
        repo.deleteBranch(branch_name)

        return {
            self.REPO_PATH: repo_path,
        }


class RepoPushToRemote(KartAlgorithm):
    REPO_PATH = "REPO_PATH"
    REPO_BRANCH_NAME = "REPO_BRANCH_NAME"
    REPO_REMOTE_NAME = "REPO_REMOTE_NAME"

    def displayName(self):
        return self.tr("Push Changes to Remote")

    def shortHelpString(self):
        return self.tr("Sync changes in a repository to a remote location")

    def icon(self):
        return icons.pushIcon

    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterFile(
                self.REPO_PATH,
                self.tr("Repo Path"),
                behavior=QgsProcessingParameterFile.Folder,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.REPO_BRANCH_NAME,
                self.tr("Branch Name"),
                defaultValue="main",
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.REPO_REMOTE_NAME,
                self.tr("Remote Name"),
                defaultValue="origin",
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        from kart.kartapi import Repository

        repo_path = self.parameterAsFile(parameters, self.REPO_PATH, context)
        branch_name = self.parameterAsString(parameters, self.REPO_BRANCH_NAME, context)
        remote_name = self.parameterAsString(parameters, self.REPO_REMOTE_NAME, context)

        repo = Repository(repo_path)
        repo.push(remote_name, branch_name)

        return {
            self.REPO_PATH: repo_path,
        }


class RepoPullFromRemote(KartAlgorithm):
    REPO_PATH = "REPO_PATH"
    REPO_BRANCH_NAME = "REPO_BRANCH_NAME"
    REPO_REMOTE_NAME = "REPO_REMOTE_NAME"

    def displayName(self):
        return self.tr("Pull Changes from Remote")

    def shortHelpString(self):
        return self.tr("Sync changes in a remote location to a local repository")

    def icon(self):
        return icons.pullIcon

    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterFile(
                self.REPO_PATH,
                self.tr("Repo Path"),
                behavior=QgsProcessingParameterFile.Folder,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.REPO_BRANCH_NAME,
                self.tr("Branch Name"),
                defaultValue="main",
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.REPO_REMOTE_NAME,
                self.tr("Remote Name"),
                defaultValue="origin",
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        from kart.kartapi import Repository

        repo_path = self.parameterAsFile(parameters, self.REPO_PATH, context)
        branch_name = self.parameterAsString(parameters, self.REPO_BRANCH_NAME, context)
        remote_name = self.parameterAsString(parameters, self.REPO_REMOTE_NAME, context)

        repo = Repository(repo_path)
        repo.pull(remote_name, branch_name)

        return {
            self.REPO_PATH: repo_path,
        }
