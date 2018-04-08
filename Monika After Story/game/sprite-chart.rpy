# This defines a dynamic displayable for Monika whose position and style changes
# depending on the variables is_sitting and the function morning_flag
define is_sitting = True

#body poses
image body_1 = im.Composite((1280,850),(0,0),"mod_assets/monika/torso.png",(0,0),"mod_assets/monika/arms-steepling.png")
image body_1_n = im.Composite((1280,850),(0,0),"mod_assets/monika/torso-n.png",(0,0),"mod_assets/monika/arms-steepling-n.png")
image body_2 = im.Composite((1280,850),(0,0),"mod_assets/monika/torso.png",(0,0),"mod_assets/monika/arms-crossed.png")
image body_2_n = im.Composite((1280,850),(0,0),"mod_assets/monika/torso-n.png",(0,0),"mod_assets/monika/arms-crossed-n.png")
image body_3 = im.Composite((1280,850),(0,0),"mod_assets/monika/torso.png",(0,0),"mod_assets/monika/arms-restleftpointright.png")
image body_3_n = im.Composite((1280,850),(0,0),"mod_assets/monika/torso-n.png",(0,0),"mod_assets/monika/arms-restleftpointright-n.png")
image body_4 = im.Composite((1280,850),(0,0),"mod_assets/monika/torso.png",(0,0),"mod_assets/monika/arms-pointright.png")
image body_4_n = im.Composite((1280,850),(0,0),"mod_assets/monika/torso-n.png",(0,0),"mod_assets/monika/arms-pointright-n.png")
image body_5 = im.Composite((1280,742),(0,0),"mod_assets/monika/body-leaning.png")
image body_5_n = im.Composite((1280,742),(0,0),"mod_assets/monika/body-leaning-n.png")

#faces
image face_s = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smile.png")
image face_s_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smile-n.png")
image face_a = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smile.png")
image face_a_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smile-n.png")
image face_b = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-big.png")
image face_b_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-big-n.png")
image face_c = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smirk.png")
image face_c_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smirk-n.png")
image face_d = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-small.png")
image face_d_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-small-n.png")
image face_e = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smile.png")
image face_e_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smile-n.png")
image face_f = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smirk.png")
image face_f_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smirk-n.png")
image face_g = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-small.png")
image face_g_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-small-n.png")
image face_h = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smirk.png")
image face_h_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smirk-n.png")
image face_i = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-small.png")
image face_i_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-small-n.png")
image face_j = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up.png",(0,0),"mod_assets/monika/face-eyes-closedhappy.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smile.png")
image face_j_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-eyes-closedhappy-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smile-n.png")
image face_k = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up.png",(0,0),"mod_assets/monika/face-eyes-closedhappy.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-big.png")
image face_k_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-eyes-closedhappy-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-big-n.png")
image face_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-eyebrows-knit.png",(0,0),"mod_assets/monika/face-eyes-closedhappy.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-big.png",(0,0),"mod_assets/monika/face-sweatdrop.png")
image face_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-eyes-closedhappy-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-big-n.png",(0,0),"mod_assets/monika/face-sweatdrop-n.png")
image face_m = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit.png",(0,0),"mod_assets/monika/face-eyes-left.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smile.png",(0,0),"mod_assets/monika/face-sweatdrop.png")
image face_m_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-eyes-left-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smile-n.png",(0,0),"mod_assets/monika/face-sweatdrop-n.png")
image face_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit.png",(0,0),"mod_assets/monika/face-eyes-left.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-big.png",(0,0),"mod_assets/monika/face-sweatdrop.png")
image face_n_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-eyes-left-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-big-n.png",(0,0),"mod_assets/monika/face-sweatdrop-n.png")
image face_o = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit.png",(0,0),"mod_assets/monika/face-eyes-left.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smirk.png",(0,0),"mod_assets/monika/face-sweatdrop.png")
image face_o_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-eyes-left-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smirk-n.png",(0,0),"mod_assets/monika/face-sweatdrop-n.png")
image face_p = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit.png",(0,0),"mod_assets/monika/face-eyes-left.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-small.png",(0,0),"mod_assets/monika/face-sweatdrop.png")
image face_p_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-eyes-left-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-small-n.png",(0,0),"mod_assets/monika/face-sweatdrop-n.png")
image face_q = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid.png",(0,0),"mod_assets/monika/face-eyes-closedsad.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smirk.png")
image face_q_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-eyes-closedsad-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smirk-n.png")
image face_r = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid.png",(0,0),"mod_assets/monika/face-eyes-closedsad.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-small.png")
image face_r_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-eyes-closedsad-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-small-n.png")

