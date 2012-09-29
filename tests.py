import unittest
from google.appengine.ext import testbed
import getfeeds

class DemoTestCase(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()

        self.testImageLinkHtml =  '<table border="0" cellpadding="0" cellspacing="0" align="center">\n\
                <tr>\n\
                <td valign="top" align="center" width="200"><div style="margin:10px;"><a href="./?ImageID=4714"><img src="../../images/Grotzinger-2-pia16157-thm.jpg" alt="This map shows the path on Mars of NASA\'s Curiosity rover toward Glenelg, an area where three terrains of scientific interest converge." width="160" border="0"></a><br><div style="margin-top:5px;margin-bottom:10px;">Curiosity\'s Roadside Discoveries</div></div></td>\n\
                <td valign="top" align="center" width="200"><div style="margin:10px;"><a href="./?ImageID=4715"><img src="../../images/Grotzinger-3-pia16158REPLACE-small-thm.jpg" alt="This image shows the topography, with shading added, around the area where NASA\'s Curiosity rover landed on Aug. 5 PDT (Aug. 6 EDT)." width="160" border="0"></a><br><div style="margin-top:5px;margin-bottom:10px;">Where Water Flowed Downslope</div></div></td>\n\
                <td valign="top" align="center" width="200"><div style="margin:10px;"><a href="./?ImageID=4716"><img src="../../images/Grotzinger-4-pia16159smaller-thm.jpg" alt="This false-color map shows the area within Gale Crater on Mars, where NASA\'s Curiosity rover landed on Aug. 5, 2012 PDT (Aug. 6, 2012 EDT)." width="160" border="0"></a><br><div style="margin-top:5px;margin-bottom:10px;">Downslope of the Fan</div></div></td>\n\
                <td valign="top" align="center" width="200"><div style="margin:10px;"><a href="./?ImageID=4717"><img src="../../images/malin-4pia16187-thm.jpg" alt="This image from NASA\'s Curiosity Rover shows a high-resolution view of an area that is known as Goulburn Scour, a set of rocks blasted by the engines of Curiosity\'s descent stage on Mars." width="160" border="0"></a><br><div style="margin-top:5px;margin-bottom:10px;">Best View of Goulburn Scour</div></div></td>\n\
                <td valign="top" align="center" width="200"><div style="margin:10px;"><a href="./?ImageID=4719"><img src="../../images/Williams-2pia16188-thm.jpg" alt="In this image from NASA\'s Curiosity rover, a rock outcrop called Link pops out from a Martian surface that is elsewhere blanketed by reddish-brown dust. The fractured Link outcrop has blocks of exposed, clean surfaces." width="160" border="0"></a><br><div style="margin-top:5px;margin-bottom:10px;">Link to a Watery Past</div></div></td>\n\
                </tr><tr>'

        self.testImagePageHtml = '<div style="margin-bottom:6px; font-style:italic;">09.27.2012</div>\n\
                                <strong>Where Water Flowed Downslope</strong>\n\
                                </td>\n\
                                </tr>\n\
                                <tr>\n\
                                <td>\n\
                                This image shows the topography, with shading added, around the area where NASA\'s Curiosity rover landed on Aug. 5 PDT (Aug. 6 EDT). Higher elevations are colored in red, with cooler colors indicating transitions downslope to lower elevations. The black oval indicates the targeted landing area for the rover known as the "landing ellipse," and the cross shows where the rover actually landed.<br><br>An alluvial fan, or fan-shaped deposit where debris spreads out downslope, has been highlighted in lighter colors for better viewing. On Earth, alluvial fans often are formed by water flowing downslope. New observations from Curiosity of rounded pebbles embedded with rocky outcrops provide concrete evidence that water did flow in this region on Mars, creating the alluvial fan. Water carrying the pebbly material is thought to have streamed downslope extending the alluvial fan, at least occasionally, to where the rover now sits studying its ancient history.\n\
                                Elevation data were obtained from stereo processing of images from the High Resolution Imaging Science Experiment (HiRISE) camera on NASA\'s Mars Reconnaissance Orbiter.\n\
                                <br><br><strong>Image Credit:</strong> NASA/JPL-Caltech/UofA\n\
                                <br><br><a href="../../images/Grotzinger-3-pia16158REPLACE-small-br.jpg">Browse Image</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="../../images/Grotzinger-3-pia16158REPLACE-small-br2.jpg">Medium Image</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="http://photojournal.jpl.nasa.gov/catalog/PIA16158" target="_blank">Full Res Image (NASA\'s Planetary Photojournal)</a>\n\
                                </td>'

    def tearDown(self):
        self.testbed.deactivate()


    def test_GetImageIDs_HtmlFragmentWithImages_ReturnsFiveImageIds(self):
        imageIds = getfeeds.GetImageIDs(self.testImageLinkHtml)
        self.assertEquals(5,len(imageIds))

    def test_GetImageIDs_HtmlFragmentWithImages_ReturnsImageIDs(self):
        imageIds = getfeeds.GetImageIDs(self.testImageLinkHtml)
        self.assertIn(4714,imageIds)


    def test_GetImageIDs_HtmlFragmentWithOutImages_ReturnsEmptyList(self):
        imageIds = getfeeds.GetImageIDs('')
        self.assertIsNotNone(imageIds)


    def test_GetImageTitle_HtmlFragmentFromImagePage_ReturnsTitle(self):
        imageTitle = getfeeds.GetImageTitle(self.testImagePageHtml)
        self.assertEquals('Where Water Flowed Downslope', imageTitle)

    def test_GetImageTitle_HtmlFragmentFromImagePage_ReturnsFirstStrong(self):
       imageTitle = getfeeds.GetImageTitle("<strong>First</strong> and <strong>Second</strong>")
       self.assertEquals('First', imageTitle)

    def test_GetImageTitle_HtmlFragmentWithoutStrong_ReturnsEmptyString(self):
       imageTitle = getfeeds.GetImageTitle('')
       self.assertEquals('', imageTitle)
       self.assertIsNotNone(imageTitle)

    def test_GetImageDate_HtmlFragmentFromImagePage_ReturnsDate(self):
        date = getfeeds.GetImageDate(self.testImagePageHtml)
        self.assertEqual('09.27.2012', date)

