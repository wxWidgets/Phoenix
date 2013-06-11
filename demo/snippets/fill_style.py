# For an explanation of the fill rules see
# http://cairographics.org/manual/cairo-cairo-t.html#cairo-fill-rule-t

snippet_normalize(cr, width, height)
cr.set_line_width(0.02)

cr.rectangle (0.04, 0.04, 0.90, 0.27);
cr.new_sub_path ();
cr.arc (0.25, 0.25, 0.15, 0, 2*M_PI);
cr.new_sub_path ();
cr.arc_negative (0.75, 0.25, 0.15, 0, -2*M_PI);

cr.set_fill_rule (cairo.FILL_RULE_EVEN_ODD);
cr.set_source_rgb (0, 0.7, 0);
cr.fill_preserve ();
cr.set_source_rgb (0, 0, 0);
cr.stroke ();

cr.translate (0, 0.50);
cr.rectangle (0.04, 0.04, 0.90, 0.27);
cr.new_sub_path ();
cr.arc (0.25, 0.25, 0.15, 0, 2*M_PI);
cr.new_sub_path ();
cr.arc_negative (0.75, 0.25, 0.15, 0, -2*M_PI);

cr.set_fill_rule (cairo.FILL_RULE_WINDING);
cr.set_source_rgb (0, 0, 0.9);
cr.fill_preserve ();
cr.set_source_rgb (0, 0, 0);
cr.stroke ();

