from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterString,
    QgsProcessingParameterFolderDestination,
)


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

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterString(
                self.REPO_PATH,
                self.tr("Repo Path"),
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
    REPO_OUTPUT_FOLDER = "REPO_OUTPUT_FOLDER"

    def displayName(self):
        return self.tr("Clone Repo")

    def shortHelpString(self):
        return self.tr("Clones a repository to a folder")

    def group(self):
        return self.tr("Repositories")

    def groupId(self):
        return "kart_repositories"

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
                self.tr("Branch/Tag/Refish"),
                optional=True,
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
        folder = self.parameterAsString(parameters, self.REPO_OUTPUT_FOLDER, context)
        refish = self.parameterAsString(parameters, self.REPO_CLONE_REFISH, context)

        repo = Repository.clone(repo_url, folder)
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

        repo_path = self.parameterAsString(parameters, self.REPO_PATH, context)
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

        repo_path = self.parameterAsString(parameters, self.REPO_PATH, context)
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

        repo_path = self.parameterAsString(parameters, self.REPO_PATH, context)
        branch_name = self.parameterAsString(parameters, self.REPO_REFISH, context)

        repo = Repository(repo_path)
        repo.deleteBranch(branch_name)

        return {
            self.REPO_PATH: repo_path,
        }
