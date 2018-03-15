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
