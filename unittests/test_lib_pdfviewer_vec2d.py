import imp_unittest, unittest
import wtc
import pickle

try:
    from wx.lib.pdfviewer.vec2d import vec2d
    havePyPDF = True
except ImportError:
    havePyPDF = False  # Assume an import error is due to missing pyPdf

#---------------------------------------------------------------------------

class lib_pdfviewer_vec2d_Tests(wtc.WidgetTestCase):
        
    @unittest.skipIf(not havePyPDF, "pyPdf required")
    def test_lib_pdfviewer_vec2d_CreationAndAccess(self):
        v = vec2d(111,222)
        self.assert_(v.x == 111 and v.y == 222)
        v.x = 333
        v[1] = 444
        self.assert_(v[0] == 333 and v[1] == 444)
    
    @unittest.skipIf(not havePyPDF, "pyPdf required")
    def test_lib_pdfviewer_vec2d_Math(self):
        v = vec2d(111,222)
        self.assertEqual(v + 1, vec2d(112,223))
        self.assert_(v - 2 == [109,220])
        self.assert_(v * 3 == (333,666))
        self.assert_(v / 2.0 == vec2d(55.5, 111))
        self.assert_(v / 2 == (55, 111))
        self.assert_(v ** vec2d(2,3) == [12321, 10941048])
        self.assert_(v + [-11, 78] == vec2d(100, 300))
        self.assert_(v / [11,2] == [10,111])
    
    @unittest.skipIf(not havePyPDF, "pyPdf required")
    def test_lib_pdfviewer_vec2d_ReverseMath(self):
        v = vec2d(111,222)
        self.assert_(1 + v == vec2d(112,223))
        self.assert_(2 - v == [-109,-220])
        self.assert_(3 * v == (333,666))
        self.assert_([222,999] / v == [2,4])
        self.assert_([111,222] ** vec2d(2,3) == [12321, 10941048])
        self.assert_([-11, 78] + v == vec2d(100, 300))
    
    @unittest.skipIf(not havePyPDF, "pyPdf required")
    def test_lib_pdfviewer_vec2d_Unary(self):
        v = vec2d(111,222)
        v = -v
        self.assert_(v == [-111,-222])
        v = abs(v)
        self.assert_(v == [111,222])
    
    @unittest.skipIf(not havePyPDF, "pyPdf required")
    def test_lib_pdfviewer_vec2d_Length(self):
        v = vec2d(3,4)
        self.assert_(v.length == 5)
        self.assert_(v.get_length_sqrd() == 25)
        self.assert_(v.normalize_return_length() == 5)
        self.assert_(v.length == 1)
        v.length = 5
        self.assert_(v == vec2d(3,4))
        v2 = vec2d(10, -2)
        self.assert_(v.get_distance(v2) == (v - v2).get_length())
        
    @unittest.skipIf(not havePyPDF, "pyPdf required")
    def test_lib_pdfviewer_vec2d_Angles(self):            
        v = vec2d(0, 3)
        self.assertEquals(v.angle, 90)
        v2 = vec2d(v)
        v.rotate(-90)
        self.assertEqual(v.get_angle_between(v2), 90)
        v2.angle -= 90
        self.assertEqual(v.length, v2.length)
        self.assertEquals(v2.angle, 0)
        self.assertEqual(v2, [3, 0])
        self.assert_((v - v2).length < .00001)
        self.assertEqual(v.length, v2.length)
        v2.rotate(300)
        self.assertAlmostEquals(v.get_angle_between(v2), -60)
        v2.rotate(v2.get_angle_between(v))
        angle = v.get_angle_between(v2)
        self.assertAlmostEquals(v.get_angle_between(v2), 0)  
    
    @unittest.skipIf(not havePyPDF, "pyPdf required")
    def test_lib_pdfviewer_vec2d_HighLevel(self):
        basis0 = vec2d(5.0, 0)
        basis1 = vec2d(0, .5)
        v = vec2d(10, 1)
        self.assert_(v.convert_to_basis(basis0, basis1) == [2, 2])
        self.assert_(v.projection(basis0) == (10, 0))
        self.assert_(basis0.dot(basis1) == 0)
        
    @unittest.skipIf(not havePyPDF, "pyPdf required")
    def test_lib_pdfviewer_vec2d_Cross(self):
        lhs = vec2d(1, .5)
        rhs = vec2d(4,6)
        self.assert_(lhs.cross(rhs) == 4)
        
    @unittest.skipIf(not havePyPDF, "pyPdf required")
    def test_lib_pdfviewer_vec2d_Comparison(self):
        int_vec = vec2d(3, -2)
        flt_vec = vec2d(3.0, -2.0)
        zero_vec = vec2d(0, 0)
        self.assert_(int_vec == flt_vec)
        self.assert_(int_vec != zero_vec)
        self.assert_((flt_vec == zero_vec) == False)
        self.assert_((flt_vec != int_vec) == False)
        self.assert_(int_vec == (3, -2))
        self.assert_(int_vec != [0, 0])
        self.assert_(int_vec != 5)
        self.assert_(int_vec != [3, -2, -5])
    
    @unittest.skipIf(not havePyPDF, "pyPdf required")
    def test_lib_pdfviewer_vec2d_Inplace(self):
        inplace_vec = vec2d(5, 13)
        inplace_ref = inplace_vec
        inplace_src = vec2d(inplace_vec)    
        inplace_vec *= .5
        inplace_vec += .5
        inplace_vec /= (3, 6)
        inplace_vec += vec2d(-1, -1)
        alternate = (inplace_src*.5 + .5)/vec2d(3,6) + [-1, -1]
        self.assertEquals(inplace_vec, inplace_ref)
        self.assertEquals(inplace_vec, alternate)
    
    @unittest.skipIf(not havePyPDF, "pyPdf required")
    def test_lib_pdfviewer_vec2d_Pickle(self):
        testvec = vec2d(5, .3)
        testvec_str = pickle.dumps(testvec)
        loaded_vec = pickle.loads(testvec_str)
        self.assertEquals(testvec, loaded_vec)
    

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
