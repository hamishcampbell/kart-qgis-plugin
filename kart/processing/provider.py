from qgis.core import QgsProcessingProvider

from kart.gui import icons
from kart.processing.tools import (
    RepoClone,
    RepoInit,
    RepoSwitchBranch,
    RepoCreateBranch,
    RepoDeleteBranch,
    RepoPullFromRemote,
    RepoPushToRemote,
)


class KartProvider(QgsProcessingProvider):
    def loadAlgorithms(self, *args, **kwargs):

        self.addAlgorithm(RepoInit())
        self.addAlgorithm(RepoClone())
        self.addAlgorithm(RepoSwitchBranch())
        self.addAlgorithm(RepoCreateBranch())
        self.addAlgorithm(RepoDeleteBranch())
        self.addAlgorithm(RepoPullFromRemote())
        self.addAlgorithm(RepoPushToRemote())

    def id(self, *args, **kwargs):
        return "Kart"

    def name(self, *args, **kwargs):
        return self.tr("Kart")

    def icon(self):
        return icons.kartIcon
