#ifndef _DUMPCLASS_H__
#define _DUMPCLASS_H__
#include <stdlib.h>
#include <stdio.h>
#include <cstring>
#include <string>

class DUMP_FUNC {

    public:
        DUMP_FUNC();
        static void DumpData(char* fn, const char* mode);
        static void DumpData(char* fn, const char* mode, int val);
        static void DumpData(char* fn, const char* mode, int val, std::string str);
};
#endif
