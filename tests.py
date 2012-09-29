# -*- coding: UTF-8 -*-

import unittest
from google.appengine.ext import testbed
from curiosityimage import CuriosityImage
import getfeeds

class DemoTestCase(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()

        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()

        self.testbed.init_datastore_v3_stub()


        self.testImageLinkHtml =  '<table border="0" cellpadding="0" cellspacing="0" align="center">\n\
                <tr>\n\
                <td valign="top" align="center" width="200"><div style="margin:10px;"><a href="./?ImageID=4714"><img src="../../images/Grotzinger-2-pia16157-thm.jpg" alt="This map shows the path on Mars of NASA\'s Curiosity rover toward Glenelg, an area where three terrains of scientific interest converge." width="160" border="0"></a><br><div style="margin-top:5px;margin-bottom:10px;">Curiosity\'s Roadside Discoveries</div></div></td>\n\
                <td valign="top" align="center" width="200"><div style="margin:10px;"><a href="./?ImageID=4715"><img src="../../images/Grotzinger-3-pia16158REPLACE-small-thm.jpg" alt="This image shows the topography, with shading added, around the area where NASA\'s Curiosity rover landed on Aug. 5 PDT (Aug. 6 EDT)." width="160" border="0"></a><br><div style="margin-top:5px;margin-bottom:10px;">Where Water Flowed Downslope</div></div></td>\n\
                <td valign="top" align="center" width="200"><div style="margin:10px;"><a href="./?ImageID=4716"><img src="../../images/Grotzinger-4-pia16159smaller-thm.jpg" alt="This false-color map shows the area within Gale Crater on Mars, where NASA\'s Curiosity rover landed on Aug. 5, 2012 PDT (Aug. 6, 2012 EDT)." width="160" border="0"></a><br><div style="margin-top:5px;margin-bottom:10px;">Downslope of the Fan</div></div></td>\n\
                <td valign="top" align="center" width="200"><div style="margin:10px;"><a href="./?ImageID=4717"><img src="../../images/malin-4pia16187-thm.jpg" alt="This image from NASA\'s Curiosity Rover shows a high-resolution view of an area that is known as Goulburn Scour, a set of rocks blasted by the engines of Curiosity\'s descent stage on Mars." width="160" border="0"></a><br><div style="margin-top:5px;margin-bottom:10px;">Best View of Goulburn Scour</div></div></td>\n\
                <td valign="top" align="center" width="200"><div style="margin:10px;"><a href="./?ImageID=4719"><img src="../../images/Williams-2pia16188-thm.jpg" alt="In this image from NASA\'s Curiosity rover, a rock outcrop called Link pops out from a Martian surface that is elsewhere blanketed by reddish-brown dust. The fractured Link outcrop has blocks of exposed, clean surfaces." width="160" border="0"></a><br><div style="margin-top:5px;margin-bottom:10px;">Link to a Watery Past</div></div></td>\n\
                </tr><tr>'

        self.testImagePageHtml = '<div style="margin-top:10px !important;">\n\
                                <table border="0" cellpadding="10" cellspacing="0" align="center" width="700">\n\
                                <tr>\n\
                                <td align="center"><a href="../../images/Grotzinger-2-pia16157-br2.jpg"><img src="../../images/Grotzinger-2-pia16157-br.jpg" alt="This map shows the path on Mars of NASA\'s Curiosity rover toward Glenelg, an area where three terrains of scientific interest converge." border="0"></a></td>\n\
                                </tr>\n\
                                <tr>\n\
                                <td>\n\
                                <div style="margin-bottom:6px; font-style:italic;">09.27.2012</div>\n\
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

    def test_CuriosityImage_DataStoreGet(self):
        #Insert a basic CuriosityImage
        ci = CuriosityImage(key_name=str(42))
        ci.imageid = 42
        ci.description = 'DESC123'
        ci.put()

        dbCI = CuriosityImage.get_by_key_name(str(42))

        self.assertIsNotNone(dbCI)
        self.assertEquals(ci.description, dbCI.description)

    def test_SaveCuriosityImage_UpdateExistingCuriosityImage(self):
        #Insert a basic CuriosityImage
        ci = CuriosityImage(key_name=str(42))
        ci.imageid = 42
        ci.description = 'DESC123'
        ci.put()

        newCi = CuriosityImage(key_name=str(42))
        newCi.imageid = 42
        newCi.description = 'NEWDESC123'

        #Save to DB
        getfeeds.SaveCuriosityImage(newCi)

        #Get back from DB
        dbCI = CuriosityImage.get_by_key_name(str(42))

        self.assertEquals(u'NEWDESC123', dbCI.description)
        self.assertNotEquals(u'NEWDESC123', ci.description)

    def test_SaveCuriosityImage_InsertIfNotExists(self):

        self.assertIsNone(CuriosityImage.get_by_key_name(str(42)))

        newCi = CuriosityImage(key_name=str(42))
        newCi.imageid = 42
        newCi.description = 'DESC123'

        #Save to DB
        getfeeds.SaveCuriosityImage(newCi)

        self.assertIsNotNone(CuriosityImage.get_by_key_name(str(42)))


    def test_GetImageIDs_HtmlFragmentWithImages_ReturnsFiveImageIds(self):
        imageIds = getfeeds.GetImageIDs(self.testImageLinkHtml)
        self.assertEquals(5,len(imageIds))

    def test_GetImageIDs_HtmlFragmentWithImages_ReturnsImageIDAndAbsoluteThumbnails(self):
        imageIds = getfeeds.GetImageIDs(self.testImageLinkHtml)
        print imageIds
        self.assertIn((4714,'http://mars.jpl.nasa.gov/msl/images/Grotzinger-2-pia16157-thm.jpg'),imageIds)

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
        self.assertEqual('2012-09-27', str(date))

    def test_GetImageDescription_HtmlFragmentFromImagePage_GetDescription(self):
        description =getfeeds.GetImageDescription(self.testImagePageHtml)
        self.assertIn('topography', description)

    def test_GetImageDescription_HtmlFragmentFromImagePage_DoesntContainTd(self):
        description =getfeeds.GetImageDescription(self.testImagePageHtml)
        self.assertNotIn('<td>', description)

    def test_GetImageDescription_HtmlFragmentFromImagePage_NbspNotEscaped(self):
        description =getfeeds.GetImageDescription(self.testImagePageHtml)
        self.assertNotIn('&amp;nbsp;', description)
        self.assertIn('&nbsp;', description)

    def test_GetImageDescription_HtmlFragmentFromImagePage_WhiteSpaceRemoved(self):
        description = getfeeds.GetImageDescription(self.testImagePageHtml)
        self.assertNotIn('  ', description)

    def test_GetImageSrc_HtmlFragmentFromImagePage_GetsMediumImageUrl(self):
        imgUrl = getfeeds.GetMediumImageUrl(self.testImagePageHtml)
        print imgUrl
        self.assertIn('images/Grotzinger-2-pia16157-br2.jpg' , imgUrl)

    def test_GetImageSrc_HtmlFragmentFromImagePage_GetsMediumImageUrlAbsolute(self):
        imgUrl = getfeeds.GetMediumImageUrl(self.testImagePageHtml)
        print imgUrl
        self.assertEquals('http://mars.jpl.nasa.gov/msl/images/Grotzinger-2-pia16157-br2.jpg' , imgUrl)

