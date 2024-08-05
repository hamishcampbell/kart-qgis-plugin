from qgis.core import QgsProcessingProvider


from kart.processing.tools import (
    RepoClone,
    RepoInit,
    RepoSwitchBranch,
    RepoCreateBranch,
    RepoDeleteBranch,
)


class KartProvider(QgsProcessingProvider):

    def loadAlgorithms(self, *args, **kwargs):

        self.addAlgorithm(RepoInit())
        self.addAlgorithm(RepoClone())
        self.addAlgorithm(RepoSwitchBranch())
        self.addAlgorithm(RepoCreateBranch())
        self.addAlgorithm(RepoDeleteBranch())

    def id(self, *args, **kwargs):
        return "Kart"

    def name(self, *args, **kwargs):
        return self.tr("Kart")

    def icon(self):
        from kart.plugin import kartIcon

        return kartIcon