image face_s_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile.png")
image face_s_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile-n.png")
image face_a_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile.png")
image face_a_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile-n.png")
image face_b_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-big.png")
image face_b_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-big-n.png")
image face_c_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk.png")
image face_c_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk-n.png")
image face_d_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-small.png")
image face_d_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-small-n.png")
image face_e_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile.png")
image face_e_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile-n.png")
image face_f_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk.png")
image face_f_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk-n.png")
image face_g_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-small.png")
image face_g_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-small-n.png")
image face_h_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk.png")
image face_h_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk-n.png")
image face_i_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-small.png")
image face_i_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-small-n.png")
image face_j_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedhappy.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile.png")
image face_j_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedhappy-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile-n.png")
image face_k_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedhappy.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-big.png")
image face_k_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedhappy-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-big-n.png")
image face_l_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedhappy.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-big.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop.png")
image face_l_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedhappy-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-big-n.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop-n.png")
image face_m_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit.png",(0,0),"mod_assets/monika/face-leaning-eyes-left.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop.png")
image face_m_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-left-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile-n.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop-n.png")
image face_n_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit.png",(0,0),"mod_assets/monika/face-leaning-eyes-left.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-big.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop.png")
image face_n_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-left-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-big-n.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop-n.png")
image face_o_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit.png",(0,0),"mod_assets/monika/face-leaning-eyes-left.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop.png")
image face_o_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-left-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk-n.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop-n.png")
image face_p_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit.png",(0,0),"mod_assets/monika/face-leaning-eyes-left.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-small.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop.png")
image face_p_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-left-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-small-n.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop-n.png")
image face_q_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedsad.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk-n.png")
image face_q_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedsad-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk-n.png")
image face_r_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedsad.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-small-n.png")
image face_r_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedsad-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-small-n.png")

# Monika
image monika 1 = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_s"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_s_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/a.png")
            )
image monika 2 = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_s"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_s_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/a.png")
            )
image monika 3 = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_s"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_s_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/a.png")
            )
image monika 4 = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_s"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_s_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/a.png")
            )
image monika 5 = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,742),(0,0),"body_5",(0,0),"face_a_l"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,742),(0,0),"body_5_n",(0,0),"face_a_l_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/3a.png")
            )

image monika 1a = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_a"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_a_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/a.png")
            )
image monika 1b = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_b"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_b_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/b.png")
            )
image monika 1c = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_c"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_c_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/c.png")
            )
image monika 1d = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_d"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_d_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/d.png")
            )
image monika 1e = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_e"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_e_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/e.png")
            )
image monika 1f = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_f"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_f_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/f.png")
            )
image monika 1g = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_g"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_g_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/g.png")
            )
image monika 1h = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_h"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_h_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/h.png")
            )
image monika 1i = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_i"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_i_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/i.png")
            )
image monika 1j = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_j"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_j_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/j.png")
            )
image monika 1k = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_k"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_k_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/k.png")
            )
image monika 1l = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_l"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_l_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/l.png")
            )
image monika 1m = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_m"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_m_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/m.png")
            )
image monika 1n = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_n"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_n_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/n.png")
            )
image monika 1o = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_o"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_o_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/o.png")
            )
image monika 1p = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_p"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_p_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/p.png")
            )
image monika 1q = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_q"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_q_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/q.png")
            )
image monika 1r = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1",(0,0),"face_r"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_1_n",(0,0),"face_r_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/r.png")
            )

image monika 2a = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_a"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_a_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/a.png")
            )
image monika 2b = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_b"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_b_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/b.png")
            )
image monika 2c = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_c"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_c_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/c.png")
            )
image monika 2d = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_d"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_d_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/d.png")
            )
image monika 2e = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_e"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_e_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/e.png")
            )
image monika 2f = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_f"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_f_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/f.png")
            )
image monika 2g = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_g"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_g_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/g.png")
            )
image monika 2h = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_h"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_h_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/h.png")
            )
image monika 2i = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_i"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_i_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/i.png")
            )
image monika 2j = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_j"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_j_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/j.png")
            )
image monika 2k = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_k"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_k_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/k.png")
            )
image monika 2l = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_l"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_l_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/l.png")
            )
image monika 2m = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_m"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_m_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/m.png")
            )
image monika 2n = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_n"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_n_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/n.png")
            )
image monika 2o = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_o"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_o_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/o.png")
            )
