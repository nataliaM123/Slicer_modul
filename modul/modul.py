import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# modul
#

class modul(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "modul" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["John Doe (AnyWare Corp.)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    It performs a simple thresholding on the input volume and optionally captures a screenshot.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# modulWidget
#

class modulWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #

    # Collapsible button
    paramCollapsibleButton = ctk.ctkCollapsibleButton()
    paramCollapsibleButton.text = "Parameters"
    self.layout.addWidget(paramCollapsibleButton)


    parametersFormLayout2 = qt.QFormLayout(paramCollapsibleButton)
	
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ["vtkMRMLModelNode"]
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout2.addRow("Input Model: ", self.inputSelector)

    self.imageOpacitySliderWidget2 = ctk.ctkSliderWidget()
    self.imageOpacitySliderWidget2.singleStep = 0.1
    self.imageOpacitySliderWidget2.minimum = 0
    self.imageOpacitySliderWidget2.maximum = 100
    self.imageOpacitySliderWidget2.value = 100
    self.imageOpacitySliderWidget2.setToolTip("Set model opacity.")
    parametersFormLayout2.addRow("Model opacity:", self.imageOpacitySliderWidget2)

    self.changeVisibilityButton = qt.QPushButton("Change visibility of model.")
    self.changeVisibilityButton.toolTip = "Hide or show model."
    self.changeVisibilityButton.enabled = True
    parametersFormLayout2.addRow(self.changeVisibilityButton)
    
    # connections
    self.changeVisibilityButton.connect('clicked(bool)', self.onChangeVisibilityButton)
    self.imageOpacitySliderWidget2.connect('valueChanged(double)', self.onImageOpacitySliderWidget2)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass

  def onChangeVisibilityButton(self):
    logic = modulLogic()  
    logic.changeVisibility(self.inputSelector.currentNode())

  def onImageOpacitySliderWidget2(self):
    logic = modulLogic()
    imageOpacity = self.imageOpacitySliderWidget2.value
    logic.setNewOpacity(self.inputSelector.currentNode(), imageOpacity)

#
# modulLogic
#


class modulLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def hasImageData(self,volumeNode):
    """This is an example logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      logging.debug('hasImageData failed: no volume node')
      return False
    return True

  def changeVisibility(self, image):
    if not self.hasImageData( image):
      slicer.util.errorDisplay('Wrong input data')
      return False
    new_image = image.GetDisplayNode()
    state = new_image.GetVisibility()
    if (state==0):
      new_image.SetVisibility(1)
    else:
      new_image.SetVisibility(0) 

  def setNewOpacity(self, image, imageOpacity):
    if not self.hasImageData( image):
      slicer.util.errorDisplay('Wrong input data')
      return False
    new_image = image.GetDisplayNode()
    new_image.SetOpacity(imageOpacity/100)
    return True


class modulTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_modul1()

  def test_modul1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        logging.info('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        logging.info('Loading %s...' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = modulLogic()
    self.assertTrue( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
