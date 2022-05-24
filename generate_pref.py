"""
Generate Pref

Generate Pref for Maya/Arnold and other DCC like Houdini via Alembic.

Instructions

    Create Pref for Maya:
        Select mesh objects on viewport
        Select frame number in UI
        Press Generate button
        
    Create Pref for other DCCs:
        Select mesh objects on viewport
        Select frame number in UI
        Press Generate button
        Export selection to Alembic with "Pref" prefix attribute
        
    Delete Pref:
        Select mesh objects on viewport
        Press Generate button

Python 2 and Python 3
Maya 2018+

Bhavesh Budhkar
bhaveshbudhkar@yahoo.com
"""


from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
from sys import stdout
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import maya.cmds as cmds


def maya_main_window():
    """
    Maya Main Window Pointer
    :return: QtWidgets.QWidget Object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class GeneratePref(QtWidgets.QWidget):
    """
    Maya UI Class
    """

    def __init__(self, title, version, parent=maya_main_window()):
        """
        Maya UI Init
        :param title: Tool Name
        :param version: Tool Version
        :param parent: Parent Window
        """
        super(GeneratePref, self).__init__(parent)

        self.title = title
        self.version = version

        self.setWindowTitle("{0} v{1}".format(self.title, self.version))

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint | QtCore.Qt.Window)
        self.setFixedSize(350, 100)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        """
        Create UI Widgets
        :return: None
        """
        self.maya_checkbox = QtWidgets.QCheckBox("Maya")
        self.maya_checkbox.setChecked(True)
        self.houdini_checkbox = QtWidgets.QCheckBox("Houdini")

        self.frame_number_label = QtWidgets.QLabel("Frame Number")

        self.frame_number = QtWidgets.QSpinBox()
        self.frame_number.setRange(0, 100000)
        self.frame_number.setValue(1001)
        self.frame_number.setButtonSymbols(QtWidgets.QSpinBox.NoButtons)

        self.generate_button = QtWidgets.QPushButton("Generate")

        self.delete_button = QtWidgets.QPushButton("Delete")

        self.vertical_spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                                     QtWidgets.QSizePolicy.Expanding)

        self.author_label = QtWidgets.QLabel("Bhavesh Budhkar")
        self.author_label.setDisabled(True)
        self.author_label.setAlignment(QtCore.Qt.AlignLeft)

        self.email_label = QtWidgets.QLabel("bhaveshbudhkar@yahoo.com")
        self.email_label.setDisabled(True)
        self.email_label.setAlignment(QtCore.Qt.AlignRight)

    def create_layouts(self):
        """
        Create UI Layouts
        :return: None
        """
        self.info_layout = QtWidgets.QHBoxLayout()
        self.info_layout.addWidget(self.author_label)
        self.info_layout.addWidget(self.email_label)

        self.dcc_checkbox_layout = QtWidgets.QGridLayout()
        self.dcc_checkbox_layout.addWidget(self.maya_checkbox, 0, 0)
        self.dcc_checkbox_layout.addWidget(self.houdini_checkbox, 0, 1)

        self.pref_layout = QtWidgets.QHBoxLayout()
        self.pref_layout.addWidget(self.frame_number_label)
        self.pref_layout.addWidget(self.frame_number)
        self.pref_layout.addWidget(self.generate_button)
        self.pref_layout.addWidget(self.delete_button)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addLayout(self.dcc_checkbox_layout)
        self.main_layout.addLayout(self.pref_layout)
        self.main_layout.addSpacerItem(self.vertical_spacer)
        self.main_layout.addLayout(self.info_layout)

        self.setLayout(self.main_layout)

    def create_connections(self):
        """
        Signals and Slots
        :return: None
        """
        self.generate_button.clicked.connect(self.generate_pref)
        self.delete_button.clicked.connect(self.delete_pref)

    @staticmethod
    def get_current_fps(frame):
        """
        Get current FPS
        :param frame: Current Frame
        :return: None
        """
        # Define current FPS and frame
        fps = om.MTime.uiUnit()
        time = om.MTime(frame, fps)
        oma.MAnimControl.setCurrentTime(time)

    @staticmethod
    def get_selection():
        """
        Get viewport selection.
        :return: Selection List
        """
        # Get shape nodes based on selected group
        viewport_selection = cmds.ls(selection=True, long=True)
        shape = cmds.listRelatives(viewport_selection, type="shape", allDescendents=True, fullPath=True)

        # Generate list of Maya Python Objects from shapes list
        selection_list = om.MSelectionList()

        for obj in shape:
            selection_list.add(obj)

        return selection_list

    @staticmethod
    def create_maya_attribute(dependency_object, points_position, typed_attr):
        """
        Create Pref attributes for Maya.
        :param dependency_object: Maya Dependency Object
        :param points_position: Geometry Points Position
        :param typed_attr: Maya Typed Attribute
        :return: None
        """
        # Create Pref attribute
        mtoa_attr = typed_attr.create("mtoa_varying_Pref", "mtoa_varying_Pref",
                                      om.MFnPointArrayData.kPointArray,
                                      om.MFnPointArrayData().create(points_position))
        mtoa_str_attr = typed_attr.create("mtoa_varying_Pref_AbcGeomScope",
                                          "mtoa_varying_Pref_AbcGeomScope",
                                          om.MFnData.kString,
                                          om.MFnStringData().create("var"))

        dependency_object.addAttribute(mtoa_attr)
        dependency_object.addAttribute(mtoa_str_attr)

    @staticmethod
    def create_houdini_attribute(dependency_object, points_position, typed_attr):
        """
        Create Pref attributes for Houdini.
        :param dependency_object: Maya Dependency Object
        :param points_position: Geometry Points Position
        :param typed_attr: Maya Typed Attribute
        :return: None
        """
        # Create Pref attribute
        pref_attr = typed_attr.create("Pref", "Pref", om.MFnPointArrayData.kPointArray,
                                      om.MFnPointArrayData().create(points_position))
        pref_str_attr = typed_attr.create("Pref_AbcGeomScope", "Pref_AbcGeomScope",
                                          om.MFnData.kString,
                                          om.MFnStringData().create("var"))

        dependency_object.addAttribute(pref_attr)
        dependency_object.addAttribute(pref_str_attr)

    @staticmethod
    def delete_maya_attribute(dependency_object):
        """
        Delete Pref attributes for Maya.
        :param dependency_object: Maya Dependency Object
        :return: None
        """
        # Remove existing Pref attributes
        try:
            remove_mtoa_attr = dependency_object.findPlug("mtoa_varying_Pref", False)
            remove_mtoa_str_attr = dependency_object.findPlug("mtoa_varying_Pref_AbcGeomScope", False)

            dependency_object.removeAttribute(remove_mtoa_attr.attribute())
            dependency_object.removeAttribute(remove_mtoa_str_attr.attribute())
        except RuntimeError:
            pass

    @staticmethod
    def delete_houdini_attribute(dependency_object):
        """
        Delete Pref attributes for Houdini.
        :param dependency_object: Maya Dependency Object
        :return: None
        """
        try:
            remove_pref_attr = dependency_object.findPlug("Pref", False)
            remove_pref_str_attr = dependency_object.findPlug("Pref_AbcGeomScope", False)

            dependency_object.removeAttribute(remove_pref_attr.attribute())
            dependency_object.removeAttribute(remove_pref_str_attr.attribute())
        except RuntimeError:
            pass

    @staticmethod
    def create_attribute(selection_list, node):
        """
        Create Typed Attribute.
        :param selection_list: Viewport Selection List
        :param node: Per object Loop Variable
        :return: dependency_object, points_position, typed_attr
        """
        # DAG node
        dag_object = selection_list.getDagPath(node)
        dag_object_node = selection_list.getDagPath(node).node()

        # Dependency node to create custom attribute
        dependency_object = om.MFnDependencyNode(dag_object_node)

        # Mesh object
        mesh_object = om.MFnMesh(dag_object)

        # Object's vertex positions in world space
        points_position = mesh_object.getPoints(om.MSpace.kWorld)

        # Entitiy level attribute
        typed_attr = om.MFnTypedAttribute(dag_object_node)

        return dependency_object, points_position, typed_attr

    def maya_pref(self, dependency_object, points_position, typed_attr):
        """
        Create Pref attributes for Maya.
        :param dependency_object: Maya Dependency Object
        :param points_position: Geometry Points Position
        :param typed_attr: Maya Typed Attribute
        :return: None
        """
        self.delete_maya_attribute(dependency_object)
        self.create_maya_attribute(dependency_object, points_position, typed_attr)

    def houdini_pref(self, dependency_object, points_position, typed_attr):
        """
        Create Pref attributes for Houdini.
        :param dependency_object: Maya Dependency Object
        :param points_position: Geometry Points Position
        :param typed_attr: Maya Typed Attribute
        :return: None
        """
        self.delete_houdini_attribute(dependency_object)
        self.create_houdini_attribute(dependency_object, points_position, typed_attr)

    def generate_pref(self):
        """
        Generate Pref on selected objects on specified frame.
        :return: None
        """

        self.get_current_fps(self.frame_number.value())

        selection_list = self.get_selection()

        # Loop through selected objects
        if not selection_list.isEmpty():
            for node in range(selection_list.length()):
                dependency_object, points_position, typed_attr = self.create_attribute(selection_list, node)

                if self.maya_checkbox.isChecked() and self.houdini_checkbox.isChecked():
                    self.maya_pref(dependency_object, points_position, typed_attr)
                    self.houdini_pref(dependency_object, points_position, typed_attr)
                elif self.maya_checkbox.isChecked():
                    self.maya_pref(dependency_object, points_position, typed_attr)
                elif self.houdini_checkbox.isChecked():
                    self.houdini_pref(dependency_object, points_position, typed_attr)

            stdout.write("Pref is generated on selected objects on frame {0}.\n".format(self.frame_number.text()))
        else:
            om.MGlobal.displayWarning("Please select at least one Geometry.\n")

    def delete_pref(self):
        """
        Delete Pref on selected objects.
        :return: None
        """
        selection_list = self.get_selection()

        # Loop through selected objects
        if not selection_list.isEmpty():
            for node in range(selection_list.length()):
                dependency_object, points_position, typed_attr = self.create_attribute(selection_list, node)

                self.delete_maya_attribute(dependency_object)
                self.delete_houdini_attribute(dependency_object)
            stdout.write("Pref is delete on selected objects.\n")
        else:
            om.MGlobal.displayWarning("Please select at least one Geometry.\n")


if __name__ == "__main__":
    ui = GeneratePref("Generate Pref", 1.0)
    ui.show()
