#include "dumpClass.h"
DUMP_FUNC::DUMP_FUNC() {
    ;
}

void DUMP_FUNC::DumpData(char* fn, const char* mode){
    FILE* fp = fopen(fn, mode);
    fprintf(fp, "%s", "empty");
    fclose(fp);
}

void DUMP_FUNC::DumpData(char* fn, const char* mode, int val){
    FILE* fp = fopen(fn, mode);
    fprintf(fp, "%d", val);
    fclose(fp);
}
void DUMP_FUNC::DumpData(char* fn, const char* mode, int val, std::string str){
    FILE* fp = fopen(fn, mode);
    fprintf(fp, "%d %s", val, str.c_str());
    fclose(fp);
}
