import unittest
from google.appengine.ext import testbed
import getfeeds

class DemoTestCase(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()

        self.testHtml =  '<table border="0" cellpadding="0" cellspacing="0" align="center">\n\
                <tr>\n\
                <td valign="top" align="center" width="200"><div style="margin:10px;"><a href="./?ImageID=4714"><img src="../../images/Grotzinger-2-pia16157-thm.jpg" alt="This map shows the path on Mars of NASA\'s Curiosity rover toward Glenelg, an area where three terrains of scientific interest converge." width="160" border="0"></a><br><div style="margin-top:5px;margin-bottom:10px;">Curiosity\'s Roadside Discoveries</div></div></td>\n\
                <td valign="top" align="center" width="200"><div style="margin:10px;"><a href="./?ImageID=4715"><img src="../../images/Grotzinger-3-pia16158REPLACE-small-thm.jpg" alt="This image shows the topography, with shading added, around the area where NASA\'s Curiosity rover landed on Aug. 5 PDT (Aug. 6 EDT)." width="160" border="0"></a><br><div style="margin-top:5px;margin-bottom:10px;">Where Water Flowed Downslope</div></div></td>\n\
                <td valign="top" align="center" width="200"><div style="margin:10px;"><a href="./?ImageID=4716"><img src="../../images/Grotzinger-4-pia16159smaller-thm.jpg" alt="This false-color map shows the area within Gale Crater on Mars, where NASA\'s Curiosity rover landed on Aug. 5, 2012 PDT (Aug. 6, 2012 EDT)." width="160" border="0"></a><br><div style="margin-top:5px;margin-bottom:10px;">Downslope of the Fan</div></div></td>\n\
                <td valign="top" align="center" width="200"><div style="margin:10px;"><a href="./?ImageID=4717"><img src="../../images/malin-4pia16187-thm.jpg" alt="This image from NASA\'s Curiosity Rover shows a high-resolution view of an area that is known as Goulburn Scour, a set of rocks blasted by the engines of Curiosity\'s descent stage on Mars." width="160" border="0"></a><br><div style="margin-top:5px;margin-bottom:10px;">Best View of Goulburn Scour</div></div></td>\n\
                <td valign="top" align="center" width="200"><div style="margin:10px;"><a href="./?ImageID=4719"><img src="../../images/Williams-2pia16188-thm.jpg" alt="In this image from NASA\'s Curiosity rover, a rock outcrop called Link pops out from a Martian surface that is elsewhere blanketed by reddish-brown dust. The fractured Link outcrop has blocks of exposed, clean surfaces." width="160" border="0"></a><br><div style="margin-top:5px;margin-bottom:10px;">Link to a Watery Past</div></div></td>\n\
                </tr><tr>'

    def tearDown(self):
        self.testbed.deactivate()


    def test_GetImageIDs_HtmlFragmentWithImages_ReturnsFiveImageIds(self):
        imageIds = getfeeds.GetImageIDs(self.testHtml)
        self.assertEquals(5,len(imageIds))

    def test_GetImageIDs_HtmlFragmentWithImages_ReturnsImageIDs(self):
        imageIds = getfeeds.GetImageIDs(self.testHtml)
        self.assertIn(4714,imageIds)


    def test_GetImageIDs_HtmlFragmentWithOutImages_ReturnsEmptyList(self):
        imageIds = getfeeds.GetImageIDs('')
        self.assertIsNotNone(imageIds)

    def test_GetImageIDs_NullString_ReturnsEmptyList(self):
        imageIds = getfeeds.GetImageIDs(None)
        self.assertIsNotNone(imageIds)

