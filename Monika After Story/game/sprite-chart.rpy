# This defines a dynamic displayable for Monika whose position and style changes
# depending on the variables is_sitting and the function is_morning()
define is_sitting = True

# Monika
image monika 1 = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/s.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/s-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/a.png")
            )
image monika 2 = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/s.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/s-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/a.png")
            )
image monika 3 = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/s.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/s-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/a.png")
            )
image monika 4 = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/s.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/s-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/a.png")
            )
image monika 5 = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/s.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/s-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/3a.png")
            )

image monika 1a = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/a.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/a-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/a.png")
            )
image monika 1b = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/b.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/b-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/b.png")
            )
image monika 1c = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/c.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/c-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/c.png")
            )
image monika 1d = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/d.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/d-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/d.png")
            )
image monika 1e = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/e.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/e-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/e.png")
            )
image monika 1f = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/f.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/f-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/f.png")
            )
image monika 1g = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/g.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/g-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/g.png")
            )
image monika 1h = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/h.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/h-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/h.png")
            )
image monika 1i = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/i.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/i-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/i.png")
            )
image monika 1j = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/j.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/j-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/j.png")
            )
image monika 1k = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/k.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/k-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/k.png")
            )
image monika 1l = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/l.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/l-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/l.png")
            )
image monika 1m = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/m.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/m-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/m.png")
            )
image monika 1n = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/n.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/n-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/n.png")
            )
image monika 1o = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/o.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/o-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/o.png")
            )
image monika 1p = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/p.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/p-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/p.png")
            )
image monika 1q = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/q.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/q-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/q.png")
            )
image monika 1r = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/r.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/r-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/r.png")
            )

image monika 2a = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/a.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/a-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/a.png")
            )
image monika 2b = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/b.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/b-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/b.png")
            )
image monika 2c = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/c.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/c-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/c.png")
            )
image monika 2d = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/d.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/d-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/d.png")
            )
image monika 2e = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/e.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/e-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/e.png")
            )
image monika 2f = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/f.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/f-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/f.png")
            )
image monika 2g = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/g.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/g-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/g.png")
            )
image monika 2h = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/h.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/h-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/h.png")
            )
image monika 2i = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/i.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/i-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/i.png")
            )
image monika 2j = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/j.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/j-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/j.png")
            )
image monika 2k = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/k.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/k-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/k.png")
            )
image monika 2l = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/l.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/l-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/l.png")
            )
image monika 2m = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/m.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/m-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/m.png")
            )
image monika 2n = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/n.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/n-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/n.png")
            )
image monika 2o = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/o.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/o-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/o.png")
            )
image monika 2p = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/p.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/p-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/p.png")
            )
image monika 2q = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/q.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/q-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/q.png")
            )
image monika 2r = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/r.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/r-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/r.png")
            )

image monika 3a = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/a.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/a-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/a.png")
            )
image monika 3b = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/b.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/b-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/b.png")
            )
image monika 3c = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/c.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/c-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/c.png")
            )
image monika 3d = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/d.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/d-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/d.png")
            )
image monika 3e = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/e.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/e-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/e.png")
            )
image monika 3f = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/f.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/f-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/f.png")
            )
image monika 3g = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/g.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/g-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/g.png")
            )
image monika 3h = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/h.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/h-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/h.png")
            )
image monika 3i = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/i.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/i-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/i.png")
            )
image monika 3j = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/j.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/j-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/j.png")
            )
image monika 3k = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/k.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/k-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/k.png")
            )
image monika 3l = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/l.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/l-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/l.png")
            )
image monika 3m = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/m.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/m-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/m.png")
            )
image monika 3n = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/n.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/n-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/n.png")
            )
image monika 3o = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/o.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/o-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/o.png")
            )
image monika 3p = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/p.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/p-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/p.png")
            )
image monika 3q = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/q.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/q-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/q.png")
            )
image monika 3r = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/r.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/r-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/r.png")
            )

image monika 4a = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/a.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/a-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/a.png")
            )
image monika 4b = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/b.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/b-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/b.png")
            )
image monika 4c = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/c.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/c-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/c.png")
            )
image monika 4d = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/d.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/d-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/d.png")
            )
image monika 4e = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/e.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/e-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/e.png")
            )
image monika 4f = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/f.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/f-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/f.png")
            )
image monika 4g = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/g.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/g-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/g.png")
            )
image monika 4h = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/h.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/h-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/h.png")
            )
image monika 4i = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/i.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/i-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/i.png")
            )
image monika 4j = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/j.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/j-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/j.png")
            )
image monika 4k = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/k.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/k-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/k.png")
            )
image monika 4l = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/l.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/l-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/l.png")
            )
image monika 4m = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/m.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/m-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/m.png")
            )
image monika 4n = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/n.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/n-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/n.png")
            )
image monika 4o = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/o.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/o-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/o.png")
            )
image monika 4p = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/p.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/p-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/p.png")
            )
image monika 4q = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/q.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/q-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/q.png")
            )
image monika 4r = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/r.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/r-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/r.png")
            )

image monika 5a = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/s.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/s-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/3a.png")
            )
image monika 5b = ConditionSwitch(
            'is_sitting and is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1.png", (502,107),"mod_assets/monika/s.png"),1.25),
            'is_sitting and not is_morning()',im.FactorScale(im.Composite((1280,742),(0,0),"mod_assets/monika/1-n.png", (502,107),"mod_assets/monika/h-n.png"),1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/3b.png")
            )

image monika g1:
    "monika/g1.png"
    xoffset 35 yoffset 55
    parallel:
        zoom 1.00
        linear 0.10 zoom 1.03
        repeat
    parallel:
        xoffset 35
        0.20
        xoffset 0
        0.05
        xoffset -10
        0.05
        xoffset 0
        0.05
        xoffset -80
        0.05
        repeat
    time 1.25
    xoffset 0 yoffset 0 zoom 1.00
    "monika 3"

image monika g2:
    block:
        choice:
            "monika/g2.png"
        choice:
            "monika/g3.png"
        choice:
            "monika/g4.png"
    block:
        choice:
            pause 0.05
        choice:
            pause 0.1
        choice:
            pause 0.15
        choice:
            pause 0.2
    repeat

define m = DynamicCharacter('m_name', image='monika', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
