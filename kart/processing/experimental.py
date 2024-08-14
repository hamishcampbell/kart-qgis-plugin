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
    QgsProcessingParameterDefinition,
    QgsProcessingOutputDefinition,
)
from kart.gui import icons


class KartAlgorithm(QgsProcessingAlgorithm):
    def createInstance(self):
        return type(self)()

    def name(self):
        return f"kart_{self.__class__.__name__.lower()}"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def initAlgorithm(self, config=None):
        return {}


# def algo(name: str):
#     def class_decorator(cls):
#         klassName = cls.__name__
#         new_cls = type(klassName, (cls, KartAlgorithm), {
#             "_NAME": name,
#         })
#         return new_cls
#     return class_decorator

# def param(param: QgsProcessingParameterDefinition):
#     def class_decorator(cls):
#         initFunc = cls.initAlgorithm

#         def wrapper(self, *args, **kwargs):
#             self.addParameter(param)
#             initFunc(self, *args, **kwargs)

#         cls.initAlgorithm = wrapper
#         return cls

#     return class_decorator


# def output(param: QgsProcessingOutputDefinition):
#     def class_decorator(cls):
#         initFunc = cls.initAlgorithm

#         def wrapper(self, *args, **kwargs):
#             self.addOutput(param)
#             initFunc(self, *args, **kwargs)

#         cls.initAlgorithm = wrapper
#         return cls

#     return class_decorator


# @algo(name="foo")
# @param(QgsProcessingParameterString("SOMEVALUE", "Name"))
# @param(QgsProcessingParameterString("SOMEVALUE2", "Name2"))
# @output(QgsProcessingOutputMultipleLayers("SOMEVALUE3", "Output Layers"))
# class TestAlgorithm:
#     def displayName(self):
#         return self.tr("Test Algorithm")

#     def shortHelpString(self):
#         return self.tr("Test Algorithm")

#     def processAlgorithm(self, parameters, context, feedback):
#         return {}
