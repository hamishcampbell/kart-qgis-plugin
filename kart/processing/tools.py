from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterFile,
    QgsProcessingParameterNumber,
    QgsProcessingParameterString,
    QgsProcessingParameterExtent,
    QgsProcessingParameterFolderDestination,
    QgsReferencedRectangle,
)
from kart.gui import icons


class KartAlgorithm(QgsProcessingAlgorithm):
    def createInstance(self):
        return self.__class__()

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

    def group(self):
        return self.tr("Repositories")

    def groupId(self):
        return "kart_repositories"

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

    def displayName(self):
        return self.tr("Clone Repo")

    def shortHelpString(self):
        return self.tr("Clones a repository to a folder")

    def group(self):
        return self.tr("Repositories")

    def groupId(self):
        return "kart_repositories"

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

    def processAlgorithm(self, parameters, context, feedback):
        from kart.kartapi import Repository

        repo_url = self.parameterAsString(parameters, self.REPO_CLONE_URL, context)
        folder = self.parameterAsFile(parameters, self.REPO_OUTPUT_FOLDER, context)
        refish = self.parameterAsString(parameters, self.REPO_CLONE_REFISH, context)
        depth = self.parameterAsInt(parameters, self.REPO_CLONE_DEPTH, context)

        extent_rect = self.parameterAsExtent(
            parameters, self.REPO_CLONE_SPATIAL_EXTENT, context
        )
        extent_crs = self.parameterAsExtentCrs(
            parameters, self.REPO_CLONE_SPATIAL_EXTENT, context
        )
        extent = None
        if extent_rect:
            extent = QgsReferencedRectangle(extent_rect, extent_crs)

        repo = Repository.clone(repo_url, folder, extent=extent, depth=depth)
        if refish:
            repo.checkoutBranch(refish)

        return {
            self.REPO_OUTPUT_FOLDER: folder,
        }


class RepoCreateBranch(KartAlgorithm):
    REPO_PATH = "REPO_PATH"
    REPO_BRANCH_NAME = "REPO_BRANCH_NAME"

    def displayName(self):
        return self.tr("Create Branch")

    def shortHelpString(self):
        return self.tr("Create a new branch")

    def group(self):
        return self.tr("Branches")

    def groupId(self):
        return "kart_branches"

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

    def group(self):
        return self.tr("Branches")

    def groupId(self):
        return "kart_branches"

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

    def group(self):
        return self.tr("Branches")

    def groupId(self):
        return "kart_branches"

    def icon(self):
        return icons.deleteIcon

    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterString(
                self.REPO_PATH,
                self.tr("Repo Path"),
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