image monika 2p = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_p"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_p_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/p.png")
            )
image monika 2q = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_q"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_q_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/q.png")
            )
image monika 2r = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2",(0,0),"face_r"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_2_n",(0,0),"face_r_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/2r.png", (0, 0), "monika/r.png")
            )

image monika 3a = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_a"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_a_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/a.png")
            )
image monika 3b = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_b"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_b_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/b.png")
            )
image monika 3c = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_c"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_c_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/c.png")
            )
image monika 3d = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_d"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_d_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/d.png")
            )
image monika 3e = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_e"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_e_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/e.png")
            )
image monika 3f = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_f"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_f_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/f.png")
            )
image monika 3g = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_g"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_g_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/g.png")
            )
image monika 3h = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_h"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_h_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/h.png")
            )
image monika 3i = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_i"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_i_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/i.png")
            )
image monika 3j = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_j"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_j_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/j.png")
            )
image monika 3k = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_k"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_k_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/k.png")
            )
image monika 3l = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_l"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_l_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/l.png")
            )
image monika 3m = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_m"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_m_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/m.png")
            )
image monika 3n = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_n"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_n_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/n.png")
            )
image monika 3o = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_o"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_o_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/o.png")
            )
image monika 3p = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_p"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_p_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/p.png")
            )
image monika 3q = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_q"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_q_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/q.png")
            )
image monika 3r = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3",(0,0),"face_r"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_3_n",(0,0),"face_r_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/1r.png", (0, 0), "monika/r.png")
            )

image monika 4a = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_a"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_a_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/a.png")
            )
image monika 4b = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_b"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_b_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/b.png")
            )
image monika 4c = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_c"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_c_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/c.png")
            )
image monika 4d = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_d"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_d_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/d.png")
            )
image monika 4e = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_e"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_e_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/e.png")
            )
image monika 4f = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_f"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_f_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/f.png")
            )
image monika 4g = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_g"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_g_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/g.png")
            )
image monika 4h = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_h"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_h_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/h.png")
            )
image monika 4i = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_i"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_i_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/i.png")
            )
image monika 4j = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_j"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_j_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/j.png")
            )
image monika 4k = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_k"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_k_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/k.png")
            )
image monika 4l = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_l"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_l_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/l.png")
            )
image monika 4m = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_m"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_m_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/m.png")
            )
image monika 4n = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_n"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_n_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/n.png")
            )
image monika 4o = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_o"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_o_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/o.png")
            )
image monika 4p = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_p"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_p_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/p.png")
            )
image monika 4q = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_q"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_q_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/q.png")
            )
image monika 4r = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_r"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_r_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/r.png")
            )

image monika 5a = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,742),(0,0),"body_5",(0,0),"face_a_l"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,742),(0,0),"body_5_n",(0,0),"face_a_l_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/3a.png")
            )
image monika 5b = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,742),(0,0),"body_5",(0,0),"face_h_l"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,742),(0,0),"body_5_n",(0,0),"face_h_l_n"),zoom=1.25),
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

