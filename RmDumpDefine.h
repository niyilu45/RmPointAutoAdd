#ifndef RMDUMPDEFINE__H_
#define RMDUMPDEFINE__H_
#define RM_DUMP_FUNC_6a40f16177a629cd3d298ba6bc68902a { \
char fn[256] = {0}; \
sprintf(fn, "monitor_%d.txt", tti); \
DUMP_FUNC::DumpData(fn, "w", AVar, BVar); \
}
#define RM_DUMP_FUNC_a6c80420d9a627180d5eab5c6a8e3d26 { \
char fn[256] = {0}; \
sprintf(fn, "monitor_%d.txt", tti); \
DUMP_FUNC::DumpData(fn, "a+", AVar, BVar); \
}
#define RM_DUMP_FUNC_d099deace0747992355df3f9d741b15d { \
char fn[256] = {0}; \
sprintf(fn, "monitor_%s_cfg%d_ag.txt", ssType.c_str(), tti); \
DUMP_FUNC::DumpData(fn, "a+", AVar); \
}
#define RM_DUMP_FUNC_ecd6f9813aec67e1f1a54d1c798be804 { \
char fn[256] = {0}; \
sprintf(fn, "no_var_file.txt"); \
DUMP_FUNC::DumpData(fn, "a+"); \
}
#define RM_DUMP_FUNC_598583eccde3d63a2aa00e56fcce9790 { \
char fn[256] = {0}; \
sprintf(fn, "monitor_%s_cfg%d_ag.txt", ssType.c_str(), tti); \
DUMP_FUNC::DumpData(fn, "w+", AVar); \
}
#endif