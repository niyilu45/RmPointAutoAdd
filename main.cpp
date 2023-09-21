#include "RmDumpDefine.h"
#include <stdlib.h>
#include <stdio.h>
#include <cstring>
#include <string>
#include "dumpClass.h"

#define RM_DUMP_FUNC_AAAA {\
    char fn[256] = {0}; \
    sprintf(fn, "RM_DUMP_FUNC_%s_AAAA.txt", ssType.c_str()); \
    DumpFile(fn, tti); \
}

//#define RM_DUMP_FUNC_AAAA tti++
void DumpFile(char* fn, int val)
{
    FILE* fp = fopen(fn, "w");
    fprintf(fp, "%d", val);
    fclose(fp);
}


int main(int argc, char* argv[])
{
    int tti = 99;
    std::string ssType = "CSS";
    int AVar = 11;
    std::string BVar = "OK";
    printf("This is for test auto gen rm dump\n");
    RM_DUMP_FUNC_6a40f16177a629cd3d298ba6bc68902a
    // RM_DUMP_FLAG: _name="monitor_{int:tti|[0:3]}.txt" || _vars = "AVar, BVar" RM_DUMP_FLAG_END
    RM_DUMP_FUNC_a6c80420d9a627180d5eab5c6a8e3d26
    // RM_DUMP_FLAG: _name="monitor_{int:tti|[0:3]}.txt" || _flag = "a+" || _vars = "AVar, BVar"RM_DUMP_FLAG_END

    RM_DUMP_FUNC_d099deace0747992355df3f9d741b15d
    // RM_DUMP_FLAG: _name="monitor_{string:ssType|['CSS', 'USS']}_cfg{int:tti|[1,2,4]}_ag.txt"|| _flag = "a+" || _en = 1 || _vars = "AVar" RM_DUMP_FLAG_END
    RM_DUMP_FUNC_ecd6f9813aec67e1f1a54d1c798be804
    // RM_DUMP_FLAG: _name="no_var_file.txt"|| _flag = "a+" RM_DUMP_FLAG_END
    RM_DUMP_FUNC_ecd6f9813aec67e1f1a54d1c798be804
    // RM_DUMP_FLAG: _name="no_var_file.txt"|| _flag = "a+" RM_DUMP_FLAG_END
    RM_DUMP_FUNC_ecd6f9813aec67e1f1a54d1c798be804
    // RM_DUMP_FLAG: _name="no_var_file.txt"|| _flag = "a+" RM_DUMP_FLAG_END
    //
    RM_DUMP_FUNC_598583eccde3d63a2aa00e56fcce9790
    // RM_DUMP_FLAG: _name="monitor_{string:ssType|['CSS', 'USS']}_cfg{int:tti|[1,2,4]}_ag.txt"|| _flag = "w+" || _en = 1 || _vars = "AVar" RM_DUMP_FLAG_END
    return 0;
}