init -1 python in mas_sprites:
    # specific image generation functions

    # main art path
    MOD_ART_PATH = "mod_assets/monika/"
    STOCK_ART_PATH = "monika/"

    # delimiters
    ART_DLM = "-"

    ### other paths:
    # H - hair (and body by connection)
    # C - clothing
    # T - sitting
    # S - standing
    # F - face parts
    # A - accessories
    C_MAIN = MOD_ART_PATH + "c/"
    F_MAIN = MOD_ART_PATH + "f/"
    A_MAIN = MOD_ART_PATH + "a/"

    # sitting standing parts
    T_MAIN = "sitting/"
    S_MAIN = "standing/"

    # facial parts
    F_T_MAIN = F_MAIN + T_MAIN
    F_S_MAIN = F_MAIN + S_MAIN
    
    # accessories TBD

    ### End paths

    # location stuff for some of the compsoite
    LOC_REG = "(1280, 850)"
    LOC_LEAN = "(1280, 742)"
    LOC_Z = "(0, 0)"
    LOC_STAND = "(960, 960)"

    # composite stuff
    I_COMP = "im.Composite"
    L_COMP = "LiveComposite"
    TRAN = "Transform"

    # zoom
    ZOOM = "zoom=1.25"

    # Prefixes for files
    PREFIX_BODY = "torso" + ART_DLM
    PREFIX_ARMS = "arms" + ART_DLM
    PREFIX_BODY_LEAN = "torso-leaning" + ART_DLM
    PREFIX_FACE = "face" + ART_DLM
    PREFIX_FACE_LEAN = "face-leaning" + ART_DLM
    PREFIX_EYEB = "eyebrows" + ART_DLM
    PREFIX_EYES = "eyes" + ART_DLM
    PREFIX_NOSE = "nose" + ART_DLM
    PREFIX_MOUTH = "mouth" + ART_DLM
    PREFIX_SWEAT = "sweatdrop" + ART_DLM
    PREFIX_EMOTE = "emote" + ART_DLM
    PREFIX_TEARS = "tears" + ART_DLM
    PREFIX_EYEG = "eyebags" + ART_DLM
    PREFIX_BLUSH = "blush" + ART_DLM

    # suffixes
    NIGHT_SUFFIX = ART_DLM + "n"
    FILE_EXT = ".png"


    def face_lean_mode(lean):
        """
        Returns the appropriate face prefix depending on lean

        IN:
            lean - type of lean

        RETURNS:
            appropriate face prefix
        """
        if lean:
            return "".join([PREFIX_FACE_LEAN, lean, ART_DLM])

        return PREFIX_FACE


    def night_mode(isnight):
        """
        Returns the appropriate night string
        """
        if isnight:
            return NIGHT_SUFFIX

        return ""

    # sprite maker functions
    def _ms_arms(clothing, hair, arms, isnight):
        """
        Creates arms string

        IN:
            clothing - type of clothing
            hair - type of hair
            arms - type of arms
            isnight - True will generate night string, false will not

        RETURNS:
            arms string
        """
        return "".join([
            LOC_Z,
            ',"',
            C_MAIN,
            clothing,
            "/",
            T_MAIN,
            PREFIX_ARMS,
            hair,
            ART_DLM,
            arms,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_blush(blush, isnight, lean=None):
        """
        Creates blush string

        IN:
            blush - type of blush
            isnight - True will generate night string, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            blush string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_BLUSH,
            blush,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_body(clothing, hair, isnight, lean=None, arms=""):
        """
        Creates body string

        IN:
            clothing - type of clothing
            hair - type of hair
            isnight - True will generate night string, false will not
            lean - type of lean
                (Default: None)
            arms - type of arms
                (Default: "")

        RETURNS:
            body string
        """
        if lean:
            # leaning is a single parter
            body_str = ",".join([
                LOC_LEAN,
                _ms_torsoleaning(clothing, hair, lean, isnight)
            ])

        else:
            # not leaning is a 2parter
            body_str = ",".join([
                LOC_REG,
                _ms_torso(clothing, hair, isnight),
                _ms_arms(clothing, hair, arms, isnight)
            ])

        # add the rest of the parts
        return "".join([
            I_COMP,
            "(",
            body_str,
            ")"
        ])


    def _ms_emote(emote, isnight, lean=None):
        """
        Creates emote string

        IN:
            emote - type of emote
            isnight - True will generate night string, false will not
            lean - type of lean
                (Dfeualt: None)

        RETURNS:
            emote string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_EMOTE,
            emote,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_eyebags(eyebags, isnight, lean=None):
        """
        Creates eyebags string

        IN:
            eyebags - type of eyebags
            isnight - True will generate night string, false will not
            lean - type of lean
                (Dfeault: None)

        RETURNS:
            eyebags string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_EYEG,
            eyebags,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_eyebrows(eyebrows, isnight, lean=None):
        """
        Creates eyebrow string

        IN:
            eyebrows - type of eyebrows
            isnight - True will generate night string, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            eyebrows string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_EYEB,
            eyebrows,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_eyes(eyes, isnight, lean=None):
        """
        Creates eyes string

        IN:
            eyes - type of eyes
            isnight - True will generate night string, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            eyes stirng
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_EYES,
            eyes,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])
            

    def _ms_face(
            eyebrows, 
            eyes, 
            nose, 
            mouth, 
            isnight, 
            lean=None,
            eyebags=None,
            sweat=None,
            blush=None,
            tears=None,
            emote=None
        ):
        """
        Create face string
        (the order these are drawn are in order of argument)

        IN:
            eyebrows - type of eyebrows
            eyes - type of eyes
            nose - type of nose
            mouth - type of mouth
            isnight - True will generate a night string, false will not
            lean - type of lean
                (Default: None)
            eyebags - type of eyebags
                (Default: None)
            sweat - type of sweat drop
                (Default: None)
            blush - type of blush
                (Default: None)
            tears - type of tears
                (Default: None)
            emote - type of emote
                (Default: None)

        RETURNS:
            face string
        """
        subparts = list()

        # lean checking
        if lean:
            subparts.append(LOC_LEAN)

        else:
            subparts.append(LOC_REG)
            
        # now for the required parts
        subparts.append(_ms_eyebrows(eyebrows, isnight, lean=lean))
        subparts.append(_ms_eyes(eyes, isnight, lean=lean))
        subparts.append(_ms_nose(nose, isnight, lean=lean))
        subparts.append(_ms_mouth(mouth, isnight, lean=lean))

        # and optional parts
        if eyebags:
            subparts.append(_ms_eyebags(eyebags, isnight, lean=lean))

        if sweat:
            subparts.append(_ms_sweat(sweat, isnight, lean=lean))

        if blush:
            subparts.append(_ms_blush(blush, isnight, lean=lean))

        if tears:
            subparts.append(_ms_tears(tears, isnight, lean=lean))

        if emote:
            subparts.append(_ms_emote(emote, isnight, lean=lean))

        # alright, now build the face string
        return "".join([
            I_COMP,
            "(",
            ",".join(subparts)
            ")"
        ])


    def _ms_mouth(mouth, isnight, lean=None):
        """
        Creates mouth string

        IN:
            mouth - type of mouse
            isnight - True will generate night string, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            mouth string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_MOUTH,
            mouth,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_nose(nose, isnight, lean=None):
        """
        Creates nose string

        IN:
            nose - type of nose
            isnight - True will genreate night string, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            nose string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_NOSE,
            nose,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_sitting(
            clothing, 
            hair,
            eyebrows,
            eyes,
            nose,
            mouth,
            isnight,
            lean=None,
            arms="",
            eyebags=None,
            sweat=None,
            blush=None,
            tears=None,
            emote=None
        ):
        """
        Creates sitting string

        IN:
            clothing - type of clothing
            hair - type of hair
            eyebrows - type of eyebrows
            eyes - type of eyes
            nose - type of nose
            mouth - type of mouth
            isnight - True will genreate night string, false will not
            lean - type of lean
                (Default: None)
            arms - type of arms
                (Default: "")
            eyebags - type of eyebags
                (Default: None)
            sweat - type of sweatdrop
                (Default: None)
            blush - type of blush
                (Default: None)
            tears - type of tears
                (Default: None)
            emote - type of emote
                (Default: None)

        RETURNS:
            sitting stirng
        """
        if lean:
            loc_str = LOC_LEAN

        else:
            loc_str = LOC_REG

        return "".join([
            TRAN,
            "(",
            L_COMP,
            "(",
            loc_str,
            ",",
            LOC_Z,
            ",",
            _ms_body(clothing, hair, isnight, lean=lean, arms=arms),
            ",",
            LOC_Z,
            ",",
            _ms_face(
                eyebrows,
                eyes,
                nose,
                mouth,
                isnight,
                lean=lean,
                eyebags=eyebags,
                sweat=sweat,
                blush=blush,
                tears=tears,
                emote=emote
            ),
            "),",
            ZOOM,
            ")"
        ])




    def _ms_sweat(sweat, isnight, lean=None):
        """
        Creates sweatdrop string
    
        IN:
            sweat -  type of sweatdrop
            isnight - True will generate night string, false will not
            lean - type of lean
                (Defualt: None)

        RETURNS:
            sweatdrop string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_SWEAT,
            sweat,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_tears(tears, isnight, lean=None):
        """
        Creates tear string

        IN:
            tears - type of tears
            isnight - True will generate night string, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            tear strring
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_TEARS,
            tears,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_torso(clothing, hair, isnight):
        """
        Creates torso string

        IN:
            clothing - type of clothing
            hair - type of hair
            isnight - True will generate night string, false will not

        RETURNS:
            torso string
        """
        return "".join([
            LOC_Z,
            ',"',
            C_MAIN,
            clothing,
            "/",
            T_MAIN,
            PREFIX_BODY,
            hair,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_torsoleaning(clothing, hair, lean, isnight):
        """
        Creates leaning torso string

        IN:
            clothing - type of clothing
            hair - type of ahri
            lean - type of leaning
            isnight - True will genreate night string, false will not

        RETURNS:
            leaning torso string
        """
        return "".join([
            LOC_Z,
            ',"',
            C_MAIN,
            clothing,
            "/",
            T_MAIN,
            PREFIX_BODY_LEAN,
            lean,
            ART_DLM,
            hair,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])

            
# Dynamic sprite builder
# retrieved from a Dress Up Renpy Cookbook
# https://lemmasoft.renai.us/forums/viewtopic.php?f=51&t=30643

init -2 python:
    import renpy.store as store
    import renpy.exports as renpy # we need this so Ren'Py properly handles rollback with classes
    from operator import attrgetter # we need this for sorting items
    import math

    # Monika character base
    class MASMonika(renpy.store.object):
        def __init__(self):
            self.name="Monika"
            self.haircut="default"
            self.haircolor="default"
            self.skin_hue=0 # monika probably doesn't have different skin color
            self.lipstick="default" # i guess no lipstick
            self.wearing=[] # no clothes is considered monika's school outfit 
            self.hair_hue=0 # hair color?
            
        def remove(self,clothes):
            if clothes in self.wearing:
                self.wearing.remove(clothes)
            return
        
        def wear(self,clothes):
            self.wearing.append(clothes)
            return
        
        def remove_all(self):
            list = [item for item in self.wearing if item.can_strip]
            if list!=[]:
                for item in list:
                    self.wearing.remove(item)
            return

    # hues, probably not going to use these
    hair_hue1 = im.matrix([ 1, 0, 0, 0, 0,
                        0, 1, 0, 0, 0,
                        0, 0, 1, 0, 0,
                        0, 0, 0, 1, 0 ])
    hair_hue2 = im.matrix([ 3.734, 0, 0, 0, 0,
                        0, 3.531, 0, 0, 0,
                        0, 0, 1.375, 0, 0,
                        0, 0, 0, 1, 0 ])
    hair_hue3 = im.matrix([ 3.718, 0, 0, 0, 0,
                        0, 3.703, 0, 0, 0,
                        0, 0, 3.781, 0, 0,
                        0, 0, 0, 1, 0 ])
    hair_hue4 = im.matrix([ 3.906, 0, 0, 0, 0,
                        0, 3.671, 0, 0, 0,
                        0, 0, 3.375, 0, 0,
                        0, 0, 0, 1, 0 ])
    skin_hue1 = hair_hue1
    skin_hue2 = im.matrix([ 0.925, 0, 0, 0, 0,
                        0, 0.840, 0, 0, 0,
                        0, 0, 0.806, 0, 0,
                        0, 0, 0, 1, 0 ])
    skin_hue3 = im.matrix([ 0.851, 0, 0, 0, 0,
                        0, 0.633, 0, 0, 0,
                        0, 0, 0.542, 0, 0,
                        0, 0, 0, 1, 0 ])
        
    hair_huearray = [hair_hue1,hair_hue2,hair_hue3,hair_hue4]
    
    skin_huearray = [skin_hue1,skin_hue2,skin_hue3]
            
            # Define a clothing item : a name, a pic and a priority order for drawing...
    
    class MASclothing(renpy.store.object):
        def __init__(self, name,pic,priority=10,bra=False,can_strip=True):
            self.name=name
            self.pic=pic
            self.priority=priority

            # this is for "Special Effects" like a scar or a wound, that 
            # shouldn't be removed by undressing.
            self.can_strip=can_strip 

            self.bra=bra # probably not using this
          

    def mas_drawsitting(
            character,
            body,
            arms,
            eyebrows,
            eyes,
            nose,
            smile,
            sweat=None
        ):
        """
        returns the command to draw monika in regular sitting position

        IN:
            character - MASMonika object
            body - selected body position
            arms - selected arms
            eyebrows - selected eyebrows
            eyes - selected eyes
            nose - selected nose
            smile - selected smile
            sweat - selected sweatdrop
                (Default: None)

        RETURNS:
            cmd for creating this monika
        """

        if sweat is not None:
            # sweat check
            sweat_str = ',(0,0),"mod_assets/monika/face-{sweat}'

#        if morning_flag:
            # morning time!


     
    # The main drawing function...
    # Monika consits of 5 parts when sitting and 2 parts when not:
    # sitting:  (also has a separate night version)
    #   4 parts of the face
    #   1 parts of the body
    # not sitting, most poses:
    #   1 left part of body 
    #   1 right part of body
    #   1 face
    # not sitting, pose 5:
    #   1 part, full body
    def draw_clothing(
            st,
            at,
            character,
            sitting=True, 
            expression="", 
            blushing=""
        ):
        """
        IN:
            st - renpy related
            at - renpy related
            character - MASMonika character object
            sitting - True if Monika is sitting down, false otherwise
                (Default: True)
            expression - expression code to display 
                (Default: None, which is a default expression)
            blushing - UNUSED
        """
        
        # Each item as a priority so we don't draw the blouse over the 
        # vest, etc
        list=sorted(character.wearing, key=attrgetter('priority')) 
        
        startpic= (
            "im.MatrixColor(\""+
            art_path+
            "_skin_pale.png\",skin_huearray["
            +str(character.skin_hue)+"])"
        )
        
        # Following bit of optional code was there for "boobs physics", or adapt it to more SFW ideas. 
        # I removed it for simplicity sake. The fundamental idea is that some clothing items affect the base body form we use
        
        #for item in list :
        #    if item.bra :
        #       startpic= art_path+"_skin_"+character.skin+"_bra.png"  
        # First composite the body with the face expression (passed through the function)    
        
        command_line="LiveComposite((344,600),(0,0),"+startpic
        command_line=command_line+",(0,0),\""+art_path+"_eye_pale_"+eyes+".png\""
        command_line=command_line+",(0,0),\""+art_path+"_mouth_"+mouth+"_"+character.lipstick+".png\""
        if blushing<>"":
             command_line=command_line+",(0,0),\""+art_path+"_blushing_"+blushing+".png\""
        command_line=command_line+",(0,0),im.MatrixColor(\""+art_path+"_hair_"+character.haircut+"_brunette.png\",hair_huearray["+str(character.hair_hue)+"])"
        
        # Then we draw each item the char is wearing.
        for item in list:
            command_line=command_line+",(0,0),\""+art_path+item.pic+"\""
        command_line=command_line+")"
        
        return eval(command_line),None # Unless you're using animations, you can set refresh rate to None
        
#init -1 python:
            
#    seraphim_jeans=clothing("Jeans","_jeans.png",5,True)
#    seraphim_leather_skirt=clothing("Leather Skirt","_leather_skirt.png",10)
#    seraphim_miniskirt_brown=clothing("Brown Mini Skirt","_miniskirt_brown.png",5)
#    seraphim_fishnet=clothing("Fishnet","_fishnet.png",1)
#    seraphim_stockings_black=clothing("Black Stockings","_stockings_black.png",1)
#    seraphim_tshirt_white=clothing("White Tshirt","_tshirt_white.png",5,True)
#    seraphim_tshirt_black=clothing("Black Tshirt","_tshirt_black.png",5,True)

#    seraphim_visor=clothing("Visor","_visor.png",15)
#    seraphim_power_armor=clothing("Power Armor","_power_armor.png",15)
    
#    seraphim_facial_scar=clothing("Facial Scar ","_facial_scar.png",1,False,False)
    
    # We sort the clothing by item type for the cloth select screen. Another option would be to create an inventory screen
#    tops = ["",seraphim_tshirt_white,seraphim_tshirt_black,seraphim_power_armor]
#    pants = ["",seraphim_leather_skirt,seraphim_miniskirt_brown,seraphim_jeans]
#    stockings = ["",seraphim_stockings_black,seraphim_fishnet]
#    eyewear = ["",seraphim_visor]
    
#init :
#    $ seraphim = PCstats("Seraphim")
    
#    image seraphim normal = DynamicDisplayable(draw_clothing,character=seraphim,art_path="seraphim/seraphim",mouth="normal",eyes="normal_straight")
#    image seraphim angry = DynamicDisplayable(draw_clothing,character=seraphim,art_path="seraphim/seraphim",mouth="grit",eyes="angry_straight")
#    image seraphim angry blushing = DynamicDisplayable(draw_clothing,character=seraphim,art_path="seraphim/seraphim",mouth="grit",eyes="angry_straight",blushing="light")

#    image side seraphim normal = LiveCrop((102,41,150,150),"seraphim normal")
#    image side seraphim angry = LiveCrop((102,41,150,150),"seraphim angry")
#    image side seraphim angry blushing = LiveCrop((102,41,150,150),"seraphim angry blushing")

#    define ser = Character(seraphim.name, color="#c8ffc8",image="seraphim",window_left_padding=150)

"""
label start:
    show seraphim normal at left
    ser "So I'll be part of this action game ? "
    ser angry "Hey !? Why am I not wearing any clothes ?"
    ser angry blushing "at least, I'm in underwear..."
    "Oops, sorry about that... Let's give you a power armor"
    $ seraphim.wear(seraphim_power_armor)
    $ seraphim.wear(seraphim_visor)
    ser normal "Much better! I though it was a different kind of game at first..."
    "Never crossed my mind..."
    "No, let's take a closer look"
    ser angry "Not TOO close, please..."
    hide seraphim
    jump body_selection

label body_selection:
    show seraphim normal at right
    menu:
        ser " Do I look ok like this ?"
        "Your skin should be":
            menu:
                "Deathly pale":
                    $ seraphim.skin_hue=0
                "Sorta pinkish...":
                    $ seraphim.skin_hue=1
                "Beach Tan":
                    $ seraphim.skin_hue=2
        "Your haircut should be":
            menu:
                "Long":
                    $ seraphim.haircut="long"
                "Short":
                    $ seraphim.haircut="short"
        "Your hair color should be":
            menu:
                "White":
                    $ seraphim.haircolor="white"
                "Blonde":
                    $ seraphim.haircolor="blonde"
                "Brunette":
                    $ seraphim.haircolor="brunette"
        "Increment Hue":
            $seraphim.hair_hue=(seraphim.hair_hue+1 )%len(hair_huearray)
            ser "[seraphim.hair_hue]"
        "About your make up":
            menu:
                "No lipstick":
                    $ seraphim.lipstick="nude"
                "Red lipstick":
                    $ seraphim.lipstick="red"
                "Purple lipstick":
                    $ seraphim.lipstick="purple"
        "You're fine as you are":
             jump clothes_selection_1
    jump body_selection

label clothes_selection_1:
    ser normal "I like this power armor, I look badass"
    "You know what's missing ? Some battle scars..."
    ser angry "Ouch!!"
    $ seraphim.wear(seraphim_facial_scar)
    ser angry "That hurts !!"
    $ seraphim.remove_all()
    ser angry "Hey !Not again!!"
    "It's only to demonstrate the remove function! Your scar is still in place, because it's defined as a 'permanent' clothing "
    ser normal "Great..."
    ser "Now can I get some clothes ?"
    "Sure..."
    $ index_e, index_t, index_p, index_s = 0,0,0,0
    jump clothes_selection_2

label clothes_selection_2:
    show seraphim at center
    $ seraphim.remove_all()
    python:
        if eyewear[index_e]!="":
            seraphim.wear(eyewear[index_e])
        if tops[index_t]!="":
            seraphim.wear(tops[index_t])
        if pants[index_p]!="":
            seraphim.wear(pants[index_p])
        if stockings[index_s]!="":
            seraphim.wear(stockings[index_s])
    
        # display the arrows for changing the dress:
        y = 50
        ui.imagebutton("arrowL.png", "arrowL.png", clicked=ui.returns(("eyewear","L")), ypos=y, xpos=150)
        ui.imagebutton("arrowR.png", "arrowR.png", clicked=ui.returns(("eyewear","R")), ypos=y, xpos=650)
        y += 80
        ui.imagebutton("arrowL.png", "arrowL.png", clicked=ui.returns(("tops","L")), ypos=y, xpos=150)
        ui.imagebutton("arrowR.png", "arrowR.png", clicked=ui.returns(("tops","R")), ypos=y, xpos=650)
        y += 80
        ui.imagebutton("arrowL.png", "arrowL.png", clicked=ui.returns(("pants","L")), ypos=y, xpos=150)
        ui.imagebutton("arrowR.png", "arrowR.png", clicked=ui.returns(("pants","R")), ypos=y, xpos=650)
        y += 80     
        ui.imagebutton("arrowL.png", "arrowL.png", clicked=ui.returns(("stockings","L")), ypos=y, xpos=150)
        ui.imagebutton("arrowR.png", "arrowR.png", clicked=ui.returns(("stockings","R")), ypos=y, xpos=650)
        
        ui.textbutton("Return", clicked=ui.returns("goback"), xpos=50, ypos=50)
    $ picked = ui.interact()
    if picked == "goback":
        jump startgame    
    if picked[0]=="eyewear":
        if picked[1] == "R":
            $ index_e+=1
        else:
            $ index_e-=1
        $ index_e = index_e %len(eyewear)
        
    if picked[0]=="tops":
        if picked[1] == "R":
            $ index_t+=1
        else:
            $ index_t-=1
        $ index_t = index_t %len(tops)
        
    if picked[0]=="pants":
        if picked[1] == "R":
            $ index_p+=1
        else:
            $ index_p-=1
        $ index_p = index_p %len(pants)
        
    if picked[0]=="stockings":
        if picked[1] == "R":
            $ index_s+=1
        else:
            $ index_s-=1
        $ index_s = index_s %len(stockings)
        
    jump clothes_selection_2

label startgame:
    show seraphim at right
    ser normal "That's what you want me to wear ?"
    ser "Have fun..."

"""
